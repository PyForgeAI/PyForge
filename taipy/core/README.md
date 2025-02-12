# PyForge Core

## License

Copyright 2021-2025 Avaiga Private Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
except in compliance with the License. You may obtain a copy of the License at
[http://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

Unless required by applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions
and limitations under the License.

## Usage

- [PyForge Core](#pyforge-core)
- [License](#license)
- [Usage](#usage)
- [What is PyForge Core](#what-is-pyforge-core)
- [Installation](#installation)
- [Contributing](#contributing)
- [Code of conduct](#code-of-conduct)
- [Directory Structure](#directory-structure)

## What is PyForge Core

PyForge is a Python library for creating Business Applications. More information on our
[website](https://www.pyforge.io). PyForge is split into multiple packages including
*pyforge-core* to let users install the minimum they need.

PyForge Core mostly includes business-oriented
features. It helps users create and manage business applications and improve analyses
capability through time, conditions and hypothesis.

A more in depth documentation of pyforge can be found [here](https://docs.pyforge.io).

## Installation

Want to install *PyForge Core*? Check out our [`INSTALLATION.md`](INSTALLATION.md) file.

## Contributing

Want to help build *PyForge Core*? Check out our [`CONTRIBUTING.md`](../../CONTRIBUTING.md) file.

## Code of conduct

Want to be part of the *PyForge Core* community? Check out our
[`CODE_OF_CONDUCT.md`](../../CODE_OF_CONDUCT.md) file.

## Directory Structure

- `pyforge/`:
  - `core/`:
    - `_entity/`: Internal package for abstract entity definition and entity's properties management.
    - `_manager/`: Internal package for entity manager.
    - `_orchestrator/`: Internal package for task orchestrating and execution.
    - `_repository/`: Internal package for data storage.
    - `_version/`: Internal package for managing PyForge Core application version.
    - `common/`: Shared data structures, types, and functions.
    - `config/`: Configuration definition, management and implementation.
    - `cycle/`: Work cycle definition, management and implementation.
    - `data/`: Data Node definition, management and implementation.
    - `exceptions/`: *pyforge-core* exceptions.
    - `job/`: Job definition, management and implementation.
    - `notification/`: Notification management system implementation.
    - `scenario/`: Scenario definition, management and implementation.
    - `sequence/`: Sequence definition, management and implementation.
    - `submission/`: Submission definition, management and implementation.
    - `task/`: Task definition, management and implementation.
    - `pyforge.py`: Main entrypoint for *pyforge-core* runtime features.
    - `INSTALLATION.md`: Instructions to install *pyforge-core*.
    - `LICENSE`: The Apache 2.0 License.
    - `README.md`: Current file.
    - `setup.py`: The setup script managing building, distributing, and installing *pyforge-core*.
- `tests/`:
  - `core/`: Unit tests following the `pyforge/core/` structure.
