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

from pyforge.gui import Gui


def test_layout_md_1(gui: Gui, helpers):
    md_string = """
<|layout|columns=1 1|gap=1rem|
# This is a layout section
|>
"""
    expected_list = ["<Layout", 'columns="1 1', 'gap="1rem"', "<h1", "This is a layout section"]
    helpers.test_control_md(gui, md_string, expected_list)


def test_layout_md_2(gui: Gui, helpers):
    md_string = """
<|layout.start|columns=1 1|gap=1rem|>
# This is a layout section
<|layout.end|>
"""
    expected_list = ["<Layout", 'columns="1 1', 'gap="1rem"', "<h1", "This is a layout section"]
    helpers.test_control_md(gui, md_string, expected_list)


def test_layout_html(gui: Gui, helpers):
    html_string = '<pyforge:layout columns="1 1" gap="1rem"><h1>This is a layout section</h1></pyforge:layout>'
    expected_list = ["<Layout", 'columns="1 1', 'gap="1rem"', "<h1", "This is a layout section"]
    helpers.test_control_html(gui, html_string, expected_list)
