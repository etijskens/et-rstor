# -*- coding: utf-8 -*-

"""Tests for et_rstor package."""

from pathlib import Path
import re
import sysconfig
import sys
if not '.' in sys.path:
    sys.path.insert(0, '.')

from et_rstor import *

def test_re():
    r = re.compile(r"<(((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*)>`_([,.:;!?\"\')}]?|(\.\.\.))\Z")
    for word in ["<https://www.sphinx-doc.org/en/master/>`_."]:
        m = r.match(word)
        for i in range(3):
            print(f"'{m.group(i)}'")
        assert m


def test_TextWrapper():
    tw = TextWrapper(width=40)
    text = "The *MIT license* is a **very liberal** license and the ``default option``. If you’re unsure which " \
           "license to choose, you can use resources such as `GitHub’s Choose a License <https://choosealicense.com>`_!"
    tw.wrap(text)



write = True

def test_Tutorial1():
    """Tutorial-1."""

    workspace = Path.home() / 'software/dev/workspace/Tutorials'
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True,exist_ok=True)

    doc = RstDocument('Tutorial-1', headings_numbered_from_level=2, is_default_document=True)

    Include( '../HYPERLINKS.rst')

    Heading( 'Getting started with Micc2', level=2, crosslink=doc.name)

    Note(
        "These tutorials focus not just on how to use micc2_. Rather they describe a workflow "
        "for how you might set up a python project and develop it using best practises, with "
        "the help of Micc2_. "
    )
    Paragraph(
        "Micc2_ wants to provide a practical interface to the many aspects of managing a "
        "Python project: setting up a new project in a standardized way, adding documentation, "
        "version control, publishing the code to PyPI_, building binary extension modules in C++ "
        "or Fortran, dependency management, ... For all these aspects there are tools available, "
        "yet I found myself struggling to get everything right and looking up the details each "
        "time I needed them. "
        "Micc2_ is an attempt to wrap all the details by providing the user with a standardized "
        "yet flexible workflow for managing a Python project. Standardizing is a great way to "
        "increase productivity. For many aspects the tools used by Micc2_ are completely hidden "
        "from the user, e.g. project setup, adding components, building binary extensions, ... "
        "For other aspects Micc2_ provides just the necessary setup for you to use other tools "
        "as you need them. Learning to use the following tools is certainly beneficial:"
        )
    List(
        [ "Git_: for version control. Its use is optional but highly recommended. See "
          ":ref:`TUTORIAL4` for some basic git_ coverage."
        , "Pytest_: for (unit) testing. Also optional and also highly recommended."
        ]
    )
    Paragraph(
        'The basic commands for these tools are covered in these tutorials.'
    )

    Heading( 'Creating a project with micc2',level=3, crosslink='create-proj')

    Paragraph(
        'Creating a new project with micc2_ is simple:'
    )

    project_name = 'my-first-project'
    package_name = package_name_of(project_name)

    CodeBlock(
        f'> micc create path/to/{project_name}'
        , language='bash'
    )
    Paragraph(
        f"This creates a new project *{project_name}* in folder ``path/to``. "
        f"Note that the directory ``path/to/{project_name}`` must either not exist, "
        f"or be empty."
    )
    Paragraph(
        "Typically, you will create a new project in the current working directory, say: "
        "your workspace, so first ``cd`` into it:"
    )
    CodeBlock(
        "cd path/to/workspace"
        , language='bash'
    )
    CodeBlock(
        f"micc2 create {project_name} --remote=none"
        , language='bash', execute=True, cwd=workspace
    )
    Paragraph(
        f"As the output tells, micc2_ has created a new project in directory "
        f":file:`{project_name}` containing a python module :file:`{package_name}.py`. "
        f"Note that the module name differs a bit from the project name. Dashes are "
        f"been replaced with underscores and uppercase with lowercase in order to yield a "
        f"`PEP 8 <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_ "
        f"compliant module name. If you want your module name to be unrelated to your "
        f"project name, check out the :ref:`project-and-module-naming` section."
    )
    Paragraph(
        "Micc2_ also automatically creates a local git_ repository for our project "
        "(provided the ``git`` command is available) and it commits all the project files "
        "that it generated with commit message 'And so this begun...'. The ``--remote=none`` "
        "flag prevents Micc2_ from also creating a remote repository on GitHub_. Without that "
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
        f"> cd {project_name}"
        , language='bash'
    )
    CodeBlock(
        "micc2 info"
        , language='bash', execute=True, cwd=workspace/project_name
    )
    Paragraph(
        f"As the ``info`` subcommand, shows info on a project, is running inside the "
        f":file:`{project_name}` directory, we get the info on the :file:`{project_name}` "
        f"project."
    )
    Paragraph(
        "To apply a Micc2_ command to a project that is not in the current working directory "
        "see :ref:`micc-project-path`."
    )
    Note(
        "Micc2 has a built-in help function: ``micc2 --help`` shows the global options, "
        "which appear in front of the subcommand, and lists the subcommands, and "
        "``micc2 subcommand --help``, prints detailed help for a subcommand."
    )
    Paragraph(
        f"Above we have created a project for a simple Python *module*, that is, the "
        f"project directory contains a file :file:`{package_name}.py` which represents "
        f"the Python module:"
    )
    CodeBlock(
        [f"{project_name}          # the project directory"
        ,f"└── {package_name}.py   # the Python module, this is where your code goes"
        ]
        , language='bash'
    )
    Paragraph(
        "The module project type above is suited for problems that can be solved with "
        "a single Python file, here :file:`my_first_project.py`. For more complex problems "
        "a *package* structure is more appropriate. To learn more about the use of Python "
        "modules vs packages, check out the :ref:`modules-and-packages` section below."
    )

    Heading( "Modules and packages", level=4, crosslink='modules-and-packages')

    Paragraph(
        "A *Python module* is the simplest Python project we can create. It is meant for rather "
        "small projects that conveniently fit in a single (Python) file. More complex projects "
        "require a *package* structure. You create them by adding the ``--package`` flag on the "
        "command line:"
    )

    project_name = 'my-package-project'
    package_name = package_name_of(project_name)

    CodeBlock(
        f"micc2 create {project_name} --package --remote=none"
        , language='bash', execute=True, cwd=workspace
    )
    Paragraph(
        f"The output shows a different file structure of the project than for a module project "
        f"we created earlier. Instead of a file :file:`{package_name}.py` there is a now a "
        f"directory :file:`{package_name}`, containing a :file:`__init__.py` file:"
    )
    CodeBlock(
        f"{project_name}          # the project directory"
        f"└── {package_name}      # the package directory"
        f"    └── __init__.py       # the file where your code goes"
        , language='bash'
    )
    Paragraph(
        "The :file:`__init__.py` in the package directory is the equivalent of the "
        ":file:`my_first_project.py` in our module structure project."
    )
    Paragraph(
        "With Micc2_ you can add additional components to your package:"
    )
    List(
        [ "Python sub-modules and sub-packages,"
        , "Command line interfaces (CLIs),"
        , "Binary extension modules written in C++ or Fortran."
        ]
    )
    Paragraph(
        "The distinction between a module structure and a package structure is also important "
        "when you publish the module. When installing a Python package with a module structure, "
        "The distinction between a module structure and a package structure is also important "
        "only the module file :file:`my_first_project.py` will be installed, while with the "
        "package structure the entire directory :file:`my_package_project` will be installed. "
        "This may also include other files needed by your project."
    )
    Paragraph(
        "If you created a project with a module structure and discover over time that its "
        "complexity has grown beyond the limits of a single module file, you can easily "
        "convert it to a *package* structure project at any time running (in the project "
        "directory):"
    )
    CodeBlock(
        "micc2 convert-to-package"
        , language='bash', execute=True, cwd=workspace/'my-first-project'
    )
    Paragraph(
        "Because we do not want to replace existing files inadvertently, this command will "
        "always fail, and tell you which files the command would need to overwrite. "
        "Check the list of file for files that you might have changed, and if there aren't "
        "any, rerun the command with the ``--overwrite`` flag:"
    )
    CodeBlock(
        "micc2 convert-to-package --overwrite"
        , language='bash', execute=True, cwd=workspace / 'my-first-project'
    )
    Paragraph(
        "If there are some files in the list you did change (this is rarely the case), "
        "rerun the command with the ``--backup`` flag instead of the ``--overwrite`` "
        "flag, to make a backup of the listed files, and manually copy the changes "
        "from the :file:`.bak` files to the new files."
    )
    Paragraph(
        "Now run the ``info`` command to verify that the project has indeed a package "
        "structure:"
    )
    CodeBlock(
        "micc2 info"
        , language='bash', execute=True, cwd=workspace / 'my-first-project'
    )

    Heading("What's in a name", level=4, crosslink='project-and-module-naming')

    Paragraph(
        "The name you choose for your project is not without consequences. Ideally, "
        "a project name is:"
    )
    List(
        [ "descriptive,"
        , "unique,"
        , "short."
        ]
    )
    Paragraph(
        "Although one might think of even more requirements, such as being easy to type, "
        "satisfying these three is already hard enough. "
        "E.g. the name :file:`my_nifty_module` may possibly be unique, but it is neither "
        "descriptive, neither short. On the other hand, :file:`dot_product` is descriptive, "
        "reasonably short, but probably not unique. Even :file:`my_dot_product` is probably "
        "not unique, and, in addition, confusing to any user that might want to adopt *your* "
        ":file:`my_dot_product`. A unique name - or at least a name that has not been taken "
        "before - becomes really important when you want to publish your code for others "
        "to use it (see :ref:`Tutorial-5` for details). The standard place to publish Python "
        "code is the `Python Package Index <https://pypi.org>`_, where you find hundreds of "
        "thousands of projects, many of which are really interesting and of high quality. Even "
        "if there are only a few colleagues that you want to share your code with, you make "
        "their life (as well as yours) easier when you publish your :file:`my_nifty_module` "
        " at PyPI_. To install your :file:`my_nifty_module` they will only need to type:"
    )
    CodeBlock(
        'python -m pip install my_nifty_module'
        , language='bash'
    )
    Paragraph(
        "The name *my_nifty_module* is not used so far, but nevertheless we recommend to "
        "choose a better name. "
    )
    Paragraph(
        "If you intend to publish your code on PyPI_, we recommend that you create your "
        "project with the ``--publish`` flag. Micc2_ then checks if the name you want "
        "to use for your project is still available on PyPI_. If not, it refuses to create "
        "the project and asks you to use another name for your project:"
    )
    CodeBlock(
        "micc2 create oops --publish"
        , language='bash', execute=True, cwd=workspace, error_ok=True
    )
    Paragraph(
        "As there are indeed hundreds of thousands of Python packages published on PyPI_, "
        "finding a good name has become quite hard. Personally, I often use a simple and "
        "short descriptive name, prefixed by my initials, :file:`et-`, which usually makes "
        "the name unique. E.g :file:`et-oops` does not exist. This has the additional "
        "advantage that all my published modules are grouped in the alphabetic PyPI_ listing."
    )
    Paragraph(
        "Another point of attention is that although in principle project names can be anything "
        "supported by your OS file system, as they are just the name of a directory, Micc2_ "
        "insists that module and package names comply with the "
        "`PEP8 module naming rules <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_. "
        "Micc2_ derives the package (or module) name from the project name as follows:"
    )
    List(
        ["capitals are replaced by lower-case"
        ,"hyphens ``'-'`` are replaced by underscores ``'_'``"]
    )
    Paragraph(
        "If the resulting module name is not PEP8 compliant, you get an informative error "
        "message:"
    )
    CodeBlock(
        "micc create 1proj"
        , language='bash', execute=True, cwd=workspace, error_ok=True
    )
    Paragraph(
        "The last line indicates that you can specify an explicit module name, unrelated to "
        "the project name. In that case PEP8 compliance is not checked. The responsability "
        "is then all yours."
    )

    Heading("First steps in project management using Micc2", level=3, crosslink='first-steps')

    Heading("The project path in Micc2", level=4, crosslink='micc-project-path')

    Paragraph(
        "All micc2_ commands accept the global ``--project-path=<path>`` parameter. "
        "Global parameters appear *before* the subcommand name. E.g. the command:"
    )
    CodeBlock(
        "micc2 --project-path path/to/my_project info"
        , language='bash'
    )
    Paragraph(
        "will print the info on the project located at :file:`path/to/my_project`. "
        "This can conveniently be abbreviated as:"
    )
    CodeBlock(
        "micc2 -p path/to/my_project info"
        , language='bash'
    )
    Paragraph(
        "Even the ``create`` command accepts the global ``--project-path=<path>`` parameter:"
    )
    CodeBlock(
        "micc2 -p path/to/my_project create"
        , language='bash'
    )
    Paragraph(
        "will attempt to create project :file:`my_project` at the specified location. "
        "The command is equivalent to:"
    )
    CodeBlock(
        "micc2 create path/to/my_project"
        , language='bash'
    )
    Paragraph(
        "The default value for the project path is the current working directory. "
        "Micc2_ commands without an explicitly specified project path will act on "
        "the project in the current working directory."
    )

    Heading("Virtual environments", level=4, crosslink='virtual-environments')

    Paragraph(
        "Virtual environments enable you to set up a Python environment that is isolated "
        "from the installed Python on your system and from other virtual environments. "
        "In this way you can easily cope with varying dependencies between your Python "
        "projects."
    )
    Paragraph(
        "For a detailed introduction to virtual environments see "
        "`Python Virtual Environments: A Primer <https://realpython.com/python-virtual-environments-a-primer/>`_."
    )
    Paragraph(
        "When you are developing or using several Python projects simultaneously, "
        "it can  become difficult for a single Python environment to satisfy all "
        "the dependency requirements of these projects. Dependency conflicts can "
        "easily arise. Python promotes and facilitates code reuse and as a consequence "
        "Python tools typically depend on tens to hundreds of other modules. If tool-A "
        "and tool-B both need module-C, but each requires a different version of it, "
        "there is a conflict because it is impossible to install two different versions "
        "of the same module in a Python environment. The  solution that the Python "
        "community has come up with for this problem is the construction of "
        "*virtual environments*, which isolates the dependencies of a single project "
        "in a single environment."
    )
    Paragraph(
        "For this reason it is recommended to create a virtual environment for every "
        "project you start. Here is how that goes:"
    )

    Heading('Creating virtual environments', level=5, crosslink='venv')

    CodeBlock(
        "python -m venv .venv-my-first-project"
        , language='bash', execute=True, cwd=workspace/'my-first-project'
    )
    Paragraph(
        "This creates a directory :file:`.venv-my-first-project` representing the virtual "
        "environment. The Python version of this virtual environment is the Python version "
        "that was used to create it. Use the ``tree`` command to get an overview of its "
        "directory structure:"
    )
    CodeBlock(
        "tree .venv-my-first-project -L 4"
        , language='bash', execute=True, cwd=workspace/'my-first-project'
    )
    Paragraph(
        "As you can see there is a :file:`bin`, :file:`include`, and a :file:`lib` directory. "
        "In the :file:`bin` directory you find installed commands, like :file:`activate`, "
        ":file:`pip`, and the :file:`python` of the virtual environment. The :file:`lib` "
        "directory contains the installed site-packages, and the :file:`include` directory "
        "containes include files of installed site-packages for use with C, C++ or Fortran."
    )
    Paragraph(
        "If the Python version you used to create the virtual environment has pre-installed "
        "packages you can make them available in your virtual environment by adding the "
        "``--system-site-packages`` flag:"
    )
    CodeBlock(
        "python -m venv .venv-my-first-project --system-site-packages"
        , language='bash'
    )
    Paragraph(
        "This is especially useful in HPC environments, where the pre-installed packages "
        "typically have a better computational efficiency."
    )
    Paragraph(
        "As to where you create these virtual environments there are two common approaches. "
        "One is to create a :file:`venvs` directory where you put all your virtual "
        "environments. This is practical if you have virtual environments which are common "
        "to several projects. The other one is to have one virtual environment for each "
        "project and locate it in the project directory. "
        "Note that if you have several Python versions on your system you may also create "
        "several virtual environments with different Python versions for a project."
    )
    Paragraph(
        "In order to use a virtual environment, you must activate it:"
    )
    CodeBlock(
        [ "> . .venv-my-first-project/bin/activate"
        , "(.venv-my-first-project) >"
        ]
        , language='bash', prompt=''
    )
    Paragraph(
        "Note how the prompt has changed as to indicate that the virtual environment is active, "
        "and that current Python is now that of the virtual environment, and the only Python "
        "packages available are the ones installed in it, as well as the system site packages "
        "of the corresponding Python if the virtual environmnet was created with the "
        "``--system-site-packages`` flag. To deactivate the virtual environment, run:"
    )
    CodeBlock(
        [ "(.venv-my-first-project) > deactivate"
        , "> "
        ]
        , language='bash', prompt=''
    )
    Paragraph(
        "The prompt has turned back to normal."
    )
    Paragraph(
        "So far, the virtual environment is pretty much empty (except for the system site "
        "packages if if was created with the ``--system-site-packages`` flag). We must install "
        "the packages that our project needs. Pip_ does the trick:"
    )
    CodeBlock(
        "python -m pip install some-needed-package"
        , language='bash'
    )
    Paragraph(
        "We must also install the project itself, if it is to be used in the virtual environment. "
        "If the project is not under development, we can just run ``pip install``. Otherwise, "
        "we want the code changes that we make while developing to be instantaneously visible in "
        "the virtual environment. Pip_ can do *editable installs*, but only for packages which "
        "provide a :file:`setup.py` file. Micc2_ does not provide :file:`setup.py` files for its "
        "projects, but it has a simple workaround for editable installs. First ``cd`` "
        "into your project directory and activate its virtual environment, then run the "
        ":file:`install-e.py` script:"
    )
    CodeBlock(
        [ "> cd path/to/my-first-project"
        , "> source .venv-my-first-project/bin/activate"
        , "(.venv-my-first-project)> python ~/.micc2/scripts/install-e.py"
        , "..."
        , "Editable install of my-first-project is ready."
        ]
        , language='bash', prompt=''
    )
    Paragraph(
        "If something is wrong with a virtual environment, you can simply delete it:"
    )
    CodeBlock(
        "rm -rf .venv-my-first-project"
        , language='bash'
    )
    Paragraph(
        "and recreate it."
    )

    Heading("Modules and scripts", level=4, crosslink='modules-and-scripts')

    Paragraph(
        "A Python script is a piece of Python code that performs a certain task. "
        "A Python module, on the other hand, is a piece of Python code that provides "
        "a client code, such as a script, with useful Python classes, functions, "
        "objects, and so on, to facilitate the script's task. To that end client code "
        "must import the module."
    )
    Paragraph(
        "Python has a mechanism that allows a Python file to behave as both as a "
        "script and as module. Consider this Python file :file:`my_first_project.py`. "
        "as it was created by Micc2_ in the first place. "
        "Note that Micc2_ always creates project files containing fully functional "
        "examples to demonstrate how things are supposed to be done."
    )
    CodeBlock(
        [ '# -*- coding: utf-8 -*-'
        , '"""'
        , 'Package my_first_project'
        , '========================'
        , ''
        , 'A hello world example.'
        , '"""'
        , ''
        , '__version__ = "0.0.0"'
        , ''
        , 'def hello(who="world"):'
        , '    """A "Hello world" method.'
        , ''
        , '    :param str who: whom to say hello to'
        , '    :returns: a string'
        , '    """'
        , '    result = f"Hello {who}!"'
        , '    return result'
        # , 'if __name__ == "__main__":'
        # , '    say_hello("students")'
        ]
        , language='python'
    )
    Paragraph(
        "The module file starts with a file doc-string that describes what the file "
        "about and a ``__version__`` definition and then goes on defining a simple "
        ":file:`hello` method. A client script :file:`script.py` can import the "
        ":file:`my_first_project.py` module to use its :file:`hello` method:"
    )
    CodeBlock(
        [ '# file script.py'
        , 'import my_first_project'
        , 'print(my_first_project.hello("dear students"))'
        ]
        , language='python'
    )
    Paragraph(
        "When executed, this results in printing ``Hello dear students!``"
    )
    CodeBlock(
        [ '> python script.py'
        , 'Hello dear students!'
        ]
        , language='bash', prompt=''
    )
    Paragraph(
        "Python has an interesting idiom for allowing a module also to behave as a "
        "script. Python defines a ``__name__`` variable for each file it interprets. "
        "When the file is executed as a script, as in ``python script.py``, the "
        "``__name__`` variable is set to ``__main__`` and when the file is imported "
        "the __name__`` variable is set to the module name. By testing the value of "
        "the __name__`` variable we can selectively execute statements depending on "
        "whether a Python file is imported or executed as a script. E.g. below we "
        "we added some tests for the ``hello`` method:"
    )
    CodeBlock(
        [ '#...'
        , 'def hello(who="world"):'
        , '    """A "Hello world" method.'
        , ''
        , '    :param str who: whom to say hello to'
        , '    :returns: a string'
        , '    """'
        , '    result = f"Hello {who}!"'
        , '    return result'
        , ''
        , 'if __name__ == "__main__":'
        , '    assert hello() == "Hello world!'
        , '    assert hello("students") == "Hello students!'
        ]
        , language='python'
    )

    Paragraph(
        "If we now execute :file:`my_first_project.py` the ``if __name__ == \"__main__\":`` " 
        "clause evaluates to ``True`` and the two assertions are executed - successfully. "
    )
    Paragraph(
        "So, adding a ``if __name__ == \"__main__\":`` clause at the end of a module "
        "allows it to behave as a script. This is Python idiom comes in handy for quick "
        "testing or debugging a module. Running the file as a script will execute the test "
        "and raise an AssertionError if it fails. If so, we can run it in debug mode to see "
        "what goes wrong."
    )
    Paragraph(
        "While this is a very productive way of testing, it is a bit on the *quick and dirty* "
        "side. As the module code and the tests become more involved, the module file will soon "
        "become cluttered with test code and a more scalable way to organise your tests is needed. "
        "Micc2_ has already taken care of this."
    )

    Heading('Testing your code', level=4, crosslink='testing-your-code')

    Paragraph(
        "`Test driven development <https://en.wikipedia.org/wiki/Test-driven_development>`_ is a "
        "software development process that relies on the repetition of a very short development cycle: "
        "requirements are turned into very specific test cases, then the code is improved so that the "
        "tests pass. This is opposed to software development that allows code to be added that is not "
        "proven to meet requirements. The advantage of this is clear: the shorter the cycle, the "
        "smaller the code that is to be searched for bugs. This allows you to produce correct code "
        "faster, and in case you are a beginner, also speeds your learning of Python. Please check "
        "Ned Batchelder's very good introduction to "
        "`testing with pytest <https://nedbatchelder.com/text/test3.html>`_."
    )
    Paragraph(
        "When Micc2_ created project :file:`my-first-project`, it not only added a ``hello`` method "
        "to the module file, it also created a test script for it in the :file:`tests` directory of "
        "the project directory. The testS for the :file:`my_first_project` module is in file "
        ":file:`tests/test_my_first_project.py`. Let's take a look at the relevant section:"
    )
    CodeBlock(
        [ '# -*- coding: utf-8 -*-'
        , '"""Tests for my_first_project package."""'
        , ''
        , 'import my_first_project'
        , ''
        , 'def test_hello_noargs():'
        , '    """Test for my_first_project.hello()."""'
        , '    s = my_first_project.hello()'
        , '    assert s=="Hello world!"'
        , ''
        , 'def test_hello_me():'
        , '    """Test for my_first_project.hello(\'me\')."""'
        , '    s = my_first_project.hello(\'me\')'
        , '    assert s=="Hello me!"'
        ]
        , language='python'
    )
    Paragraph(
        "The :file:`tests/test_my_first_project.py` file contains two tests. One for "
        "testing the ``hello`` method with a default argument, and one for testing it "
        "with argument ``'me'``. Tests like this are very useful to ensure that during "
        "development the changes to your code do not break things. There are many "
        "Python tools for unit testing and test driven development. Here, we use "
        "Pytest_. The tests are automatically found and executed by "
        "running ``pytest`` in the project directory:"
    )
    CodeBlock(
        "pytest tests -v"
        , language='bash', execute=True, cwd=workspace/'my-first-project'
    )
    Paragraph(
        "Specifying the :file:`tests` directory ensures that Pytest_ looks for tests "
        "only in the :file:`tests` directory. This is usually not necessary, but it avoids "
        "that ``pytest``'s test discovery algorithm discovers test which are not meant "
        "to be. The ``-v`` flag increases ``pytest``'s verbosity. The output shows that "
        "``pytest`` discovered the two tests put in place by Micc2_ and that they both "
        "passed."
    )
    Note(
        "Pytest_ looks for test methods in all :file:`test_*.py` or :file:`*_test.py` "
        "files in the current directory and accepts (1) ``test`` prefixed methods outside "
        "classes and (2) ``test`` prefixed methods inside ``Test`` prefixed classes as test"
        "methods to be executed."
    )
    Paragraph(
        "If a test would fail you get a detailed report to help you find the cause of the"
        "error and fix it."
    )
    Note(
        "A failing test not necessarily implies that your module is faulty. Test code is "
        "also code and therefore can contain errors, too.  It is not uncommon that a failing "
        "test is caused by a buggy test rather than a buggy method or class."
    )

    Heading('Debugging test code', level=5, crosslink='debug-test-code')

    Paragraph(
        "When the report provided by Pytest_ does not yield an obvious clue on the "
        "cause of the failing test, you must use debugging and execute the failing "
        "test step by step to find out what is going wrong where. From the viewpoint "
        "of Pytest_, the files in the :file:`tests` directory are modules. Pytest_ "
        "imports them and collects the test methods, and executes them. Micc2_ also "
        "makes every test module executable using the "
        "Python ``if __name__ == \"__main__\":`` idiom described above. At the end "
        "of every test file you will find some extra code:"
    )
    CodeBlock(
        [ 'if __name__ == "__main__":                                   # 0'
        , '    the_test_you_want_to_debug = test_hello_noargs           # 1'
        , '                                                             # 2'
        , '    print("__main__ running", the_test_you_want_to_debug)    # 3'
        , '    the_test_you_want_to_debug()                             # 4'
        , '    print(\'-*# finished #*-\')                              # 5'
        ]
        , language='python'
    )
    Paragraph(
        "On line ``# 1``, the name of the test method we want to debug is aliased as "
        "``the_test_you_want_to_debug``, c.q. ``test_hello_noargs``. The variable thus "
        "becomes an alias for the test method. Line ``# 3`` prints a message with the "
        "name of the test method being debugged to assure you that you are running the "
        "test you want. Line ``# 4`` calls the test method, and, finally, line ``# 5`` "
        "prints a message just before quitting, to assure you that the code went well "
        "until the end."
    )
    CodeBlock(
        [ '(.venv-my-first-project) > python tests/test_my_first_project.py'
        , '__main__ running <function test_hello_noargs at 0x1037337a0>     # output of line # 3'
        , '-*# finished #*-                                                 # output of line # 5'
        ]
        , language='python'
    )
    Paragraph(
        'Obviously, you can run this script in a debugger to see what goes wrong where.'
    )

    Heading('Generating documentation', level=4, crosslink='generate-doc')

    Note(
        "It is not recommended to build documentation in HPC environments."
    )
    Paragraph(
        'Documentation is generated almost completely automatically from the source '
        'code using Sphinx_. It is extracted from the doc-strings in your code. '
        'Doc-strings are the text between triple double quote pairs in the examples above, '
        'e.g. ``"""This is a doc-string."""``. Important doc-strings are:'
    )
    List(
        [ '*module* doc-strings: at the beginning of the module. Provides an overview of '
          'what the module is for.'
        , '*class* doc-strings: right after the ``class`` statement: explains what the class '
          'is for. Usually, the doc-string of the __init__ method is put here as well, as '
          '*dunder* methods (starting and ending with a double underscore) are not '
          'automatically considered by Sphinx_.'
        , '*method* doc-strings: right after a ``def`` statement, class methods should also'
          'get a doc-string.'
        ]
    )
    Paragraph(
        "According to `pep-0287 <https://www.python.org/dev/peps/pep-0287/>`_ the recommended "
        "format for Python doc-strings is "
        "`restructuredText <http://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_."
        "E.g. a typical method doc-string looks like this:"
    )
    CodeBlock(
        [ "def hello_world(who='world'):"
        , '    """Short (one line) description of the hello_world method.'
        , ''
        , '    A detailed description of the hello_world method.'
        , '    blablabla...'
        , ''
        , '    :param str who: an explanation of the who parameter. You should'
        , '        mention e.g. its default value.'
        , '    :returns: a description of what hello_world returns (if relevant).'
        , '    :raises: which exceptions are raised under what conditions.'
        , '    """'
        , '    # here goes your code ...'
        ]
        , language='python'
    )
    Paragraph(
        "Here, you can find some more "
        "`examples <http://queirozf.com/entries/python-docstrings-reference-examples>`_."
    )
    Paragraph(
        "Thus, if you take good care writing doc-strings, helpful documentation "
        "follows automatically."
    )
    Paragraph(
        "Micc2_ sets up al the necessary components for documentation generation in "
        "the :file:`docs` directory. To generate documentation in html format, run:"
    )
    CodeBlock(
        "micc2 doc", language='bash', prompt='(.venv-my-first-project) > '
    )
    Paragraph(
        "This will generate documentation in html format in directory "
        ":file:`et-dot/docs/_build/html`. The default html theme for this is "
        "sphinx_rtd_theme_. To view the documentation open the file "
        ":file:`et-dot/docs/_build/html/index.html` in your favorite browser . "
        "Other formats than html are available, but your might have to install "
        "addition packages. To list all available documentation formats run:"
    )
    CodeBlock(
        [ "micc2 doc help"], language='bash'
    )
    Paragraph(
        "The boilerplate code for documentation generation is in the :file:`docs` directory, "
        "just as if it were generated manually using the ``sphinx-quickstart`` command. "
        "Modifying those files is not recommended, and only rarely needed. Then there are "
        "a number of :file:`.rst` files in the project directory with capitalized names:"
    )
    List(
        [ ':file:`README.rst` is assumed to contain an overview of the project. This file '
          'has some boiler plate text, but must essentially be maintained by the authors '
          'of the project.'
        , ':file:`AUTHORS.rst` lists the contributors to the project.'
        , ':file:`CHANGELOG.rst` is supposed to describe the changes that were made '
          'to the code from version to version. This file must entirely be maintained by'
          'by the authors of the project.'
        , ':file:`API.rst` describes the classes and methods of the project in detail. This '
          'file is automatically updated when new components are added through Micc2_'
          'commands.'
        , ':file:`APPS.rst` describes command line interfaces or apps added to your project. '
          'Just as :file:`API.rst` it is automatically updated when new CLIs are added through '
          'Micc2_ commands. For CLIs the documentation is extracted from the ``help`` parameters '
          'of the command options with the help of Sphinx_click_.'
        ]
    )
    Note(
        "The :file:`.rst` extenstion stands for reStructuredText_. "
        "It is a simple and concise approach to text formatting. See "
        "`RestructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ "
        "for an overview."
    )

    Heading('Version control', level=4, crosslink='version-control')

    Paragraph(
        "Version control is extremely important for any software project "
        "with a lifetime of more a day.  Micc2_ facilitates version control by "
        "automatically creating a local git_ repository in your project directory. "
        "If you do not want to use it, you may ignore it or even delete it. If you "
        "have setup Micc2_ correctly, it can even create remote Github_ repositories "
        "for your project, public as well as private."
    )
    Paragraph(
        "Git_ is a version control system (VCS) that solves many practical problems related "
        "to the process software development, independent of whether your are the only "
        "developer, or whether there is an entire team working on it from different places "
        "in the world. You find more information about how Micc2_ cooperates with Git_ "
        "in :ref:`Tutorial-4`."
    )

    Heading('Miscellaneous', level=3, crosslink='miscellaneous')

    Heading('License', level=4, crosslink='license')

    Paragraph(
        "When you set up Micc2 you can select the default license for your Micc2_ projects. "
        "You can choose between:"
    )
    List(
        [ 'MIT license'
        , 'BSD license'
        , 'ISC license'
        , 'Apache Software License 2.0'
        , 'GNU General Public License v3'
        , 'Not open source'
        ]
    )
    Paragraph(
        "If you’re unsure which license to choose, you can use resources such as "
        "`GitHub’s Choose a License <https://choosealicense.com>`_. "
        "You can always overwrite the default chosen when you create a project. "
        "The first characters suffice to select the license:"
    )
    CodeBlock(
        "micc2 --software-license=BSD create"
    )
    Paragraph(
        "The project directory will contain a :file:`LICENCE` file, a plain text file "
        "describing the license applicable to your project."
    )

    Heading('The pyproject.toml file', level=4, crosslink='pyproject-toml')

    Paragraph(
        "Micc2_ maintains a :file:`pyproject.toml` file in the project directory. "
        "This is the modern way to describe the build system requirements of a project "
        "(see `PEP 518 <https://www.python.org/dev/peps/pep-0518/>`_ ). Although this "
        "file's content is generated automatically some understanding of it is useful "
        "(checkout https://poetry.eustace.io/docs/pyproject/). "
    )
    Paragraph(
        "In Micc2_'s predecessor, Micc_, Poetry_ was used extensively for creating "
        "virtual environments and managing a project's dependencies. However, at the "
        "time of writing, Poetry_ still fails to create virtual environments which honor"
        "the ``--system-site-packages``. This causes serious problems on HPC clusters, and "
        "consequently, we do not recommend the use of poetry_ when your projects have to "
        "run on HPC clusters. As long as this issue remains, we recommend to add a project's "
        "dependencies manually in the :file:`pyproject.toml` file, so that when someone "
        "would install your project with Pip_, its dependendies are installed with it. "
        "Poetry_ remains indeed very useful for publishing your project to PyPI_ from your "
        "desktop or laptop. "
    )
    Paragraph(
        "The :file:`pyproject.toml` file is rather human-readable. Most entries are trivial. "
        "There is a section for dependencies ``[tool.poetry.dependencies]``, development "
        "dependencies ``[tool.poetry.dev-dependencies]``. You can maintain these manually. "
        "There is also a section for CLIs ``[tool.poetry.scripts]`` which is updated "
        "automatically whenever you add a CLI through Micc2_. "
    )
    CodeBlock(
        [ '> cat pyproject.toml'
        , ''
        , '[tool.poetry]'
        , 'name = "my-first-project"'
        , 'version = "0.0.0"'
        , 'description = "My first micc2 project"'
        , 'authors = ["John Doe <john.doe@example.com>"]'
        , 'license = "MIT"'
        , ''
        , 'readme = \'Readme.rst\''
        , ''
        , 'repository = "https://github.com/jdoe/my-first-project"'
        , 'homepage = "https://github.com/jdoe/my-first-project"'
        , ''
        , '[tool.poetry.dependencies]'
        , 'python = "^3.7"'
        , ''
        , '[tool.poetry.dev-dependencies]'
        , ''
        , '[tool.poetry.scripts]'
        , ''
        , '[build-system]'
        , 'requires = ["poetry>=0.12"]'
        , 'build-backend = "poetry.masonry.api"'
        ]
        , language='bash', prompt=''
    )
    if write:
        doc.write(Path.home()/'workspace/et-micc2/tutorials/')
    else:
        print('>>>>>>')
        print(doc, end='')
        print('<<<<<<')


def test_Tutorial2():
    """Tutorial-2."""

    workspace = Path.home() / 'software/dev/workspace/Tutorials'
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    doc = RstDocument('Tutorial-2', headings_numbered_from_level=2, is_default_document=True)
    doc.heading_numbers[2] += 1

    Include('../HYPERLINKS.rst')

    Heading('A first real project',level=2, crosslink='tutorial-2')

    Paragraph(
        "Let's start with a simple problem: a Python module that computes the "
        "`scalar product of two arrays <https://en.wikipedia.org/wiki/Dot_product>`_, "
        "generally referred to as the *dot product*. Admittedly, this not a very "
        "rewarding goal, as there are already many Python packages, e.g. Numpy_, "
        "that solve this problem in an elegant and efficient way. However, because "
        "the dot product is such a simple concept in linear algebra, it allows us to "
        "illustrate the usefulness of Python as a language for HPC, as well as the "
        "capabilities of Micc2_."
    )
    Paragraph(
        "First, we set up a new project for this *dot* project, with the name "
        ":file:`ET-dot`, ``ET`` being my initials (check out :ref:`project-and-module-naming`). "
        # "Not knowing beforehand how involved this project will become, "
        # "we create a simple *module* project without a remote Github_ repository:"
    )
    project_name = 'ET-dot'
    project_path = workspace / project_name
    CodeBlock(
        f'micc2 create {project_name} --package --remote=none'
        , language='bash', execute=True, cwd=workspace
    )
    #--------------------------------------------------------------------------------
    # We want to be able use the packagee we create in this tutorial. Apparently,
    # Python cannot reload the module correctly after it changes its structure from
    # module to package. So, this is the true reason why we need to create a
    # package from the beginning: otherwise we would not be able to execute the
    # et_dot's code inside the tutorial.
    #--------------------------------------------------------------------------------
    Paragraph(
        "We already create a package project, rather than the default module project, "
        "just to avoid having to ``micc2 convert-to-package`` later, and to be prepared "
        "for having to add other components (See the :ref:`modules-and-packages` section"
        "for details on the difference between projects with a module structure and a "
        "package structure)."
    )
    Paragraph(
        "We ``cd`` into the project directory, so Micc2_ knows is as the current project."
    )
    CodeBlock(
        'cd ET-dot'
        , language='bash'
    )
    Paragraph(
        "Now, open module file :file:`et_dot.py` in your favourite editor and start coding "
        "a dot product method as below. The example code created by Micc2_ can be removed."
    )
    CodeBlock(
        [ '# -*- coding: utf-8 -*-'
        , '"""'
        , 'Package et_dot'
        , '=============='
        , 'Python module for computing the dot product of two arrays.'
        , '"""'
        , '__version__ = "0.0.0"'
        , ''
        , 'def dot(a,b):'
        , '    """Compute the dot product of *a* and *b*.'
        , ''
        , '    :param a: a 1D array.'
        , '    :param b: a 1D array of the same length as *a*.'
        , '    :returns: the dot product of *a* and *b*.'
        , '    :raises: ValueError if ``len(a)!=len(b)``.'
        , '    """'
        , '    n = len(a)'
        , '    if len(b)!=n:'
        , '        raise ValueError("dot(a,b) requires len(a)==len(b).")'
        , '    result = 0'
        , '    for i in range(n):'
        , '        result += a[i]*b[i]'
        , '    return result'
        ]
        , language='python', copyto=project_path/'et_dot/__init__.py'
    )
    Paragraph(
        "We defined a :py:meth:`dot` method with an informative doc-string that describes "
        "the parameters, the return value and the kind of exceptions it may raise. If "
        "you like, you can add a ``if __name__ == '__main__':`` clause for quick-and-dirty "
        "testing or debugging (see :ref:`modules-and-scripts`). It is a good idea to commit "
        "this implementation to the local git repository:"
    )
    CodeBlock(
        "git commit -a -m 'implemented dot()'"
        , language='bash', execute=True, cwd=project_path
    )
    Paragraph(
        "(If there was a remote GitHub repository, you could also push that commit ``git push``, "
        "as to enable your colleagues to acces the code as well.)"
    )
    Paragraph(
        "We can use the dot method in a script as follows:"
    )
    CodeBlock(
        [ 'from et_dot import dot'
        , ''
        , 'a = [1,2,3]'
        , 'b = [4.1,4.2,4.3]'
        , 'a_dot_b = dot(a,b)'
        ]
        , language='python'
    )
    Paragraph(
        'Or we might execute these lines at the Python prompt:'
    )
    CodeBlock(
        ['from et_dot import dot'
        , 'a = [1,2,3]'
        , 'b = [4.1,4.2,4.3]'
        , 'a_dot_b = dot(a,b)'
        , 'expected = 1*4.1 + 2*4.2 +3*4.3'
        , 'print(f"a_dot_b = {a_dot_b} == {expected}")'
        ]
        , language='pycon', execute=True, cwd=project_path
    )
    Note(
        'This dot product implementation is naive for several reasons:'
    )
    List(
        [ 'Python is very slow at executing loops, as compared to Fortran or C++.'
        , 'The objects we are passing in are plain Python :py:obj:`list`s. A :py:obj:`list` '
          'is a very powerfull data structure, with array-like properties, but it is not '
          'exactly an array. A :py:obj:`list` is in fact an array of pointers to Python '
          'objects, and therefor list elements can reference anything, not just a numeric '
          'value as we would expect from an array. With elements being pointers, looping '
          'over the array elements implies non-contiguous memory access, another source of '
          'inefficiency.'
        , 'The dot product is a subject of Linear Algebra. Many excellent libraries have been '
          'designed for this purpose. Numpy_ should be your starting point because it is well '
          'integrated with many other Python packages. There is also '
          '`Eigen <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_, a C++ template '
          'library for linear algebra that is neatly exposed to Python by pybind11_.'
        ]
        , indent=4
    )
    Paragraph(
        'However, starting out with a simple and naive implementation is not a bad idea at all. '
        'Once it is proven correct, it can serve as reference implementation to validate later '
        'improvements.'
        , indent=4
    )

    Heading('Testing the code', level=3,crosslink='testing-code')

    Paragraph(
        "In order to prove that our implementation of the dot product is correct, we write "
        "some tests. Open the file :file:`tests/test_et_dot.py`, remove the original "
        "tests put in by micc2_, and add a new one like below:"
    )
    CodeBlock(
        [ 'import et_dot'
        , ''
        , 'def test_dot_aa():'
        , '    a = [1,2,3]'
        , '    expected = 14'
        , '    result = et_dot.dot(a,a)'
        , '    assert result==expected'
        ]
        , language='python', copyto=project_path/'tests/test_et_dot.py'
    )
    Paragraph(
        'The test :py:meth:`test_dot_aa` defines an array with 3 ``int`` '
        'numbers, and computes the dot product with itself. The expected '
        'result is easily calculated by hand. '
        'Save the file, and run the test, usi           ng Pytest_ as explained in '
        ':ref:`testing-your-code`. Pytest_ will show a line for every test '
        'source file an on each such line a ``.`` will appear for every '
        'successfull test, and a ``F`` for a failing test. Here is the '
        'result:'
    )
    CodeBlock(
        "pytest tests"
        , language='bash', execute=True, cwd=project_path
    )
    Paragraph(
        'Great, our test succeeds. If you want some more detail you can add the '
        '``-v`` flag. Pytest_ always captures the output without showing it. '
        'If you need to see it to help you understand errors, add the ``-s`` flag.'
    )
    Paragraph(
        "We thus have added a single test and verified that it works by running "
        "''pytest''. It is good practise to commit this to our local git repository:"
    )
    CodeBlock(
        "git commit -a -m 'added test_dot_aa()'"
        , language='bash', execute=True, cwd=project_path
    )
    Paragraph(
        "Obviously, our test tests only one particular case, and, perhaps, other "
        "cases might fail. A clever way of testing is to focus on properties. "
        "From mathematics we now that the dot product is commutative. Let's add a "
        "test for that. Open :file:`test_et_dot.py` again and add this code:"
    )
    CodeBlock(
        [ 'import random'
        , ''
        , 'def test_dot_commutative():'
        , '    # create two arrays of length 10 with random float numbers:'
        , '    a = []'
        , '    b = []'
        , '    for _ in range(10):'
        , '        a.append(random.random())'
        , '        b.append(random.random())'
        , '    # test commutativity:'
        , '    ab = et_dot.dot(a,b)'
        , '    ba = et_dot.dot(b,a)'
        , '    assert ab==ba'
        ]
        , language='python', copyto=project_path/'tests/test_et_dot.py', append=True
    )
    Note(
        "Focussing on mathematical properties sometimes requires a bit more thought. "
        "Our mathematical intuition is based on the properties of real numbers - which, "
        "as a matter of fact, have infinite precision. Programming languages, however, "
        "use floating point numbers, which have a finite precision. The mathematical "
        "properties for floating point numbers are not the same as for real numbers. "
        "we'll come to that later."
    )
    CodeBlock(
        "pytest tests -v"
        , language='bash', execute=True, cwd=project_path
    )
    Paragraph(
        "The new test passes as well."
    )
    Paragraph(
        "Above we used the :py:meth:`random` module from Python's standard library "
        "for generating the random numbers that populate the array. Every time we "
        "run the test, different random numbers will be generated. That makes the "
        "test more powerful and weaker at the same time. By running the test over "
        "and over againg new random arrays will be tested, growing our cofidence in"
        "our dot product implementations. Suppose, however, that all of a sudden the"
        "test fails. What are we going to do? We know that something is wrong, but "
        "we have no means of investigating the source of the error, because the next "
        "time we run the test the arrays will be different again and the test may "
        "succeed again. The test is irreproducible. Fortunateely, that can be fixed "
        "by setting the seed of the random number generator:"
    )
    CodeBlock(
        [ 'def test_dot_commutative():'
        , '    # Fix the seed for the random number generator of module random.'
        , '    random.seed(0)'
        , '    # choose array size'
        , '    n = 10'
        , '    # create two arrays of length 10 with zeroes:'
        , '    a = n*[0]'
        , '    b = n*[0]'
        , '    # repeat the test 1000 times:'
        , '    for _ in range(1000):'
        , '        for i in range(10):'
        , '             a[i] = random.random()'
        , '             b[i] = random.random()'
        , '    # test commutativity:'
        , '    ab = et_dot.dot(a,b)'
        , '    ba = et_dot.dot(b,a)'
        , '    assert ab==ba'
        ]
        , language='python', copyto=project_path/'tests/test_et_dot.py', append=True
    )
    CodeBlock(
        "pytest tests -v"
        , language='bash', execute=True, cwd=project_path
    )
    Paragraph(
        "The 1000 tests all pass. If, say test 315 would fail, it would fail every time "
        "we run it and the source of error could be investigated."
    )
    Paragraph(
        "Another property is that the dot product of an array of ones with another array "
        "is the sum of the elements of the other array. Let us add another test for that:"
    )
    CodeBlock(
        [ 'def test_dot_one():'
        , '    # Fix the seed for the random number generator of module random.'
        , '    random.seed(0)'
        , '    # choose array size'
        , '    n = 10'
        , '    # create two arrays of length 10 with zeroes, resp. ones:'
        , '    a = n*[0]'
        , '    one = n*[1]'
        , '    # repeat the test 1000 times:'
        , '    for _ in range(1000):'
        , '        for i in range(10):'
        , '             a[i] = random.random()'
        , '    # test:'
        , '    aone = et_dot.dot(a,one)'
        , '    expected = sum(a)'
        , '    assert aone==expected'
        ]
        , language='python', copyto=project_path / 'tests/test_et_dot.py', append=True
    )
    CodeBlock(
        "pytest tests -v"
        , language='bash', execute=True, cwd=project_path
    )
    Paragraph(
        "Success again. We are getting quite confident in the correctness of our implementation. "
        "Here is yet another test:"
    )
    CodeBlock(
        [ 'def test_dot_one_2():'
        , '    a1 = 1.0e16'
        , '    a   = [a1 , 1.0, -a1]'
        , '    one = [1.0, 1.0, 1.0]'
        , '    # test:'
        , '    aone = et_dot.dot(a,one)'
        , '    expected = 1.0'
        , '    assert aone == expected'
        ]
        , language='python', copyto=project_path / 'tests/test_et_dot.py', append=True
    )
    Paragraph(
        "Clearly, it is a special case of the test above. The expected result is the sum "
        "of the elements in ``a``, that is ``1.0``. Yet it - unexpectedly - fails. "
        "Fortunately pytest_ produces a readable report about the failure:"
    )
    CodeBlock(
        "pytest tests -v"
        , language='bash', execute=True, cwd=project_path, error_ok=True
    )
    Paragraph(
        "Mathematically, our expectations about the outcome of the test are certainly correct. "
        "Yet, pytest_ tells us it found that the result is ``0.0`` rather than ``1.0``. What "
        "could possibly be wrong? Well our mathematical expectations are based on our assumption "
        "that the elements of ``a`` are real numbers. They aren't. The elements of ``a`` are "
        "floating point numbers, which can only represent a finite number of decimal digits. "
        "*Double precision* numbers, which are the default floating point type in Python, are "
        "typically truncated after 16 decimal digits, *single precision* numbers after 8. "
        "Observe the consequences of this in the Python statements below:"
    )
    CodeBlock(
        [ "print( 1.0 + 1e16 )"
        , "print( 1e16 + 1.0 )"
        ]
        , language='pycon', execute=True
    )
    Paragraph(
        "Because ``1e16`` is a 1 followed by 16 zeroes, adding ``1`` would alter the 17th digit,"
        "which is, because of the finite precision, not represented. An approximate result is "
        "returned, namely ``1e16``, which is of by a relative error of only 1e-16."
    )
    CodeBlock(
        [ "print( 1e16 + 1.0 - 1e16 )"
        , "print( 1e16 - 1e16 + 1.0 )"
        , "print( 1.0 + 1e16 - 1e16 )"
        ]
        , language='pycon', execute=True
    )
    Paragraph(
        "Although each of these expressions should yield ``0.0``, if they were real numbers, "
        "the result differs because of the finite precision. Python executes the expressions "
        "from left to right, so they are equivalent to: "
    )
    CodeBlock(
        [ "1e16 + 1.0 - 1e16 = ( 1e16 + 1.0 ) - 1e16 = 1e16 - 1e16 = 0.0"
        , "1e16 - 1e16 + 1.0 = ( 1e16 - 1e16 ) + 1.0 = 0.0  + 1.0  = 1.0"
        , "1.0 + 1e16 - 1e16 = ( 1.0 + 1e16 ) - 1e16 = 1e16 - 1e16 = 0.0"
        ]
        , language='pycon'
    )
    Paragraph(
        "There are several lessons to be learned from this:"
    )
    List(
        [ "The test does not fail because our code is wrong, but because our mind is used to "
          "reasoning about real number arithmetic, rather than *floating point arithmetic* "
          "rules. As the latter is subject to round-off errors, tests sometimes fail "
          "unexpectedly. Note that for comparing floating point numbers the the standard "
          "library provides a :py:meth:`math.isclose` method."
        , "Another silent assumption by which we can be mislead is in the random numbers. "
          "In fact, :py:meth:`random.random` generates pseudo-random numbers **in the interval "
          "``[0,1[``**, which is quite a bit smaller than ``]-inf,+inf[``. No matter how often "
          "we run the test the special case above that fails will never be encountered, which "
          "may lead to unwarranted confidence in the code."
        ]
    )
    Paragraph(
        "So let us fix the failing test using :py:meth:`math.isclose` to account for round-off "
        "errors by specifying an relative tolerance and negating the condition for the "
        "original test:"
    )
    CodeBlock(
        [ 'def test_dot_one_2():'
        , '    a1 = 1.0e16'
        , '    a   = [a1 , 1.0, -a1]'
        , '    one = [1.0, 1.0, 1.0]'
        , '    # test:'
        , '    aone = et_dot.dot(a,one)'
        , '    expected = 1.0'
        , '    assert aone != expected'
        , '    assert math.isclose(result, expected, rel_tol=1e-15)'
        ]
        , language='python', copyto=project_path / 'tests/test_et_dot.py', append=True
    )
    Paragraph(
        "Another aspect that deserves testing the behavior of the code in exceptional "
        "circumstances. Does it indeed raise :py:exc:`ArithmeticError` if the arguments "
        "are not of the same length?"
    )
    CodeBlock(
        [ "import pytest"
        , ""
        , "def test_dot_unequal_length():"
        , "    a = [1,2]"
        , "    b = [1,2,3]"
        , "    with pytest.raises(ArithmeticError):"
        , "        et_dot.dot(a,b)"
        ]
        , language='python', copyto=project_path / 'tests/test_et_dot.py', append=True
    )
    Paragraph(
        "Here, :py:meth:`pytest.raises` is a *context manager* that will verify that "
        ":py:exc:`ArithmeticError` is raise when its body is executed. The test will "
        "succeed if indeed the code raises :py:exc:`ArithmeticError` and raise "
        ":py:exc:`AssertionErrorError` if not, causing the test to fail. For an "
        "explanation fo context managers see "
        "`The Curious Case of Python's Context Manager <https://rednafi.github.io/digressions/python/2020/03/26/python-contextmanager.html>`_."
        "Note that you can easily make :meth:`et_dot.dot` raise other exceptions, e.g. "
        ":exc:`TypeError` by passing in arrays of non-numeric types:"
    )
    CodeBlock(
        [ "import et_dot"
        , "et_dot.dot([1,2],[1,'two'])"
        , "del et_dot #hide#"
        ]
        , language='pycon', execute=True, cwd=project_path, error_ok=True
    )
    Paragraph(
        "Note that it is not the product ``a[i]*b[i]`` for ``i=1`` that is wreaking havoc, "
        "but the addition of its result to ``d``. Furthermore, Don't bother the link to "
        "where the error occured in the traceback. It is due to the fact that this course "
        "is completely generated with Python rather than written by hand)."
    )
    Paragraph(
        "More tests could be devised, but the current tests give us sufficient confidence. "
        "The point where you stop testing and move on with the next issue, feature, or "
        "project is subject to various considerations, such as confidence, experience, "
        "problem understanding, and time pressure. In any case this is a good point to "
        "commit changes and additions, increase the version number string, and commit the "
        "version bumb as well:"
    )
    CodeBlock(
        [ "git commit -a -m 'dot() tests added'"
        , "micc2 version -p"
        , "git commit -a -m 'v0.0.1'"
        ]
        , language='bash', execute=True, cwd=project_path
    )
    Paragraph(
        "The the ``micc2 version`` flag ``-p`` is shorthand for ``--patch``, and requests "
        "incrementing the patch (=last) component of the version string, as seen in the "
        "output. The minor component can be incremented with ``-m`` or ``--minor``, the "
        "major component with ``-M`` or ``--major``. "
    )
    Paragraph(
        "At this point you might notice that even for a very simple and well defined "
        "function, as the dot product, the amount of test code easily exceeds the amount "
        "of tested code by a factor of 5 or more. This is not at all uncommon. As the "
        "tested code here is an isolated piece of code, you will probably leave it alone "
        "as soon as it passes the tests and you are confident in the solution. If at some "
        "point, the :py:meth:`dot` would failyou should add a test that reproduces the error "
        "and improve the solution so that it passes the test."
    )
    Paragraph(
        "When constructing software for more complex problems, there will be several "
        "interacting components and running the tests after modifying one of the components "
        "will help you assure that all components still play well together, and spot problems "
        "as soon as possible."
    )

    Heading('Improving efficiency', level=3, crosslink='improving-efficiency')

    Paragraph(
        "There are times when a just a correct solution to the problem at hand is"
        "sufficient. If ``ET-dot`` is meant to compute a few dot products of small "
        "arrays, the naive implementation above will probably be sufficient. "
        "However, if it is to be used many times and for large arrays and the user "
        "is impatiently waiting for the answer, or if your computing resources are "
        "scarse, a more efficient implementation is needed. Especially in scientific "
        "computing and high performance computing, where compute tasks may run for days "
        "using hundreds or even thousands of of compute nodes and resources are to be "
        "shared with many researchers, using the resources efficiently is of utmost "
        "importance and efficient implementations are therefore indispensable."
    )
    Paragraph(
        "However important efficiency may be, it is nevertheless a good strategy for "
        "developing a new piece of code, to start out with a simple, even naive "
        "implementation, neglecting efficiency considerations totally, instead "
        "focussing on correctness. Python has a reputation of being an extremely "
        "productive programming language. Once you have proven the correctness of "
        "this first version it can serve as a reference solution to verify the "
        "correctness of later more efficient implementations. In addition, the "
        "analysis of this version can highlight the sources of inefficiency and "
        "help you focus your attention to the parts that really need it."
    )

    Heading('Timing your code', level=4, crosslink='timing-code')

    Paragraph(
        "The simplest way to probe the efficiency of your code is to time it: write "
        "a simple script and record how long it takes to execute. Here's a script "
        "that computes the dot product of two long arrays of random numbers."
    )
    CodeBlock(
        [ '"""File prof/run1.py"""'
        , 'import sys              #hide#'
        , 'sys.path.insert(0,".")  #hide#'
        , 'import random'
        , 'from et_dot import dot # the dot method is all we need from et_dot'
        , ''
        , 'def random_array(n=1000):'
        , '    """Create an array with n random numbers in [0,1[."""'
        , '    # Below we use a list comprehension (a Python idiom for '
        , '    # creating a list from an iterable object).'
        , '    a = [random.random() for i in range(n)]'
        , '    return a'
        , ''
        , 'if __name__==\'__main__\':'
        , '    a = random_array()'
        , '    b = random_array()'
        , '    print(dot(a, b))'
        , '    print("-*# done #*-")'
        ]
        , language='python', copyto=project_path / 'prof/run1.py'
    )
    Paragraph(
        "Executing this script yields:"
    )
    CodeBlock(
        "python ./prof/run1.py"
        ,language='bash', execute=True, cwd=project_path
    )
    Note(
        "Every run of this script yields a slightly different outcome because "
        "we did not fix ``random.seed()``. It will, however, typically be around "
        "250. Since the average outcome of ``random.random()`` is 0.5, so every "
        "entry contributes on average ``0.5*0.5 = 0.25`` and as there are 1000 "
        "contributions, that makes on average 250.0."
    )
    Paragraph(
        "We are now ready to time our script. There are many ways to achieve this. "
        "Here is a `particularly good introduction <https://realpython.com/python-timer/>`_. "
        "The `et-stopwatch project <https://et-stopwatch.readthedocs.io/en/latest/readme.html>`_ "
        "takes this a little further. It can be installed in your current Python environment "
        "with ``pip``:"
    )
    CodeBlock(
        'python -m pip install et-stopwatch'
        , language='bash', execute=True
    )
    Paragraph(
        "Although ``pip`` is complaining a bit about not being up to date, the "
        "installation is successful."
    )
    Paragraph(
        "To time the script above, modify it as below, using the :py:class:`Stopwatch` "
        "class as a context manager:"
    )
    CodeBlock(
        [ '"""File prof/run1.py"""'
        , 'import sys              #hide#'
        , 'sys.path.insert(0,".")  #hide#'
        , 'import random'
        , 'from et_dot import dot # the dot method is all we need from et_dot'
        , ''
        , 'from et_stopwatch import Stopwatch'
        , ''
        , 'def random_array(n=1000):'
        , '    """Create an array with n random numbers in [0,1[."""'
        , '    # Below we use a list comprehension (a Python idiom for '
        , '    # creating a list from an iterable object).'
        , '    a = [random.random() for i in range(n)]'
        , '    return a'
        , ''
        , 'if __name__==\'__main__\':'
        , '    with Stopwatch(message="init"):'
        , '        a = random_array()'
        , '        b = random_array()'
        , '    with Stopwatch(message="dot "):'
        , '        a_dot_b = dot(a, b)'
        , '    print(a_dot_b)'
        , '    print("-*# done #*-")'
        ]
        , language='python', copyto=project_path / 'prof/run1.py'
    )
    Paragraph(
        "and execute it again:"
    )
    CodeBlock(
        "python ./prof/run1.py"
        ,language='bash', execute=True, cwd=project_path
    )
    Paragraph(
        "When the script is executed each :py:class:`with` block will print "
        "the time it takes to execute its body. The first :py:class:`with` "
        "block times the initialisation of the arrays, and the second times "
        "the computation of the dot product. Note that the initialization of "
        "the arrays takes a bit longer than the dot product computation. "
        "Computing random numbers is expensive."
    )

    Heading("Comparison to Numpy", level=4, crosslink='comparison-numpy')

    Paragraph(
        "As said earlier, our implementation of the dot product is rather "
        "naive. If you want to become a good programmer, you should understand "
        "that you are probably not the first researcher in need of a dot product "
        "implementation. For most linear algebra problems, Numpy_ provides very "
        "efficient implementations.Below the modified :file:`run1.py` script adds "
        "timing results for the Numpy_ equivalent of our code."
    )
    CodeBlock(
        [ '"""File prof/run1.py"""'
        , 'import sys                                                           #hide#'
        , 'sys.path.insert(0,".")                                               #hide#'
        , 'import random                                                        #hide#'
        , 'from et_dot import dot # the dot method is all we need from et_dot   #hide#'
        , 'from et_stopwatch import Stopwatch                                   #hide#'
        , 'def random_array(n=1000):                                            #hide#'
        , '    """Create an array with n random numbers in [0,1[."""            #hide#'
        , '    # Below we use a list comprehension (a Python idiom for          #hide#'
        , '    # creating a list from an iterable object).                      #hide#'
        , '    a = [random.random() for i in range(n)]                          #hide#'
        , '    return a                                                         #hide#'
        , '# ...'
        , 'import numpy as np'
        , ''
        , 'if __name__==\'__main__\':'
        , '    with Stopwatch(message="et init"):'
        , '        a = random_array()'
        , '        b = random_array()'
        , '    with Stopwatch(message="et dot "):'
        , '        dot(a,b)'
        , '    with Stopwatch(message="np init"):'
        , '        a = np.random.rand(1000)'
        , '        b = np.random.rand(1000)'
        , '    with Stopwatch(message="np dot "):'
        , '        np.dot(a,b)'
        , '    print("-*# done #*-")'
        ]
        , language='python', copyto=project_path / 'prof/run1.py'
    )
    Paragraph(
        "Its execution yields:"
    )
    CodeBlock(
        "python ./prof/run1.py"
        ,language='bash', execute=True, cwd=project_path
    )
    Paragraph(
        "Obviously, numpy does significantly better than our naive dot product "
        "implementation. It completes the dot product in 7.5% of the time. It is "
        "important to understand the reasons for this improvement:"
    )
    List(
        [ "Numpy_ arrays are contiguous data structures of floating point numbers, "
          "unlike Python's :py:class:`list` which we have been using for our arrays, "
          "so far. In a Python :py:class:`list` object is in fact a pointer that can "
          "point to an arbitrary Python object. The items in a Python :py:class:`list` "
          "object may even belong to different types. Contiguous memory access is far "
          "more efficient. In addition, the memory footprint of a numpy array is "
          "significantly lower that that of a plain Python list."
        , "The loop over Numpy_ arrays is implemented in a low-level programming "
          "languange, like C, C++ or Fortran. This allows to make full use of the "
          "processors hardware features, such as *vectorization* and "
          "*fused multiply-add* (FMA)."
        ]
    )
    Note(
        "Note that also the initialisation of the arrays with numpy is almost 6 times "
        "faster, for roughly the same reasons."
    )

    Heading('Conclusion', level=4, crosslink='conclusion')

    Paragraph(
        "There are three important generic lessons to be learned from this tutorial:"
    )
    List(
        [ "Always start your projects with a simple and straightforward implementation which "
          "can be easily be proven to be correct, even if you know that it will not satisfy "
          "your efficiency constraints. You should use it as a reference solution to prove the "
          "correctness of later more efficient implementations."
        , "Write test code for proving correctness. Tests must be reproducible, and be run "
          "after every code extension or modification to ensure that the changes did not "
          "break the existing code."
        , "Time your code to understand which parts are time consuming and which not. "
          "Optimize bottlenecks first and do not waste time optimizing code that does "
          "not contribute significantly to the total runtime. Optimized code is typically "
          "harder to read and may become a maintenance issue."
        , 'Before you write any code, in this case our dot product implementation, spend '
          'some time searching the internet to see what is already available. Especially '
          'in the field of scientific and high performance computing there are many excellent '
          'libraries available which are hard to beat. Use your precious time for new stuff. '
          'Consider adding new features to an existing codebase, rather than starting from '
          'scratch. It will improve your programming skills and gain you time, even though '
          'initially your progress may seem slower. It might also give your code more '
          'visibility, and more users, because you provide them with and extra feature on '
          'top of something they are already used to.'
        ]
        , numbered=True
    )

    Heading('Binary extension modules', level=2, crosslink='tutorial-3')

    Heading('Introduction - High Performance Python', level=3, crosslink='intro-HPPython')
    Paragraph(
        "Suppose for a moment that our dot product implementation :py:meth:`et_dot.dot()` "
        "we developed in tutorial-2` is way too slow to be practical for the research "
        "project that needs it, and that we did not have access to fast dot product "
        "implementations, such as :py:meth:`numpy.dot()`. The major advantage we took "
        "from Python is that coding :py:meth:`et_dot.dot()` was extremely easy, and even "
        "coding the tests wasn't too difficult. In this tutorial you are about to discover "
        "that coding a highly efficient replacement for :py:meth:`et_dot.dot()` is not too "
        "difficult either. There are several approaches for this. Here are a number of "
        "highly recommended links covering them:"
    )
    List(
        [ "`Why you should use Python for scientific research <https://developer.ibm.com/dwblog/2018/use-python-for-scientific-research/>`_"
        , "`Performance Python: Seven Strategies for Optimizing Your Numerical Code <https://www.youtube.com/watch?v=zQeYx87mfyw>`_"
        , "`High performance Python 1 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-1>`_"
        , "`High performance Python 2 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-2>`_"
        , "`High performance Python 3 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-3>`_"
        , "`High performance Python 4 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-4>`_"
        ]
    )
    Paragraph(
        "Two of the approaches discussed in the *High Performance Python* series involve "
        "rewriting your code in Modern Fortran or C++ and generate a shared library that "
        "can be imported in Python just as any Python module. This is exactly the approach "
        "taken in important HPC Python modules, such as Numpy_, pyTorch_ and pandas_."
        "Such shared libraries are called *binary extension modules*. Constructing binary "
        "extension modules is by far the most scalable and flexible of all current "
        "acceleration strategies, as these languages are designed to squeeze the maximum of "
        "performance out of a CPU."
    )
    Paragraph(
        "However, figuring out how to build such binary extension modules is a bit of a "
        "challenge, especially in the case of C++. This is in fact one of the main reasons "
        "why Micc2_ was designed: facilitating the construction of binary extension modules "
        "and enabling the developer to create high performance tools with ease. To that end, "
        "Micc2_ can provide boilerplate code for binary extensions as well a practical wrapper "
        "for building the binary extension modules, the ``micc2 build`` command. This command "
        "uses CMake_ to pass the build options to the compiler, while bridging the gap between "
        "C++ and Fortran, on one hand and Python on the other hand using pybind11_ and f2py_. "
        "respectively. This is illustrated in the figure below:"
    )
    Image('../tutorials/im-building.png')
    Paragraph(
        "There is a difference in how f2py_ and pybind11_ operate. F2py_ is an *executable* "
        "that inspects the Fortran source and create wrappers for the subprograms it finds and "
        "uses the compiler to build the extension module. (The wrappers are in C, so f2py_ needs "
        "a C compiler as well). Pybind11_ is a *C++ template library* that is used to express "
        "the interface between Python and C++."
    )

    Heading('Choosing between Fortran and C++ for binary extension modules', level=4, crosslink='f90-or-cpp')

    Paragraph(
        "Here are a number of arguments that you may wish to take into account for choosing the "
        "programming language for your binary extension modules:"
    )
    List(
        [ "Fortran is a simpler language than C++."
        , "It is easier to write efficient code in Fortran than C++."
        , "C++ is a general purpose language (as is Python), whereas Fortran is meant for "
          "scientific computing. Consequently, C++ is a much more expressive language."
        , "C++ comes with a huge standard library, providing lots of data structures and "
          "algorithms that are hard to match in Fortran. If the standard library is not "
          "enough, there are also the highly recommended `Boost <https://boost.org>`_ "
          "libraries and many other high quality domain specific libraries. There are also "
          "domain specific libraries in Fortran, but their count differs by an order of "
          "magnitude at least."
        , "With Pybind11_ you can almost expose anything from the C++ side to Python, and "
          "vice versa, not just functions."
        , "Modern Fortran is (imho) not as good documented as C++. Useful places to look "
          "for language features and idioms are:"
        ]
    )
    List(
        [ 'Fortran: https://www.fortran90.org/'
        , 'C++: http://www.cplusplus.com/'
        , 'C++: https://en.cppreference.com/w/'
        ]
        , indent=4
    )
    Paragraph(
        "In short, C++ provides much more possibilities, but it is not for the novice. "
        "As to my own experience, I discovered that working on projects of moderate "
        "complexity I progressed significantly faster using Fortran rather than C++, "
        "despite the fact that my knowledge of Fortran is quite limited compared to C++. "
        "However, your mileage may vary."
    )

    Heading('Adding Binary extensions to a Micc2_ project',level=3, crosslink='add-bin-ext')

    Paragraph(
        "Adding a binary extension to your current project is simple. To add a binary "
        "extension 'foo' written in (Modern) Fortran, run:"
    )
    CodeBlock(
        "micc add foo --f90"
        , language='bash'
    )
    Paragraph(
        "and for a C++ binary extension, run:"
    )
    CodeBlock(
        "micc add bar --cpp"
        , language='bash'
    )
    Paragraph(
        "The ``add`` subcommand adds a component to your project. It specifies a name, "
        "here, ``foo``, and a flag to specify the kind of the component, ``--f90`` for a "
        "Fortran binary extension module, ``--cpp`` for a C++ binary extension module. "
        "Other components are a Python sub-module with module structure (``--module``), "
        "or package structure ``--package``, and a CLI script (`--cli` and `--clisub`). "
        "More details about these other components are found in :ref:`tutorial-4`."
    )
    Paragraph(
        "You can add as many components to your code as you want. However, the project "
        "must have a *package* structure (see :ref:`modules-and-packages` for how to "
        "convert a project with a *module* structure)."
    )
    Paragraph(
        "The binary modules are build with the ``micc2 build`` command. This build all"
        "binary extension modules in the project. To only build the ``foo`` binary "
        "extension use the ``-m`` flag and specify the module to build:"
    )
    CodeBlock(
        "micc2 build -m foo"
        , language='bash'
    )
    Paragraph(
        "As Micc2_ always creates complete working examples you can build the "
        "binary extensions right away and run their tests with pytest_"
    )
    Paragraph(
        "If there are no syntax errors the binary extensions will be built, "
        "and you will be able to import the modules :py:mod:`foo` and "
        ":py:mod:`bar` in your project scripts and use their subroutines "
        "and functions. Because :py:mod:`foo` and :py:mod:`bar` are "
        "submodules of your micc_ project, you must import them as:"
    )
    CodeBlock(
        [ "import my_package.foo"
        , "import my_package.bar"
        , ""
        , "# call foofun in my_package.foo"\
        , "my_package.foo.foofun(...)"
        , ""
        , "# call barfun in my_package.bar"\
        , "my_package.bar.barfun(...)"
        ]
    )

    Heading('Build options', level=4, crosslink='micc2-build-options')

    Paragraph(
        "Here is an overview of ``micc2 build`` options:"
    )
    CodeBlock(
        "micc2 build --help"
        , language='bash', execute=True
    )

    Heading('Building binary extension modules from Fortran', level=3, crosslink='building-f90')

    Paragraph(
        'So, in order to implement a more efficient dot product, let us add a Fortran '
        'binary extension module with name ``dotf``:'
    )
    # CodeBlock(
    #     "micc2 add dotf --f90"
    #     , language='bash', execute=True, cwd=project_path, error_ok=True
    # )
    # Paragraph(
    #     "For Micc2 to be able to add components to a project, the project must "
    #     "have package structure. We did not foresee that when we created the "
    #     ":file:`ET-dot` project with a module structure, but, fortunately, Micc2 "
    #     "can convert it:"
    # )
    # CodeBlock(
    #     "micc2 convert-to-package --overwrite"
    #     , language='bash', execute=True, cwd=project_path, error_ok=True
    # )
    # Paragraph(
    #     "(See the :ref:`modules-and-packages` section for the meaning of the "
    #     "``--overwrite`` flag). We can now run the ``micc2 add`` command again:"
    # )
    CodeBlock(
        "micc2 add dotf --f90"
        , language='bash', execute=True, cwd=project_path, error_ok=True
    )
    Paragraph(
        "The command now runs successfully, and the output tells us where to "
        "enter the Fortran source code, the build settings, the test code and "
        "the documentation of the added module. Everything related to the "
        ":file:`dotf` sub-module is in subdirectory :file:`ET-dot/et_dot/f90_dotf`. "
        "That directory has a ``f90_`` prefix indicating that it relates to a "
        "Fortran binary extension module. As useal, these files contain "
        "already working example code that you an inspect to learn how things "
        "work."
    )
    Paragraph(
        "Let's continue our development of a Fortran version of the dot product. "
        "Open file :file:`ET-dot/et_dot/f90_dotf/dotf.f90` in your favorite editor "
        "or IDE and replace the existing example code in the Fortran source file with:"
    )
    CodeBlock(
        [ 'function dot(a,b,n)'
        , '  ! Compute the dot product of a and b'
        , '    implicit none'
        , '  !'
        , '  !-----------------------------------------------'
        , '    integer*4              , intent(in)    :: n'
        , '    real*8   , dimension(n), intent(in)    :: a,b'
        , '    real*8                                 :: dot'
        , '  ! declare local variables'
        , '    integer*4 :: i'
        , '  !-----------------------------------------------'
        , '    dot = 0.'
        , '    do i=1,n'
        , '        dot = dot + a(i) * b(i)'
        , '    end do'
        , 'end function dot'
        ]
        , language='fortran', copyto=project_path / 'et_dot/f90_dotf/dotf.f90'
    )
    def annoying(output):
        lines = output.splitlines(keepends=True)
        keep_lines = []
        for line in lines:
            pass
        return '\n'.join(keep_lines)
    Paragraph(
        "The binary extension module can now be built by running ``micc2 build``. "
        "This produces a lot of output, which comes from cmake, f2py and the "
        "compilation process:"
    )
    CodeBlock(
        "micc2 build --clean"
        , language='bash', execute=True, cwd=project_path
    )

    extension_suffix = sysconfig.get_config_var('EXT_SUFFIX')
    pydist, pyver, os_so = extension_suffix.split('-')
    os,soext = os_so.split('.')


    Paragraph(
        f"If there are no syntax errors in the Fortran code, the binary extension "
        f"module will build successfully, as above and be installed in a the "
        f"package directory of our project :file:`ET-dot/et_dot`. The full module "
        f"name is :file:`dotf{extension_suffix}`. The extension is composed of: "
        f"the kind of Python distribution (``{pydist[1:]}``), the MAJORminor version "
        f"string of the Python version being used (``{pyver}`` as we are running "
        f"Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}), "
        f"the OS on which we are working (``{os}``), and an extension indicating "
        f"a shared library on this OS (``.{soext}``). This file can be imported "
        f"in a Python script, by using the filename without the extension, i.e. "
        f"``dotf``. As the module was built successfully, we can test it. Here is "
        f"some test code. Enter it in file :file:`ET-dot/tests/test_f90_dotf.py`:"
    )
    CodeBlock(
        [ 'import numpy as np'
        , 'import et_dot'
        , '# create an alias for the dotf binary extension module'
        , 'f90 = et_dot.dotf'
        , ''
        , 'def test_dot_aa():'
        , '    # create an numpy array of floats:'
        , '    a = np.array([0,1,2,3,4],dtype=float)'
        , '    # use the original dot implementation to compute the expected result:'
        , '    expected = et_dot.dot(a,a)'
        , '    # call the dot function in the binary extension module with the same arguments:'
        , '    a_dot_a = f90.dot(a,a)'
        , '    assert a_dot_a == expected'
        ]
        , language='Python', copyto=project_path / 'tests/test_f90_dotf.py'
    )
    Paragraph(
        "Then run the test (we only run the test for the dotf module, as "
        "we did not touch the :py:meth:`et_dot.dot` implementation):"
    )
    CodeBlock(
        "pytest tests/test_f90_dotf.py"
        , language='bash', execute=True, cwd=project_path
    )
    Paragraph(
        "The astute reader will notice the magic that is happening here: "
        "``a`` is a numpy array, which is passed as the first and second "
        "parameter to the :py:meth:`et_dot.dotf.dot` function defined in "
        "our binary extension module. Note that the third parameter of "
        "the :py:meth:`et_dot.dotf.dot` function is omitted. How did that "
        "happen? The Micc2 build function uses f2py_ to build the binary "
        "extension module. When calling :py:meth:`et_dot.dotf.dot` you are "
        "in fact calling a wrapper function that f2py created that extracts "
        "the pointer to the memory of array ``a`` and its length. The wrapper "
        "function then calls the Fortran function with the approprioate "
        "parameters as specified in the Fortran function definition. This "
        "invisible wrapper function is in fact rather intelligent, it even "
        "handles type conversions. E.g. we can pass in a Python array, and "
        "the wrapper will convert it into a numpy array, or an array of ints, "
        "and the wrapper will convert it into a float array. In fact the "
        "wrapper considers all implicit type conversions allowed by Python. "
        "However practical this feature may be, type conversion requires "
        "copying the entire array and converting each element. For long "
        "arrays this may be prohibitively expensive. For this reason the "
        ":file:`et_dot/f90_dotf/CMakeLists.txt` file specifies the "
        "``F2PY_REPORT_ON_ARRAY_COPY=1`` flag which makes the wrappers issue a "
        "warning to tell you that you should modify the client program to pass "
        "types to the wrapper which to not require conversion."
    )
    CodeBlock(
        [ 'import et_dot'
        , 'from importlib import reload                             #hide#'
        , 'et_dot = reload(et_dot)                                  #hide#'
        , 'a = [1,2,3]'
        , 'b = [2,2,2]'
        , 'print(et_dot.dot(a,b))'
        , 'print(et_dot.dotf.dot(a,b))'
        , 'print("created an array from object",file=sys.stderr)    #hide#'
        , 'print("created an array from object",file=sys.stderr)    #hide#'
        ]
    , language = 'pycon', execute=True, cwd=project_path
    )
    # For some reason the error message 'created an array from object' is not
    # captured by python. we faked it with a hidden print stmt.

    Paragraph(
        "Here, ``a`` and ``b`` are plain Python lists, not numpy arrays, and"
        "they contain ``int`` numbers. :py:meth:`et_dot.dot()` therefore also "
        "returns an int (``12``). However, the Fortran implementation "
        ":py:meth:`et_dot.dotf.dot()` expects an array of floats and returns a "
        "float (``12.0``). The wrapper converts the Python lists ``a`` and ``b`` "
        "to numpy ``float`` arrays. If the binary extension module was compiled "
        "with ``F2PY_REPORT_ON_ARRAY_COPY=1`` (the default setting) the wrapper "
        "will warn you with the message``created an array from object``. If we "
        "construct the numpy arrays ourselves, but still of type ``int``, the "
        "wrapper has to convert the ``int`` array into a ``float`` array, because "
        "that is what corresponds the the Fortran ``real*8`` type, and will "
        "warn that it *copied* the array to make the conversion:"
    )
    CodeBlock(
        [ 'import et_dot'
        , 'import numpy as np'
        , 'from importlib import reload                                 #hide#'
        , 'et_dot = reload(et_dot)                                      #hide#'
        , 'a = np.array([1,2,3])'
        , 'b = np.array([2,2,2])'
        , 'print(et_dot.dot(a,b))'
        , 'print(et_dot.dotf.dot(a,b))'
        , 'print("copied an array: size=3, elsize=8", file=sys.stderr)  #hide#'
        , 'print("copied an array: size=3, elsize=8", file=sys.stderr)  #hide#'
        ]
    , language = 'pycon', execute=True, cwd=project_path
    )
    # For some reason the error message 'copied an array: size=3, elsize=8' is
    # not captured by python. we faked it with a hidden print stmt.
    Paragraph(
        "Here, ``size`` refers to the length of the array, and elsize is the"
        "number of bytes needed for each element of the target array type, c.q. "
        "a ``float``."
    )
    Note(
        "The wrappers themselves are generated in C code, so, you not only need "
        "a Fortran compiler, but also a C compiler."
    )
    Paragraph(
        "Note that the test code did not explicitly import :py:mod:`et_dot.dotf`, "
        "just :py:mod:`et_dot`. This is only possible because Micc2 has modified "
        ":file:`et_dot/__init__.py` to import every submodule that has been added "
        "to the project:"
    )
    CodeBlock(
        [ '# in file et_dot/__init__.py'
        , 'import et_dot.dotf'
        ]
        , language='python'
    )
    Paragraph(
        "If the submodule :py:mod:`et_dot.dotf` was not built or failed to build, "
        "that import statement will fail and raise a :py:exc:`ModuleNotFoundError` "
        "exception. Micc2 has added a little extra magic to attempt to build the "
        "module automatically in that case:"
    )
    CodeBlock(
        [ '# in file et_dot/__init__.py'
        , 'try:'
        , '    import et_dot.dotf'
        , 'except ModuleNotFoundError as e:'
        , '    # Try to build this binary extension:'
        , '    from pathlib import Path'
        , '    import click'
        , '    from et_micc2.project import auto_build_binary_extension'
        , '    msg = auto_build_binary_extension(Path(__file__).parent, "dotf")'
        , '    if not msg:'
        , '        import et_dot.dotf'
        , '    else:'
        , '        click.secho(msg, fg="bright_red")'
        ]
        , language='python'
    )

    Heading("Dealing with Fortran modules", level=4, crosslink='f90-modules')

    Paragraph(
        "Modern Fortran has a *module* concept of its own. This may be a bit confusing, "
        "as we have been talking about modules in a Python context, so far. The Fortran "
        "module is meant to group variable and procedure definitions that conceptually "
        "belong together. Inside fortran they are comparable to C/C++ header files. Here "
        "is an example:"
    )
    CodeBlock(
        [ 'MODULE my_f90_module'
        , 'implicit none'
        , 'contains'
        , '  function dot(a,b)'
        , '    ...'
        , '  end function dot'
        , 'END MODULE my_f90_module'
        ]
        , language='fortran'
    )
    Paragraph(
        "F2py translates the module containing the Fortran ``dot`` definition into "
        "an extra *namespace* appearing in between the :py:mod:`dotf` Python submodule "
        "and the :py:meth:`dot` function, which is found in ``et_dot.dotf.my_f90_module`` "
        "instead of in ``et_dot.dotf``."
    )


    """
    """
    doc.verbose = True
    if write:
        doc.write(Path.home()/'workspace/et-micc2/tutorials/')
    else:
        print(f'>>>>>>\n{doc}\n<<<<<<')


# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    # set write to False for debugging
    # write = False

    the_test_you_want_to_debug = test_Tutorial2

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof