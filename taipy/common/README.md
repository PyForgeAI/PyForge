# PyForge Common

## License
Copyright 2021-2025 Avaiga Private Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at
[http://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

## Usage
- [License](#license)
- [Usage](#usage)
- [PyForge Common](#what-is-pyforge-common)
- [Installation](#installation)
- [Contributing](#contributing)
- [Code of conduct](#code-of-conduct)
- [Directory Structure](#directory-structure)

## What is PyForge Common

PyForge is a Python library for creating Business Applications. More information on our
[website](https://www.pyforge.io). PyForge is split into multiple packages including *pyforge-common* to let users
install the minimum they need.

PyForge Common is a package designed to have the code that serves as basis for the other PyForge packages,
including classes and methods to enable logging, cli and users to configure their PyForge application.

More in-depth documentation of pyforge can be found [here](https://docs.pyforge.io).

## Installation

Want to install *PyForge Common*? Check out our [`INSTALLATION.md`](INSTALLATION.md) file.

## Contributing

Want to help build *PyForge Common*? Check out our [`CONTRIBUTING.md`](../../CONTRIBUTING.md) file.

## Code of conduct

Want to be part of the *PyForge Common* community? Check out our [`CODE_OF_CONDUCT.md`](../../CODE_OF_CONDUCT.md) file.

## Directory Structure

- `pyforge/`:
  - `common/`: Common data structures, types, and functions.
    - `config/`: Configuration definition, management, and implementation. `pyforge.Config` is the main entrypoint for configuring a PyForge Core application.
      - `_config_comparator/`: Internal package for comparing configurations.
      - `_serializer/`: Internal package for serializing and deserializing configurations.
      - `checker/`: Configuration checker and issue collector implementation.
      - `common/`: Shared data structures, types, and functions.
      - `exceptions/`: *pyforge-common* exceptions.
      - `global_app/`: `GlobalAppConfig` implementation.
      - `stubs/`: Helper functions to create the `config.pyi` file.
      - `INSTALLATION.md`: Instructions to install *pyforge-common*.
      - `LICENSE`: The Apache 2.0 License.
      - `README.md`: Current file.
      - `setup.py`: The setup script managing building, distributing, and installing *pyforge-common*.
    - `logger/`: PyForge logger implementation.
- `tests/`:
  - `common/`: Tests for the *pyforge-common* package.
