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

    def __init__( self, name
                , headings_numbered_from_level=None
                , is_default_document=False
                , verbose=True
                , width=72
                ):
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

        if is_default_document:
            RstItem.default_document = self

        self.verbose = verbose

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
        """Concatenate all RstItems"""
        self.rst = ''
        for item in self.items:
            self.rst += item.rst


    # def __str__(self):
    #     if not self.rst:
    #         self.rstor()
    #     return self.rst


    def write(self, path='.'):
        """Write the document to a file.

        :param (Path,str) path: directory to create the file in.
        """
        if not self.rst:
            self.rstor()
        p = path / f'{self.name}.rst'
        with p.open(mode='w') as f:
            f.write(self.rst)


####################################################################################################
# Base classes
####################################################################################################
class RstItem():
    """Base class for items to be added to an RstDocument.

    Derived classes must:

    * call ``self.rstor()`` at the end of the ctor.
    * reimplement :py:meth:`rstor()`

    :param RstDocument document: document to append this RstItem to.
    """
    default_document = None

    def __init__(self, document):
        """Create an RstItem and add it to document (if not None)."""
        if document:
            self.document = document
        elif RstItem.default_document:
            self.document = RstItem.default_document
        else:
            self.document = None

        if self.document:
            self.document.append(self)


    def show_progress(self):
        if self.document.verbose:
            print(f"\nrstor> {self.__class__.__name__}")
            print(f"$$$$$$\n{self.rst}$$$$$$\n")


    def rstor(self):
        """Convert RstItem content to ``.rst`` format.

        This method must be implemented by every derived class.
        """
        raise NotImplementedError()


    # def __str__(self):
    #     if not self.rst:
    #         self.rstor()
    #     return self.rst

####################################################################################################
# Heading
####################################################################################################
class Heading(RstItem):
    """Heading item.

    See https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#sections
    for standard.

    :param int level: 0-5.
    :param str text: heading text.
    """
    parameters = [('#',True)
                 ,('*',True)
                 ,('=',False)
                 ,('-',False)
                 ,('^',False)
                 ,('"',False)
                 ]

    def __init__(self, heading, level=0, val=None, crosslink='', document=None):
        super().__init__(document=document)
        self.parms = Heading.parameters[level]

        self.heading = heading.replace('\n', ' ')
        if level >= self.document.headings_numbered_from_level:
            if val is None:
                self.document.heading_numbers[level] += 1
            else:
                self.document.heading_numbers[level] = val
            for l in range(level+1,6):
                self.document.heading_numbers[l] = 0
            numbering = ''
            for l in range(self.document.headings_numbered_from_level,level+1):
                numbering += f'{self.document.heading_numbers[l]}.'
            self.heading = f"{numbering} {self.heading}"

        self.crosslink = crosslink

        self.rstor()
        self.show_progress()


    def rstor(self):
        self.rst = ''
        if self.crosslink:
            self.rst += f'.. _{self.crosslink}:\n\n'

        n = len(self.heading)
        underline = n * self.parms[0]
        if self.parms[1]:
            self.rst += f'{underline}\n' \
                        f'{self.heading}\n' \
                        f'{underline}\n\n'
        else:
            self.rst += f'{self.heading}\n' \
                        f'{underline}\n\n'


####################################################################################################
# Paragraph
####################################################################################################
class Paragraph(RstItem):
    def __init__(self, text, width=72, indent=0, document=None):
        super().__init__(document=document)
        self.text = text
        self.width = width
        self.indent = indent*' '
        self.rstor()
        self.show_progress()


    def rstor(self):
        lines = self.document.textwrapper.wrap(self.text)
        self.rst = ''
        for line in lines:
            self.rst += f'{self.indent}{line}\n'
        self.rst += '\n'


####################################################################################################
# Note
####################################################################################################
class Note(RstItem):
    def __init__(self, text, document=None):
        super().__init__(document=document)
        self.paragraphs = listify(text)
        self.rstor()
        self.show_progress()


    def rstor(self):
        self.rst = '.. note::\n\n'
        for paragraph in self.paragraphs:
            lines = self.document.textwrapper.wrap(paragraph)
            for line in lines:
                self.rst += f'   {line}\n'
            self.rst += '\n'


