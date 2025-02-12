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

import logging
import os
import sys


def test_import_pyforge_packages() -> bool:
    """
    Import pyforge package and call gui, Scenario and rest attributes.
    """
    import pyforge as tp

    valid_install = True
    if not hasattr(tp, "gui"):
        logging.error("PyForge installation has no attribute gui")
        valid_install = False
    if not hasattr(tp, "Scenario"):
        logging.error("PyForge installation has no attribute Scenario")
        valid_install = False
    if not hasattr(tp, "rest"):
        logging.error("PyForge installation has no attribute rest")
        valid_install = False

    return valid_install


def is_pyforge_gui_install_valid() -> bool:
    from pathlib import Path

    import pyforge

    pyforge_gui_core_path = Path(pyforge.__file__).absolute().parent / "gui_core" / "lib" / "pyforge-gui-core.js"
    if not pyforge_gui_core_path.exists():
        logging.error("File pyforge-gui-core.js not found in pyforge installation path")
        return False

    pyforge_gui_webapp_path = Path(pyforge.__file__).absolute().parent / "gui" / "webapp"

    if not os.path.exists(pyforge_gui_webapp_path):
        return False

    if not any(fname.endswith(".js") for fname in os.listdir(pyforge_gui_webapp_path)):
        logging.error("Missing js files inside pyforge gui webapp folder")
        return False

    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logging.info("Trying to import pyforge and verify it's main attributes")
    if not test_import_pyforge_packages() or not is_pyforge_gui_install_valid():
        sys.exit(1)

    logging.info("PyForge installation Validated")
    sys.exit(0)
