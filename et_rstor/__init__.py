# -*- coding: utf-8 -*-
"""
Package et_rstor
================

A package for generating .rst documents with Python commands.

"""

from pathlib import Path
import subprocess
import shutil
import re
from contextlib import redirect_stdout, redirect_stderr, contextmanager
import io
import sys
import os
import traceback

__version__ = "1.1.2"


####################################################################################################
# RstDocument
####################################################################################################
class RstDocument:

    def __init__(self, name, width=72, headings_numbered_from_level=None, is_default_document=False):
        """Create a RstDocument.

        :param str name: name of the document, used as a filename for writing the document.
        :param int width: used by TextWrapper to convert long strings into lines.
        :param in_range(6) headings_numbered_from_level: heading level from which numbering will be used.
        :param bool is_default_document: if True any RstItem created without specifying a document will
            automatically be added to this RstDocument.
        """
        self.items = []
        self.name = name

        self.heading_numbers = 6*[-1]
        self.headings_numbered_from_level = 6 # = no numbering of headings

        self.width = width
        self.set_textwrapper()

        if headings_numbered_from_level < 6:
            self.headings_numbered_from_level = headings_numbered_from_level
            for l in range(headings_numbered_from_level,6):
                self.heading_numbers[l] = 0
        self.verbose = False
        if is_default_document:
            RstItem.default_document = self
        self.rst = ''


    def append(self, item):
        """Append an Rstitem item to this RstDocument."""
        self.items.append(item)

    def set_textwrapper(self, textwrapper=None):
        """Set a TextWrapper object for the RstDocument"""
        if textwrapper is None:
            self.textwrapper = TextWrapper(width=self.width)
        elif isinstance(textwrapper,TextWrapper):
            self.textwrapper = textwrapper
        else:
            raise ValueError('Argument must be a TextWrapper object.')


    def rstor(self):
        self.rst = ''
        for item in self.items:
            self.rst += item.rst
        return self.rst


    def write(self, path='.'):
        """Write the document to a file.

        :param (Path,str) path: directory to create the file in.
        """

        with path.open(mode='w') as f:
            f.write(str(self))


####################################################################################################
# Base classes
####################################################################################################
class RstItem():
    """Base class for items to be added to an RstDocument."""
    default_document = None
    
    def __init__(self, document):
        """Create RstItem.

        :param RstDocument document: document to append this RstItem to.
        """
        if document:
            self.document = document
        elif RstItem.default_document:
            self.document = RstItem.default_document
        else:
            self.document = None

        if self.document:
            self.document.append(self)


    def process(self):
        print(f"\nrstor> {self.__class__.__name__}")
        rst = self.rstor()
        print(f">>>>>>\n{rst}<<<<<<\n")


    def rstor(self):
        """convert content to rst format."""
        raise NotImplementedError()


####################################################################################################
# Heading
####################################################################################################
class Heading(RstItem):
    parameters = [('#',True)
                 ,('*',True)
                 ,('=',False)
                 ,('-',False)
                 ,('^',False)
                 ,('"',False)
                 ]
    def __init__(self, text, level=0, val=None, crosslink='', document=None):
        """Heading item.

        See https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#sections
        for standard.

        :param int level: 0-5.
        :param str text: heading text.
        """
        super().__init__(document=document)

        text = text.replace('\n', ' ')
        self.parms = Heading.parameters[level]
        if level >= self.document.headings_numbered_from_level:
            if val is None:
                self.document.heading_numbers[level] += 1
            else:
                self.document.heading_numbers[level] += val
            for l in range(level+1,6):
                self.document.heading_numbers[l] = 0
            self.text = ''
            for l in range(self.document.headings_numbered_from_level,level+1):
                self.text += f'{self.document.heading_numbers[l]}.'
            self.text += f" {text}"
        else:
            self.text = text
        self.crosslink = crosslink
        self.process()


    def rstor(self):
        text = ''
        if self.crosslink:
            text += f'.. _{self.crosslink}:\n\n'

        n = len(self.text)
        line = n * self.parms[0]
        if self.parms[1]:
            text += f'{line}\n{self.text}\n{line}\n\n'
        else:
            text += f'{self.text}\n{line}\n\n'
        self.rst = text
        return self.rst



####################################################################################################
# Paragraph
####################################################################################################
class Paragraph(RstItem):
    def __init__(self, text, width=72, indent=0, document=None):
        super().__init__(document=document)

        self.text = text
        self.width = width
        self.indent = indent*' '
        self.process()


    def rstor(self):
        lines = self.document.textwrapper.wrap(self.text)
        text = ''
        for line in lines:
            text += f'{self.indent}{line}\n'
        text += '\n'
        self.rst = text
        return self.rst


####################################################################################################
# Note
####################################################################################################
class Note(RstItem):
    def __init__(self, text, document=None):
        super().__init__(document=document)
        self.paragraphs = listify(text)
        self.process()

    def rstor(self):
        text = '.. note::\n\n'
        for paragraph in self.paragraphs:
            lines = self.document.textwrapper.wrap(paragraph)
            for line in lines:
                text += f'   {line}\n'
            text += '\n'
        self.rst = text
        return self.rst


####################################################################################################
# Include
####################################################################################################
class Include(RstItem):
    def __init__(self, filename, document=None):
        super().__init__(document=document)
        self.filename = filename
        self.process()

    def rstor(self):
        self.rst = f'.. include:: {self.filename}\n\n'
        return self.rst

####################################################################################################
# Image
####################################################################################################
class Image(RstItem):
    def __init__(self, filepath, document=None):
        super().__init__(document=document)
        self.filepath = filepath
        self.process()

    def rstor(self):
        self.rst = f'.. include:: {self.filepath}\n\n'
        return self.rst


####################################################################################################
# List
####################################################################################################
class List(RstItem):
    def __init__(self, items, numbered=False, indent=0, document=None):
        """List item, bulleted or numbered"""
        super().__init__(document=document)
        self.items = listify(items)
        self.numbered = numbered
        self.indent = indent*' '
        self.process()


    def rstor(self):
        bullet, indent2 = ('#.','  ') if self.numbered else ('*',' ')
        text = ''
        for item in self.items:
            lines = self.document.textwrapper.wrap(item)
            text += f'{self.indent}{bullet} {lines[0]}\n'
            for line in lines[1:]:
                text += f'{self.indent}{indent2} {line}\n'
            text += '\n'
        self.rst = text
        return self.rst


####################################################################################################
# CodeBlock
####################################################################################################
class CodeBlock(RstItem):
    default_prompts = { 'bash': '> '
                      , 'python': ''
                      , 'pycon': '>>> '
                      }

    def __init__( self, lines
                , language='', execute=False
                , indent=4
                , prompt=None
                , cwd='.', setup=None, cleanup=None, copyto=None, append=False
                , error_ok=False
                , document = None
                ):
        """

        :param lines: command or list of commands
        :param str language: language of the command
        :param bool execute: if True, execute the commands and add the output to the text. If False
            the lines are printed literally, no prompt is added.
        :param str prompt: prompt to appear in front of executed commands, ignored if execute==False.
        :param indent: indentation of the code-block
        :param callable() setup: function that has to be executed before the command lines.
        :param callable() cleanup: function that has to be executed before the command lines.
        :param Path copyto: copy the code to this file.
        :param bool append: append the code to copyto instead of copy.
        """
        super().__init__(document=document)
        self.lines = listify(lines)
        self.language = language

        if prompt is None:
            self.prompt = CodeBlock.default_prompts.get(language,'')
        else:
            self.prompt = prompt

        self.indent = indent*' '
        self.execute = execute
        self.cwd = cwd
        self.setup = setup
        self.cleanup = cleanup
        self.copyto = copyto
        self.append = append
        self.error_ok = error_ok
        self.process()


    def rstor(self):
        text = f'.. code-block:: {self.language}\n\n'

        if self.execute:
            if self.setup:
                self.setup()
            if self.language == 'bash':
                for line in self.lines:
                    print(f"{self.language}@ {line}")
                    text += f'{self.indent}{self.prompt}{line}\n'
                    # execute the command and add its output
                    completed_process = subprocess.run( line
                                                      , cwd=self.cwd
                                                      , stdout=subprocess.PIPE
                                                      , stderr=subprocess.STDOUT
                                                      , shell=True
                                                      )
                    output = self.indent + completed_process.stdout.decode('utf-8').replace('\n', '\n'+self.indent)
                    if completed_process.returncode and not self.error_ok:
                        print(output)
                        raise RuntimeError()
                    text += output+'\n'

            elif self.language == 'pycon':
                sys.path.insert(0,'.')
                print(self.cwd)
                with in_directory(self.cwd):
                    output = ''
                    for line in self.lines:
                        print(f"{self.language}@ {line}")
                        hide = line.endswith('#hide#')
                        stdout = io.StringIO()
                        with redirect_stdout(stdout):
                            if not hide:
                                output += f"{self.prompt}{line}\n"
                            try:
                                exec(line)
                            except:
                                if self.error_ok:
                                    print(traceback.format_exc())
                                else:
                                    raise
                            if not hide:
                                output += stdout.getvalue()

                    # indent the output if necessary
                    if self.indent:
                        output = self.indent + output.replace('\n', '\n' + self.indent)
                    text += '\n>>>\n' + output + '\n'

            else:
                raise NotImplementedError()

            if self.cleanup:
                self.cleanup()
        else:
            text = f'.. code-block:: {self.language}\n\n'
            for line in self.lines:
                if not line.endswith('#hide#'):
                    text += f'{self.indent}{self.prompt}{line}\n'

        text += '\n'

        if self.copyto :
            self.copyto.parent.mkdir(parents=True,exist_ok=True)
            mode = 'a+' if self.append else 'w'
            with self.copyto.open(mode=mode) as f:
                for line in self.lines:
                    f.write(line + '\n')

        self.rst = text
        return self.rst


