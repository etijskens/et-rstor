# -*- coding: utf-8 -*-

"""Tests for et_rstor package."""

from et_rstor import *
from pathlib import Path
import os


def test_rstor0():
    """Tutorial-1."""

    workspace = Path.home() / 'software/dev/workspace/Tutorials'
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True,exist_ok=True)

    doc = RstDocument('Tutorial-1', headings_numbered_from_level=2,is_default_document=True)

    Include( '../HYPERLINKS.rst')

    Heading( 'Getting started with Micc2', level=2, crosslink='TUTORIAL1')

    Note(
        [ "These tutorials focus not just on how to use micc2_. Rather they describe a workflow"
          "for how you might set up a python project and develop it using best practises, with"
          "the help of micc_."
        , "All tutorial sections start with the bare essentials, which should get you"
          "up and running. They are often followed by more detailed subsections that"
          "provide useful background information that is needed for intermediate or"
          "advanced usage. These sections have an explicit *[intermediate]* or "
          "*[advanced]* tag in the title, e.g. :ref:`modules-and-packages` and they are"
          "indented. Background sections can be skipped on first reading, but the user"
          "is encouraged to read them at some point. The tutorials are rather extensive"
          "as they interlaced with many good practices advises."
        ]
    )

    Paragraph(
        "Micc_ wants to provide a practical interface to the many aspects of managing a"
        "Python project: setting up a new project in a standardized way, adding documentation,"
        "version control, publishing the code to PyPI_, building binary extension modules in C++"
        "or Fortran, dependency management, ... For all these aspects there are tools available,"
        "yet I found myself struggling to get everything right and looking up the details each "
        "time I needed them."
        "Micc_ is an attempt to wrap all the details by providing the user with a standardized"
        "yet flexible workflow for managing a Python project. Standardizing is a great way to"
        "increase productivity. For many aspects the tools used by Micc_ are completely hidden"
        "from the user, e.g. project setup, adding components, building binary extensions, ..."
        "For other aspects Micc_ provides just the necessary setup for you to use other tools"
        "as you need them. Learning to use the following tools is certainly beneficial:"
        )

    List(
        ["Git_: for version control. Its use is optional but highly recommended. See "
         ":ref:`TUTORIAL4` for some basic git_ coverage."
        ,"Pytest_: for (unit) testing. Also optional and also highly recommended."
        ]
    )

    Paragraph(
        'The basic commands for these tools are covered in these tutorials.'
    )

    Heading( 'Creating a project with micc2',level=3, crosslink='create-proj')

    Paragraph(
        'Creating a new project with micc2_ is simple:'
    )

    CodeBlock(
        '> micc create path/to/my-first-project'
        , language='bash'
    )

    Paragraph(
        "This creates a new project *my-first-project* in folder ``path/to``. "
        "Note that the directory ``path/to/my-first-project`` must either not exist, "
        "or be empty."
    )
    Paragraph(
        "Typically, you will create a new project in the current working directory, say: "
        "your workspace, so first ``cd`` into it:"
    )
    CodeBlock(
        "cd path/to/workspace"
        , language='bash'
    )

    project_name = 'my-first-project'
    rm_myfirstproject = RemoveDir(workspace, project_name)

    CodeBlock(
        f"micc2 create {project_name} --remote=none"
        , language='bash', execute=True, prompt='> ', cwd=workspace, setup=rm_myfirstproject
    )

    Paragraph(
        "As the output tells, micc2_ has created a new project in directory "
        ":file:`my-first-project` containing a python module :file:`my_first_project.py`."
        "Note that the module name differs a bit from the project name. Dashes are"
        "been replaced with underscores and uppercase with lowercase in order to yield a "
        "`PEP 8 <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_ "
        "compliant module name. If you want your module name to be unrelated to your "
        "project name, check out the :ref:`project-and-module-naming` section."
    )

    Paragraph(
        "Micc2_ also automatically creates a local git_ repository for our project (provided"
        "the ``git`` command is available) and it commits all the project files that it"
        "generated with commit message 'And so this begun...'. The ``--remote=none`` flag "
        "prevents Micc2_ from also creating a remote repository on GitHub_. Without that "
        "flag Micc2_ would have created a public remote repository on GitHub_ and pushed "
        "that first commit. This, of course, requires that we have set up Micc2_ with a "
        "GitHub_ username and a personal access token for it as described in "
        ":ref:`micc2-setup`. You can also request the remote repository to be private by "
        "specifying ``--remote=private``."
    )

    Paragraph(
        "After creating the project, we ``cd`` into the project directory. All Micc2_ "
        "commands detect automatically that they are run from a project directory and "
        "consequently act on the project in the current working directory. E.g.:"
    )

    CodeBlock(
        "> cd my-first-project"
        , language='bash'
    )
    CodeBlock(
        "micc2 info"
        , language='bash', execute=True, prompt='> ', cwd=workspace/project_name
    )

    Paragraph(
        f"As the ``info`` subcommand, shows info on a project, is run inside the "
        f":file:`{project_name}` directory, we get the info on the :file:`{project_name}`"
        f"project."
    )

    Paragraph(
        "To apply a Micc2_ command to a project that is not in the current working directory"
        "see :ref:`micc-project-path`."
    )

    Paragraph(
        "Above we have created a project for a simple Python *module*, that is, the"
        "project directory contains a file ``my_first_project.py`` which represents "
        "the Python module:"
    )

    CodeBlock(
        ["my-first-project          # the project directory"
        ,"└── my_first_project.py   # the Python module, this is where your code goes"
        ]
        , language='bash'
    )

    Paragraph(
        "The module project type above is suited for problems that can be solved with "
        "a single Python file, here :file:`my_first_project.py`. For more complex problems a"
        "*package* structure is more appropriate. To learn more about the use of Python modules"
        "vs packages, check out the :ref:`modules-and-packages` section below."
    )

    Heading( "Modules and packages", level=3, crosslink='modules-and-packages')

    Paragraph(
        "A *Python module* is the simplest Python project we can create. It is meant for rather"
        "small projects that conveniently fit in a single (Python) file. More complex projects"
        "require a *package* structure. They are created by adding the ``--package`` flag on the"
        "command line:"
    )

    CodeBlock(
        "micc create my-package-project --package --remote=none"

    )
    """



    """
    doc.verbose = True
    print('>>>>>>')
    print(doc, end='')
    print('<<<<<<')



    
# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_rstor0

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof