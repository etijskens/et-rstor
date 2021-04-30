# -*- coding: utf-8 -*-

"""Tests for et_rstor package."""

from et_rstor import *
from pathlib import Path
import os


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
        'pip install my_nifty_module'
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
        , language='bash', execute=True, cwd=workspace
    )
    Paragraph(
        "As there are indeed hundreds of thousands of Python packages published on PyPI_, "
        "finding a good name has become quite hard. Personally, I often use a simple and "
        "short descriptive name, prefixed by my initials, :filee:`et-`, which usually makes "
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
        , language='bash', execute=True, cwd=workspace
    )
    Paragraph(
        "The last line indicates that you can specify an explicit module name, unrelated to "
        "the project name. In that case PEP8 compliance is not checked. The responsability "
        "is then all yours."
    )

    Heading("First steps in project management using Micc2", level=3, crosslink='first-steps')

    Heading("The project path in Micc2", level=4, crosslink='micc-project-path')

    Paragraph(
        "All micc_ commands accept the global ``--project-path=<path>`` parameter. "
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
        "pip install some-needed-package"
        , language='bash'
    )
    Paragraph(
        "We must also install the project itself, if it is to be used in the virtual environment. "
        "If the project is not under development, we can just run ``pip  install .``. Otherwise, "
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

    Heading('Testing your code', level=4, crosslink='testing')

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
        "When micc_ created project :file:`my-first-project`, it not only added a ``hello`` method "
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
        "imports them and collects the test methods, and executes them. Micc_ also "
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
        'code using `Sphinx <http://www.sphinx-doc.org/en/master/>`_. It is extracted '
        'from the doc-strings in your code. Doc-strings are the text between triple '
        'double quote pairs in the examples above, e.g. ``"""This is a doc-string."""``.'
        'Important doc-strings are:'
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
        "micc2 docs html"
        , language='bash', prompt='(.venv-my-first-project) > '
    )
    Paragraph(
        "This will generate documentation in :file:`et-dot/docs/_build/html`. "
        "The default html theme for this is sphinx_rtd_theme_. To view "
        "the documentation open the file :file:`et-dot/docs/_build/html/index.html`. "
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
        "The project directory contains a :file:`LICENCE` file, a :file:`text` file "
        "describing the licence applicable to your project. You can choose between:"
    )
    List(
        [ 'MIT license,'
        , 'BSD license,'
        , 'ISC license,'
        , 'Apache Software License 2.0,'
        , 'GNU General Public License v3, and'
        , 'Not open source.'
        ]
    )
    Paragraph(
        "When you set up Micc2 you can select the default license for your Micc2_ projects. "
        "You can always overwrite the default option when you create a project:"
    )
    CodeBlock(
        "micc2 --software-license=create"
    )
    """

    MIT license is a very liberal license and the default option. If you’re unsure which
    license to choose, you can use resources such as `GitHub’s Choose a License <https://choosealicense.com>`_

    You can select the license file when you create the project:
    """
    doc.verbose = True
    print('>>>>>>')
    # print(doc.items[-1])
    print(doc, end='')
    print('<<<<<<')

import re
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
# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_Tutorial1

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof