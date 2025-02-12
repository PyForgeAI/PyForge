# Installation

There are different ways to install PyForge GUI, depending on how
you plan to use it:

- [Installing the latest release](#installing-the-latest-release)
- [Installing the development version](#installing-the-development-version)
  - [1 - Clone the repository](#1---clone-the-repository)
  - [2 - Install Node.js](#2---install-nodejs)
  - [3 - Build the JavaScript bundle](#3---build-the-javascript-bundle)
  - [4 - Install the package as editable](#4---install-the-package-as-editable)
- [Debugging the JavaScript bundle](#debugging-the-javascript-bundle)
- [Running the tests](#running-the-tests)

PyForge GUI needs your system to have **Python 3.9** or above installed.

## Installing the latest release

The easiest way to install PyForge GUI is using pip

Run the command:
```bash
pip install pyforge-gui
```

## Installing the development version

The development version of PyForge GUI is updated daily with changes from the
PyForge R&D and external contributors that we praise for their input.

You should also install this version if you want to contribute to the development of PyForge GUI. Here are the steps to follow:

### 1 - Clone the PyForge repository

Clone the PyForge repository using the following command:
```bash
git clone https://github.com/Avaiga/pyforge.git
```

This creates the 'pyforge' directory holding all the package's source code, and the 'pyforge-gui'
source code is in the 'pyforge/gui' directory.

### 2 - Install Node.js

PyForge GUI has some code dealing with the client side of the web applications.
This code is written in <a href="https://www.typescriptlang.org/" target="_blank">TypeScript</a>, relies on <a href="https://reactjs.org/" target="_blank">React</a> components, and is packaged into a JavaScript bundle
that is sent to browsers when they connect to all PyForge GUI applications.

This bundle needs to be built before being usable by PyForge GUI.

First you need to install <a href="https://nodejs.org/" target="_blank">Node.js</a> on your system.

**Select the "Recommended For Most Users" version, and follow the instructions for your system.**

**Select "Automatically install the necessary tools" when asked.**

### 3 - Build the JavaScript bundle

Open a new terminal and run the following commands:

- Install the DOM dependencies
```bash
cd gui
cd dom
npm i
```
- Install the web app dependencies
```bash
cd ..
npm i
```
- Build the web app
```bash
npm run build
```

After a few minutes, this creates the directory `pyforge/gui/webapp` in the root directory of the repository
where the front-end code for PyForge GUI is split into a set of JavaScript bundles.

### 4 - Install the package as editable

In a terminal, **at the root of the repository**, run:
```bash
pip install -e . --user
```

This should install the dev version of PyForge GUI as editable. You are now ready to use it.

## Debugging the JavaScript bundle

If you plan to modify the front-end code and need to debug the TypeScript
code, you must use the following:
```bash
npm run build:dev
```

instead of the *standard* build option.

This will preserve the debugging symbols, and you will be able to navigate in the
TypeScript code from your debugger.

> **Note:** Web application location
>
> When you are developing front-end code for the PyForge GUI package, it may
> be cumbersome to have to install the package over and over when you know
> that all that has changed is the JavaScript bundle that makes the PyForge
> web app.
>
> By default, the PyForge GUI application searches for the front-end code
> in the `[pyforge-gui-package-dir]/pyforge/src/gui/webapp` directory.<br/>
> You can, however, set the environment variable `TAIPY_GUI_WEBAPP_PATH`
> to the location of your choice, and PyForge GUI will look for the web
> app in that directory.<br/>
> If you set this variable to the location where you build the web app
> repeatedly, you will no longer have to reinstall PyForge GUI before you
> try your code again.


## Running the tests

To run the tests on the package, you need to install the required development packages.
We recommend using [Pipenv](https://pipenv.pypa.io/en/latest/) to create a virtual environment
and install the development packages.

```bash
pip install pipenv
pipenv install --dev
```

Then you can run *pyforge-gui* tests with the following command:

```bash
pipenv run pytest tests/gui
```
