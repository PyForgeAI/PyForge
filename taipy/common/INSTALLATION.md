# Installation

The latest stable version of *pyforge-common* can be installed using `pip`:
```bash
pip install pyforge-common
```

## Development version

You can install the development version of *pyforge-common* with `pip` and `git` directly from the PyForge repository:
```bash
pip install git+https://git@github.com/Avaiga/pyforge
```

This command installs the development version of *pyforge* package in the Python environment with all
its dependencies, including the *pyforge-common* package.

If you need the source code for *pyforge-common* on your system so you can see how things are done or
maybe participate in the improvement of the packages, you can clone the GitHub repository:

```bash
git clone https://github.com/Avaiga/pyforge.git
```

This creates the 'pyforge' directory holding all the package's source code, and the 'pyforge-common'
source code is in the 'pyforge/config' directory.

## Running the tests

To run the tests on the package, you need to install the required development packages.
We recommend using [Pipenv](https://pipenv.pypa.io/en/latest/) to create a virtual environment
and install the development packages.

```bash
pip install pipenv
pipenv install --dev
```

Then you can run *pyforge-common* tests with the following command:

```bash
pipenv run pytest tests/common
```