####################################################################################################
# Include
####################################################################################################
class Include(RstItem):
    def __init__(self, filename, document=None):
        super().__init__(document=document)
        self.include_file = filename
        self.rstor()
        self.show_progress()


    def rstor(self):
        self.rst = f'.. include:: {self.include_file}\n\n'


####################################################################################################
# Image
####################################################################################################
class Image(RstItem):
    def __init__(self, filepath, document=None):
        super().__init__(document=document)
        self.filepath = filepath
        self.rstor()
        self.show_progress()


    def rstor(self):
        self.rst = f'.. include:: {self.filepath}\n\n'


####################################################################################################
# List
####################################################################################################
class List(RstItem):
    def __init__(self, items, numbered=False, indent=0, document=None):
        """List item, bullets or numbered"""
        super().__init__(document=document)
        self.items = listify(items)
        self.numbered = numbered
        self.indent = indent*' '
        self.rstor()
        self.show_progress()


    def rstor(self):
        bullet, indent2 = ('#.','  ') if self.numbered else ('*',' ')
        self.rst = ''
        for item in self.items:
            lines = self.document.textwrapper.wrap(item)
            self.rst += f'{self.indent}{bullet} {lines[0]}\n'
            for line in lines[1:]:
                self.rst += f'{self.indent}{indent2} {line}\n'
            self.rst += '\n'


