# Installation

The latest stable version of *pyforge-core* is available through *pip*:
```bash
pip install pyforge-core
```

## Development version

You can install the development version of *pyforge-core* with *pip* and *git* via the pyforge repository:
```bash
pip install git+https://git@github.com/Avaiga/pyforge
```

This command installs the development version of *pyforge* package in the Python environment with all
its dependencies, including the *pyforge-core* package.

If you need the source code for *pyforge-core* on your system so you can see how things are done or
maybe participate in the improvement of the packages, you can clone the GitHub repository:

```bash
git clone https://github.com/Avaiga/pyforge.git
```

This creates the 'pyforge' directory holding all the package's source code, and the 'pyforge-core'
source code is in the 'pyforge/core' directory.

## Running the tests

To run the tests on the package, you need to install the required development packages.
We recommend using [Pipenv](https://pipenv.pypa.io/en/latest/) to create a virtual environment
and install the development packages.

```bash
pip install pipenv
pipenv install --dev
```

Then you can run *pyforge-core* tests with the following command:

```bash
pipenv run pytest tests/core
```
