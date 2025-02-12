# PyForge Templates

## License

Copyright 2021-2025 Avaiga Private Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
except in compliance with the License. You may obtain a copy of the License at
[http://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

Unless required by applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions
and limitations under the License.

## What is PyForge templates

PyForge is a Python library for creating Business Applications. More information on our
[website](https://www.pyforge.io). PyForge is split into multiple packages including *pyforge-templates*
to let users install the minimum they need.

PyForge templates is a repository that contains application templates created and
maintained by PyForge. It helps users getting started with a simple and ready-to-go application.

To create a PyForge application using this template, first you need to install PyForge (> 2.2).
Then from a terminal, run the following command.
```bash
pyforge create
```
or
```bash
pyforge create --application "default"
```

After providing necessary information, your new application is created in the current
working directory.

## Installation

The latest stable version of *pyforge-templates* is available through *pip*:
```bash
pip install pyforge-templates
```

You can install the development version of *pyforge-templates* with *pip* and *git* via the pyforge repository:
```bash
pip install git+https://git@github.com/Avaiga/pyforge
```

This command installs the development version of *pyforge* package in the Python environment with all
its dependencies, including the *pyforge-templates* package.

If you need the source code for *pyforge-templates* on your system so you can see how things are done or
maybe participate in the improvement of the packages, you can clone the GitHub repository:

```bash
git clone https://github.com/Avaiga/pyforge.git
```

This creates the 'pyforge' directory holding all the package's source code, and the 'pyforge-templates'
source code is in the 'pyforge/templates' directory.
