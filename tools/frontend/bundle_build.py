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

import platform
import subprocess
import sys
from pathlib import Path

with_shell = platform.system() == "Windows"


def build_gui(root_path: Path):
    print(f"Building pyforge-gui frontend bundle in {root_path}.")  # noqa: T201
    already_exists = (root_path / "pyforge" / "gui" / "webapp" / "index.html").exists()
    if already_exists:
        print(f'Found pyforge-gui frontend bundle in {root_path  / "pyforge" / "gui" / "webapp"}.')  # noqa: T201
    else:
        subprocess.run(["npm", "ci"], cwd=root_path / "frontend" / "pyforge-gui" / "dom", check=True, shell=with_shell)
        subprocess.run(["npm", "ci"], cwd=root_path / "frontend" / "pyforge-gui", check=True, shell=with_shell)
        subprocess.run(["npm", "run", "build"], cwd=root_path / "frontend" / "pyforge-gui", check=True, shell=with_shell)


def build_pyforge(root_path: Path):
    print(f"Building pyforge frontend bundle in {root_path}.")  # noqa: T201
    already_exists = (root_path / "pyforge" / "gui_core" / "lib" / "pyforge-gui-core.js").exists()
    if already_exists:
        print(f'Found pyforge frontend bundle in {root_path / "pyforge" / "gui_core" / "lib"}.')  # noqa: T201
    else:
        # Specify the correct path to pyforge-gui in gui/.env file
        env_file_path = root_path / "frontend" / "pyforge" / ".env"
        if not env_file_path.exists():
            with open(env_file_path, "w") as env_file:
                env_file.write(f"TAIPY_DIR={root_path}\n")
        subprocess.run(["npm", "ci"], cwd=root_path / "frontend" / "pyforge", check=True, shell=with_shell)
        subprocess.run(["npm", "run", "build"], cwd=root_path / "frontend" / "pyforge", check=True, shell=with_shell)


if __name__ == "__main__":
    root_path = Path(__file__).absolute().parent.parent.parent
    if len(sys.argv) > 1:
        if sys.argv[1] == "gui":
            build_gui(root_path)
        elif sys.argv[1] == "pyforge":
            build_pyforge(root_path)
    else:
        build_gui(root_path)
        build_pyforge(root_path)
