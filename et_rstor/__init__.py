# -*- coding: utf-8 -*-
"""
Package et_rstor
================

A package for generating .rst documents with Python commands.

"""

from pathlib import Path
from textwrap import TextWrapper
import subprocess
import shutil

__version__ = "1.0.0"


class RstDocument:

    def __init__(self, name, width=72, headings_numbered_from_level=None, is_default_document=False):
        """Create a RstDocument.

        :param str name: name of the document, used as a filename for writing the document.
        :param int width: used by TextWrapper to convert long strings into lines.
        :param in_range(6) headings_numbered_from_level: heading level from which numbering will be used.
        :param bool is_default_document: if True any RstItem created without specifying a document will
            automatically be added to this RstDocument.
        """
        self.name = name
        self.heading_numbers = 6*[-1]
        self.headings_numbered_from_level = 6 # = no numbering of headings
        
        self.width = width
        self.set_textwrapper()
        if headings_numbered_from_level < 6:
            self.headings_numbered_from_level = headings_numbered_from_level
            for l in range(headings_numbered_from_level,6):
                self.heading_numbers[l] = 0
        self.items = []
        self.verbose = False
        if is_default_document:
            RstItem.default_document = self


    def append(self, item):
        """Append an Rstitem item to this RstDocument."""
        self.items.append(item)

    def set_textwrapper(self, textwrapper=None):
        """Set a TextWrapper object for the RstDocument"""
        if textwrapper is None:
            self.textwrapper = TextWrapper( width=self.width
                                          , replace_whitespace=True
                                          , break_long_words=False
                                          , break_on_hyphens=False
                                          )
        elif isinstance(textwrapper,TextWrapper):
            self.textwrapper = textwrapper
        else:
            raise ValueError('Argument must be a TextWrapper object.')


    def __str__(self):
        if self.verbose:
            print(f'Processing {self.__class__.__name__} {self.name}:')
        result = ''
        for item in self.items:
            if self.verbose:
                item.show_progress()
            result += f"{item}"
        if self.verbose:
            print(f'Processing {self.__class__.__name__} {self.name} done.')
        return result


    def write(self, path='.', ext='.rst'):
        """Write the document to a file.

        :param (Path,str) path: directory to create the file in.
        """

        f = s if filename.endswith(ext) else filename+ext
        p = Path(path) / f
        with p.open(mode='w') as f:
            f.write(str(self))


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


    def __str__(self):
        raise NotImplementedError()


    def show_progress(self):
        print(self.__class__.__name__)

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
    def __init__(self, text, level=0, crosslink='', document=None):
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
            self.document.heading_numbers[level] += 1
            for l in range(level+1,6):
                self.document.heading_numbers[l] = 0
            self.text = ''
            for l in range(self.document.headings_numbered_from_level,level+1):
                self.text += f'{self.document.heading_numbers[l]}.'
            self.text += f" {text}"
        else:
            self.text = text
        self.crosslink = crosslink

    def __str__(self):
        text = ''
        if self.crosslink:
            text += f'.. _{self.crosslink}:\n\n'

        n = len(self.text)
        line = n * self.parms[0]
        if self.parms[1]:
            text += f'{line}\n{self.text}\n{line}\n\n'
        else:
            text += f'{self.text}\n{line}\n\n'
        return text


    def show_progress(self):
        print(self.__class__.__name__, self.text )


####################################################################################################
# Paragraph
####################################################################################################
class Paragraph(RstItem):
    def __init__(self, text, width=72, indent=0, document=None):
        super().__init__(document=document)

        self.text = text
        self.width = width
        self.indent = indent*' '


    def __str__(self):
        lines = self.document.textwrapper.wrap(self.text)
        text = ''
        for line in lines:
            text += f'{self.indent}{line}\n'
        text += '\n'
        return text


####################################################################################################
# Note
####################################################################################################
class Note(RstItem):
    def __init__(self, text, document=None):
        super().__init__(document=document)
        self.paragraphs = listify(text)

    def __str__(self):
        text = '.. note::\n\n'
        for paragraph in self.paragraphs:
            lines = self.document.textwrapper.wrap(paragraph)
            for line in lines:
                text += f'   {line}\n'
            text += '\n'
        return text


####################################################################################################
# Include
####################################################################################################
class Include(RstItem):
    def __init__(self, filename, document=None):
        super().__init__(document=document)
        self.filename = filename

    def __str__(self):
        return f'.. include:: {self.filename}\n\n'


####################################################################################################
# List
####################################################################################################
class List(RstItem):
    def __init__(self, items, numbered=False, document=None):
        """List item, bulleted or numbered"""
        super().__init__(document=document)
        self.items = listify(items)
        self.numbered = numbered

    def __str__(self):
        bullet = '#' if self.numbered else '*'
        text = ''
        for item in self.items:
            lines = self.document.textwrapper.wrap(item)
            text += f'{bullet} {lines[0]}\n'
            for line in lines[1:]:
                text += f'  {line}\n'
            text += '\n'
        return text


####################################################################################################
# CodeBlock
####################################################################################################
class CodeBlock(RstItem):

    def __init__( self, lines
                , language='', execute=False
                , prompt='', indent=4
                , cwd='.', setup=None, cleanup=None
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
        """
        super().__init__(document=document)
        self.lines = listify(lines)
        self.language = language
        self.prompt = prompt
        self.indent = indent*' '
        self.execute = execute
        self.cwd = cwd
        self.setup = setup
        self.cleanup = cleanup

    def __str__(self):
        text = f'.. code-block:: {self.language}\n\n'

        if self.execute:
            if self.setup:
                self.setup()
            for line in self.lines:
                text += f'{self.indent}{self.prompt}{line}\n'
                # execute the command and add its output
                if self.language == 'bash':
                    cmd = line.split(' ')
                    completed_process = subprocess.run( cmd, cwd=self.cwd
                                                      , stdout=subprocess.PIPE
                                                      , stderr=subprocess.STDOUT
                                                      )
                    output = self.indent + completed_process.stdout.decode('utf-8').replace('\n', '\n'+self.indent)
                    text += output+'\n'
                else:
                    raise NotImplementedError()

            if self.cleanup:
                self.cleanup()
        else:
            text = f'.. code-block:: {self.language}\n\n'
            for line in self.lines:
                text += f'{self.indent}{line}\n'

        text += '\n'
        return text


    def show_progress(self):
        if self.execute:
            print(self.__class__.__name__, 'executing ...')
        else:
            print(self.__class__.__name__)


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