####################################################################################################
# CodeBlock
####################################################################################################
class CodeBlock(RstItem):
    """Rst code-block directive.

    :param lines: command or list of commands
    :param str language: language of the commands
    :param bool execute: if True, execute the commands and add the output to the text. If False
        the lines are printed literally, no prompt is added.
    :param bool error_ok: if True, exceptions raised will be absorbed by the .rst text instead
        of propagated to Python (which will abort the script)
    :param str prompt: prompt to appear in front of the commands or statements, ignored if execute==False.
    :param indent: indentation of the code-block. default=4
    :param Path copyto: copy the code to this file.
    :param bool append: append the code to the copyto destination instead of overwriting.
    :param callable() setup: function that has to be executed before the command lines.
    :param callable() cleanup: function that has to be executed before the command lines.

    .. warning::

            language=='pycon': if a module has been modified it must be reloaded (importlib.reload).
            However, reloading a binary extension does not work. the CodeBlock must be executed in
            a separate Python session.
    """

    default_prompts = { 'bash': '> '
                      , 'python': ''
                      , 'pycon': '>>> '
                      }

    def __init__( self
                , lines=[]
                , language=''
                , execute=False
                , cwd='.'
                , error_ok=False
                , stdout=True
                , stderr=True
                , hide=False
                , indent=4
                , prompt=None
                , copyto=None, append=False
                , copyfrom=None, filter=None
                , setup=None, cleanup=None
                , document = None
                ):
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
        self.error_ok = error_ok
        self.stdout = stdout
        self.stderr = stderr
        self.hide = hide
        self.copyto = copyto
        self.copyfrom = copyfrom
        self.filter = filter
        self.append = append
        self.setup = setup
        self.cleanup = cleanup

        if self.document.verbose:
            print(f"\nrstor> {self.__class__.__name__}{' (hidden)' if self.hide else ''}")

        self.rstor()

        if self.document.verbose and not self.hide:
            print(f"$$$$$$\n{self.rst}$$$$$$\n")


    def rstor(self):
        self.rst = ''

        if not self.hide:
            self.rst = f'.. code-block:: {self.language}\n\n'

        if self.copyfrom:
            with self.copyfrom.open(mode='r') as f:
                self.lines = f.readlines()
            # Remove trailing newlines and withspace
            for l,line in enumerate(self.lines):
                self.lines[l] = line.rstrip()
            if self.filter:
                self.lines = self.filter(self.lines)

        if self.execute:
            if not self.language:
                self.language='bash' # default

            if self.setup:
                self.setup()
            if self.language == 'bash':
                for line in self.lines:
                    print(f"{self.language}@ {line}")
                    if not self.hide:
                        self.rst += f'{self.indent}{self.prompt}{line}\n'
                    # execute the command and add its output
                    self.stdout = subprocess.PIPE if self.stdout else None
                    self.stderr = subprocess.STDOUT if self.stderr else None
                    completed_process = subprocess.run( line
                                                      , cwd=self.cwd
                                                      , stdout=self.stdout
                                                      , stderr=self.stderr
                                                      , shell=True
                                                      )
                    if not self.hide:
                        output = completed_process.stdout.decode('utf-8')
                        if self.indent:
                            output = self.indent + output.replace('\n', '\n'+self.indent)
                        self.rst += output+'\n'

                    if completed_process.returncode and not self.error_ok:
                        print(output)
                        raise RuntimeError()

            elif self.language == 'pycon':
                sys.path.insert(0,'.')
                # print(self.cwd)
                with in_directory(self.cwd):
                    output = ''
                    for line in self.lines:
                        print(f"{self.language}@ {line}") # show progress
                        hide_line = '#hide#' in line
                        hide_stdout = '#hide_stdout#' in line
                        hide_stderr = '#hide_stderr#' in line
                        str_stdout = io.StringIO()
                        str_stderr = io.StringIO()
                        with redirect_stderr(str_stderr):
                            with redirect_stdout(str_stdout):
                                if not hide_line:
                                    output += f"{self.prompt}{line}\n"
                                try:
                                    exec(line)
                                except:
                                    if self.error_ok:
                                        print(traceback.format_exc())
                                    else:
                                        raise
                                o = str_stdout.getvalue()
                                if o and not hide_stdout:
                                    output += o
                                e = str_stderr.getvalue()
                                if e and not hide_stderr:
                                    output += e

                    # indent the output if necessary
                    if self.indent:
                        output = self.indent + output.replace('\n', '\n' + self.indent)

                    self.rst += output

            else:
                raise NotImplementedError()

            if self.cleanup:
                self.cleanup()
        else:
            self.rst = f'.. code-block:: {self.language}\n\n'
            for line in self.lines:
                if not line.endswith('#hide#'):
                    self.rst += f'{self.indent}{self.prompt}{line}\n'

        self.rst += '\n'

        if self.copyto :
            self.copyto.parent.mkdir(parents=True,exist_ok=True)
            mode = 'a+' if self.append else 'w'
            with self.copyto.open(mode=mode) as f:
                for line in self.lines:
                    f.write(line + '\n')



class Table(RstItem):
    """ Table class

    :param list-of-lists rows: a list of rows, each row being a list as well. First row is
        title row.
    """
    def __init__(self
                , rows
                , document=None
                 ):
        super().__init__(document=document)
        self.rows = rows
        self.indent = 4*' '
        self.rstor()
        self.show_progress()

    def rstor(self):
        self.rst = ''
        nrows = len(self.rows)
        ncols = len(self.rows[0])
        for row in self.rows[1:]:
            if len(row) != ncols:
                raise ValueError('all rows must have the same number of columns')
        # Convert rows to str and find out the width of each column
        wcol = ncols*[0]
        for row in self.rows:
            for c,val in enumerate(row):
                sval = str(val)
                row[c] = sval
                w = len(sval)
                wcol[c] = max(w,wcol[c])
        # Insert lines
        self.rows.insert(0, [])
        self.rows.insert(2, [])
        self.rows.append([])
        for c in range(ncols):
            line = wcol[c]*'='
            self.rows[ 0].append(line)
            self.rows[ 2].append(line)
            self.rows[-1].append(line)
        # compile table in rst format:
        for row in self.rows:
            self.rst += '\n' + self.indent
            for c,val in enumerate(row):
                self.rst += val.ljust(wcol[c]+2)

        self.rst += '\n\n'


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
        self.lookahead = 15

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
