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

import sys


def extract_gui_version(base_path: str) -> None:
    with open("setup.py") as f:
        for line in f:
            if "pyforge-gui" in line:
                start = line.find("pyforge-gui")
                end = line.rstrip().find('",')
                print(f"VERSION={line[start:end]}")  # noqa: T201
                break


if __name__ == "__main__":
    extract_gui_version(sys.argv[1])