####################################################################################################
# Utilities
####################################################################################################
def listify(obj,types=str):
    """If obj is a list verify that the type of its items are  in types. Otherwise verify that the
    type of obj is in types, and put obj in a list.

    Raises ValueError if the type of obj is not in types or if obj is a list and not all its items
    have a type in types.

    :param obj: an object.
    :param tuple types: tuple of accepted types.
    :return: list of objects whose type is in types
    """
    if isinstance(obj, list):
        pass
    elif isinstance(obj, types):
        obj = [obj]
    else:
        raise ValueError(f'Expecting type {types}, or list of {types}, got {type(obj)}.')

    # Validate
    for i,item in enumerate(obj):
        if not isinstance(item, types):
            raise ValueError(f'Item {i} must be of type {types}.')

    return obj

class RemoveDir:
    def __init__(self, cwd, dir, document=None):
        self.cwd = Path(cwd)
        self.pdir = self.cwd / dir

    def __call__(self):
        if self.pdir.is_dir():
            shutil.rmtree(self.pdir)


def package_name_of(project_name):
    """
    :param str project_name:
    """
    return project_name.lower().replace('-','_')


class TextWrapper:
    """Our own TextWrapper class.

    textwrapper.TextWrapper is not able to keep inline formatted strings
    together. E.g.::

        Part of this text appears in **bold face**.

    textwrapper.TextWrapper will first detect the words::

        'Part', 'of', 'this', 'text', 'appears', 'in', '**bold', 'face**.'

    and then combine them back into words.
    If the word '**bold' appears at the end of the line, there is a chance
    that the next word 'face**' will appear only on the next line, which
    destroys the intended formatting restructuredText.

    Patterns that need to be kept together:

    * '*italics text*
    * '**bold face text**'
    * ``inline monospace``
    * links: `text <url>`_
    * things like :file:`may occasionally contain spaces`, are ignored for the time being.

    Note that these patterns may be followed with punctuation: . , : ; ... ? ! ) ] } ' "
    """
    patterns = \
    ( ( re.compile(r"\A\*(\w+)")  , re.compile(r"(\w+)\*([,.:;!?\"\')}]?|(\.\.\.))\Z") )    # italics
    , ( re.compile(r"\A\*\*(\w+)"), re.compile(r"(\w+)\*\*([,.:;!?\"\')}]?|(\.\.\.))\Z") )  # bold face
    , ( re.compile(r"\A``(\w+)")  , re.compile(r"(\w+)``([,.:;!?\"\')}]?|(\.\.\.))\Z") )    # inline code sample
    , ( re.compile(r"\A`(\w+)")                                                             # hyperlink
      , re.compile(r"<(((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*)>`_([,.:;!?\"\')}]?|(\.\.\.))\Z") )
    )

    def __init__(self,width=72):
        """"""
        self.width = width
        self.lookahead = 10

    def wrap(self, text):
        """"""
        # split text in words
        words = text.split(' ')

        # join words that should not have been split
        n = len(words)
        i = 0
        while i < n:
            word0 = words[i]
            found = False
            for p in TextWrapper.patterns:
                if found:
                    break
                m0 = p[0].match(word0)
                if m0:
                    # begin of pattern found
                    for j in range(1,self.lookahead+1):
                        if i+j >= n:
                            break
                        word1 = words[i+j]
                        m1 = p[1].match(word1)
                        if m1:
                            # end of pattern found, append all words to the wo
                            words[i] = ' '.join(words[i:i+j+1])
                            # pop the words that were appended to words[i]
                            for k in range(j):
                                words.pop(i+1)
                                n -= 1
                            found = True
                            break
            # print(words[i]) # for debugging
            i += 1

        # build lines out of the words
        lines = []
        i = 0
        i0 = i
        space_left = self.width
        while i < n:
            word_len = len(words[i])
            if word_len > self.width: # a very long word
                if i0 < i:
                    lines.append(' '.join(words[i0:i]))
                    lines.append(words[i])
                    # print(lines[-2])
                    # print(lines[-1])
                    i0 = i+1
                    space_left = self.width
            else:
                space_left -= word_len
                if space_left < 0:
                    lines.append(' '.join(words[i0:i]))
                    # print(lines[-1])
                    i0 = i
                    space_left = self.width - word_len
            i += 1
        lines.append(' '.join(words[i0:]))
        return lines


@contextmanager
def in_directory(path):
    """Context manager for changing the current working directory while the body of the
    context manager executes.
    """
    previous_dir = os.getcwd()
    os.chdir(str(path)) # the str method takes care of when path is a Path object
    try:
        yield os.getcwd()
    finally:
        os.chdir(previous_dir)
