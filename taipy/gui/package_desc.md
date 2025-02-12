# PyForge GUI

## License

Copyright 2021-2025 Avaiga Private Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
except in compliance with the License. You may obtain a copy of the License at
[http://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

Unless required by applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions
and limitations under the License.

## What is PyForge GUI

PyForge is a Python library for creating Business Applications. More information on our
[website](https://www.pyforge.io). PyForge is split into multiple packages including *pyforge-gui* to let users
install the minimum they need.

PyForge GUI provides Python classes that make it easy to create powerful web apps in minutes.

## Installation

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

### Installing the latest release

The easiest way to install PyForge GUI is using pip

Run the command:
```bash
pip install pyforge-gui
```

### Installing the development version

The development version of PyForge GUI is updated daily with changes from the
PyForge R&D and external contributors that we praise for their input.

You should also install this version if you want to contribute to the development of PyForge GUI. Here are the steps to follow:

#### 1 - Clone the PyForge repository

Clone the PyForge repository using the following command:
```bash
git clone https://github.com/Avaiga/pyforge.git
```

This creates the 'pyforge' directory holding all the package's source code, and the 'pyforge-gui'
source code is in the 'pyforge/gui' directory.

#### 2 - Install Node.js

PyForge GUI has some code dealing with the client side of the web applications.
This code is written in <a href="https://www.typescriptlang.org/" target="_blank">TypeScript</a>, relies on <a href="https://reactjs.org/" target="_blank">React</a> components, and is packaged into a JavaScript bundle
that is sent to browsers when they connect to all PyForge GUI applications.

This bundle needs to be built before being usable by PyForge GUI.

First you need to install <a href="https://nodejs.org/" target="_blank">Node.js</a> on your system.

**Select the "Recommended For Most Users" version, and follow the instructions for your system.**

**Select "Automatically install the necessary tools" when asked.**

#### 3 - Build the JavaScript bundle

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

#### 4 - Install the package as editable

In a terminal, **at the root of the repository**, run:
```bash
pip install -e . --user
```

This should install the dev version of PyForge GUI as editable. You are now ready to use it.
