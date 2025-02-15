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

import pyforge.gui.builder as tgb
from pyforge.gui import Gui


def test_part_builder_1(gui: Gui, helpers):
    with tgb.Page(frame=None) as page:
        with tgb.part(class_name="class1"):  # type: ignore[attr-defined]
            tgb.text(value="This is a part")  # type: ignore[attr-defined]
    expected_list = ["<Part", "This is a part"]
    helpers.test_control_builder(gui, page, expected_list)
