# Copyright 2021-2025 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import os
import sys
from importlib.util import find_spec

from pyforge.common._cli._base_cli._pyforge_parser import _PyForgeParser
from pyforge.common._cli._create_cli_factory import _CreateCLIFactory
from pyforge.common._cli._help_cli import _HelpCLI
from pyforge.common._cli._run_cli import _RunCLI
from pyforge.core._cli._core_cli_factory import _CoreCLIFactory
from pyforge.core._entity._migrate_cli import _MigrateCLI
from pyforge.core._version._cli._version_cli_factory import _VersionCLIFactory
from pyforge.gui._gui_cli import _GuiCLI

from .version import _get_version


def _entrypoint():
    # Add the current working directory to path to execute version command on FS repo
    sys.path.append(os.path.normpath(os.getcwd()))

    _PyForgeParser._parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Print the current PyForge version and exit.",
    )

    if find_spec("pyforge.enterprise"):
        from pyforge.enterprise._entrypoint import _entrypoint_initialize as _enterprise_entrypoint_initialize

        _enterprise_entrypoint_initialize()

    _core_cli = _CoreCLIFactory._build_cli()
    _create_cli = _CreateCLIFactory._build_cli()

    _RunCLI.create_parser()
    _GuiCLI.create_run_parser()
    _core_cli.create_run_parser()

    _VersionCLIFactory._build_cli().create_parser()
    _create_cli.generate_template_map()
    _create_cli.create_parser()
    _MigrateCLI.create_parser()
    _HelpCLI.create_parser()

    if find_spec("pyforge.enterprise"):
        from pyforge.enterprise._entrypoint import _entrypoint_handling as _enterprise_entrypoint_handling

        _enterprise_entrypoint_handling()

    args, _ = _PyForgeParser._parser.parse_known_args()
    if args.version:
        print(f"PyForge {_get_version()}")  # noqa: T201
        sys.exit(0)

    _RunCLI.handle_command()
    _HelpCLI.handle_command()
    _VersionCLIFactory._build_cli().handle_command()
    _MigrateCLI.handle_command()
    _create_cli.handle_command()

    _PyForgeParser._remove_argument("help")
    _PyForgeParser._parser.print_help()
