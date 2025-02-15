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


def test_metric_builder_none(gui: Gui, helpers):
    with tgb.Page(frame=None) as page:
        tgb.metric(type=None, value=42)
    expected_list = ["<Metric", 'type="None"', 'value={42.0}']
    helpers.test_control_builder(gui, page, expected_list)

def test_metric_builder_none_lowercase(gui: Gui, helpers):
    with tgb.Page(frame=None) as page:
        tgb.metric(type="none", value=42)
    expected_list = ["<Metric", 'type="none"', 'value={42.0}']
    helpers.test_control_builder(gui, page, expected_list)

def test_metric_builder_circular(gui: Gui, helpers):
    with tgb.Page(frame=None) as page:
        tgb.metric(type="circular", value=42)
    expected_list = ["<Metric", 'type="circular"', 'value={42.0}']
    helpers.test_control_builder(gui, page, expected_list)

def test_metric_builder_linear(gui: Gui, helpers):
    with tgb.Page(frame=None) as page:
        tgb.metric(type="linear", value=42)
    expected_list = ["<Metric", 'type="linear"', 'value={42.0}']
    helpers.test_control_builder(gui, page, expected_list)
