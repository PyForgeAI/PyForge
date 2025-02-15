Welcome to the installation section of the PyForge web application builder! This section will
guide you through the seamless and straightforward process of setting up and deploying your
own powerful web applications.

!!! note "Installation for Contributing to PyForge"

    If you aim to modify the PyForge source code or contribute to its development, please refer
    to the contributing page to get more information.

# Installing PyForge library

## Prerequisite

Before installing PyForge, ensure you have Python (**version 3.9 or later**) and
[pip](https://pip.pypa.io) installed on your system. If you don't have pip installed, you can
follow these steps to install it:

1. **[Python Installation Guide](http://docs.python-guide.org/en/latest/starting/installation/)**:
    Follow the installation guide to set up Python on your system.
    After the installation, you can open the Command Prompt and type `python --version` to check
    the installed Python version.

2. **[Installing pip](https://pip.pypa.io/en/latest/installation/)**: Pip is included by default
    if you use Python 3.4 or later. Otherwise, you can follow the official
    installation page of pip to install it. To verify the installation, type `pip --version` or
    `pip3 --version`.

Alternatively, if you are using a Conda environment, you can install pip using the following
command:
```console
conda install pip
```

## The latest stable release from Pypi

### Pip
The preferred method to install PyForge is by using **pip**. After downloading PyForge package
from **[PyPI repository](https://pypi.org/project/pyforge/)** the following commands install
it in the Python environment with all its dependencies. Open your terminal or command prompt
and run the following command:
```console
pip install pyforge
```

### Pipenv
If you are using a virtual environment with **[Pipenv](https://pipenv.pypa.io/en/latest/)**,
use the following command:
```console
pipenv install pyforge
```

### Venv
Alternatively, you can use `venv` to create a virtual environment. Please run the following
commands replacing `<myenv>` (twice) with your desired environment name:
```console
python -m venv <myenv>
source myenv/bin/activate  # On Windows use `<myenv>\Scripts\activate`
pip install pyforge
```

### Conda
If you prefer to work within a [Conda](https://docs.conda.io/projects/conda/en/latest/index.html)
environment, you can install PyForge using the following commands replacing `<myenv>` with your
desired environment name:
```console
conda create -n <myenv>
conda activate <myenv>
pip install pyforge
```

## A specific version from PyPI

### Pip
To install a specific version of PyForge, use the following command replacing `<version>` with a
specific version number of PyForge among the
**[list of all released PyForge versions](https://pypi.org/project/pyforge/#history)**:
```console
pip install pyforge==<version>
```

### Pipenv
If you are using a virtual environment with **[Pipenv](https://pipenv.pypa.io/en/latest/)**,
use the following command:
```console
pipenv install pyforge==<version>
```

### Venv
Alternatively, you can use `venv` to create a virtual environment:
```console
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
pip install pyforge==<version>
```

### Conda
If you prefer to work within a [Conda](https://docs.conda.io/projects/conda/en/latest/index.html)
environment, you can install PyForge using the following commands replacing `<myenv>` with your
desired environment name:
```console
conda create -n <myenv>
conda activate <myenv>
pip install pyforge==<version>
```

## A development version from GitHub

### Pip
The development version of PyForge is hosted on
**[GitHub repository](https://git@github.com/Avaiga/pyforge)** using the `develop` branch. This
branch is updated daily with changes from the PyForge R&D team and external contributors whom we
praise for their input.

The development version of PyForge can be installed using **pip**. After downloading PyForge source
code from the **[GitHub repository](https://git@github.com/Avaiga/pyforge)** the following commands
build the package, and install it in the Python environment with all its dependencies.

Open your terminal or command prompt and run the following command:

```bash
pip install git+https://git@github.com/Avaiga/pyforge
```

### Pipenv
If you are using a virtual environment with **[Pipenv](https://pipenv.pypa.io/en/latest/)**,
use the following command:
```console
pipenv install git+https://git@github.com/Avaiga/pyforge
```

### Venv
Alternatively, you can use `venv` to create a virtual environment:
```console
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
pip install git+https://git@github.com/Avaiga/pyforge
```

### Conda
If you prefer to work within a [Conda](https://docs.conda.io/projects/conda/en/latest/index.html)
environment, you can install PyForge using the following commands replacing `<myenv>` with your
desired environment name:
```console
conda create -n <myenv>
conda activate <myenv>
pip install git+https://git@github.com/Avaiga/pyforge
```

# Installing PyForge with Colab

Google Colab is a popular and free Jupyter notebook environment that requires no setup
and runs entirely in the cloud. To install PyForge in Google Colab, follow these simple
steps:

1. **Open a new Colab notebook**: Visit [Google Colab](https://colab.research.google.com)
    and start a new notebook.

2. **Run the installation command**: In a new cell, enter the following command and run
    the cell to install the latest stable release of PyForge in your Colab environment:

    ```python
    !pip install --ignore-installed pyforge
    ```

3. **Start building your app**: Follow this
    [tutorial](https://docs.pyforge.io/en/latest/tutorials/articles/colab_with_ngrok/) to build
    and run your PyForge web application directly within the Colab notebook.

!!! tip
    Remember that Google Colab environments are ephemeral. If you disconnect or restart
    your Colab session, you will need to reinstall PyForge.
