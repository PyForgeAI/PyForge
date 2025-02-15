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

from datetime import datetime

from pyforge.gui import Gui


def test_date_range_md_1(gui: Gui, test_client, helpers):
    gui._bind_var_val(
        "dates", [datetime.strptime("15 Dec 2020", "%d %b %Y"), datetime.strptime("31 Dec 2020", "%d %b %Y")]
    )
    md_string = "<|{dates}|date_range|>"
    expected_list = [
        "<DateRange",
        'defaultDates="[&quot;2020-12-',
        'updateVarName="_TpDr_tpec_TpExPr_dates_TPMDL_0"',
        "dates={_TpDr_tpec_TpExPr_dates_TPMDL_0}",
    ]
    helpers.test_control_md(gui, md_string, expected_list)


def test_date_range_md_2(gui: Gui, test_client, helpers):
    gui._bind_var_val(
        "dates", [datetime.strptime("15 Dec 2020", "%d %b %Y"), datetime.strptime("31 Dec 2020", "%d %b %Y")]
    )
    md_string = "<|{dates}|date_range|with_time|label_start=start|label_end=end|>"
    expected_list = [
        "<DateRange",
        'defaultDates="[&quot;2020-12-',
        'updateVarName="_TpDr_tpec_TpExPr_dates_TPMDL_0"',
        "dates={_TpDr_tpec_TpExPr_dates_TPMDL_0}",
        "withTime={true}",
        'labelStart="start"',
        'labelEnd="end"',
    ]
    helpers.test_control_md(gui, md_string, expected_list)

def test_date_range_md_3(gui: Gui, test_client, helpers):
    gui._bind_var_val(
        "dates", [datetime.strptime("15 Dec 2020", "%d %b %Y"), datetime.strptime("31 Dec 2020", "%d %b %Y")]
    )
    md_string = "<|{dates}|date_range|with_time|analogic|label_start=start|label_end=end|>"
    expected_list = [
        "<DateRange",
        'defaultDates="[&quot;2020-12-',
        'updateVarName="_TpDr_tpec_TpExPr_dates_TPMDL_0"',
        "dates={_TpDr_tpec_TpExPr_dates_TPMDL_0}",
        "withTime={true}",
        "analogic={true}",
        'labelStart="start"',
        'labelEnd="end"',
    ]
    helpers.test_control_md(gui, md_string, expected_list)

def test_date_range_md_width(gui: Gui, test_client, helpers):
    # do not remove test_client: it brings an app context needed for this test
    gui._bind_var_val(
        "dates", [datetime.strptime("15 Dec 2020", "%d %b %Y"), datetime.strptime("31 Dec 2020", "%d %b %Y")]
    )
    md_string = "<|{dates}|date_range|width=70%|>"
    expected_list = [
        "<DateRange",
        'defaultDates="[&quot;2020-12-',
        'updateVarName="_TpDr_tpec_TpExPr_dates_TPMDL_0"',
        'width="70%"',
        "dates={_TpDr_tpec_TpExPr_dates_TPMDL_0}",
    ]
    helpers.test_control_md(gui, md_string, expected_list)


def test_date_range_html_1(gui: Gui, test_client, helpers):
    gui._bind_var_val(
        "dates", [datetime.strptime("15 Dec 2020", "%d %b %Y"), datetime.strptime("31 Dec 2020", "%d %b %Y")]
    )
    html_string = '<pyforge:date_range dates="{dates}" />'
    expected_list = [
        "<DateRange",
        'defaultDates="[&quot;2020-12-',
        'updateVarName="_TpDr_tpec_TpExPr_dates_TPMDL_0"',
        "dates={_TpDr_tpec_TpExPr_dates_TPMDL_0}",
    ]
    helpers.test_control_html(gui, html_string, expected_list)


def test_date_range_html_2(gui: Gui, test_client, helpers):
    gui._bind_var_val(
        "dates", [datetime.strptime("15 Dec 2020", "%d %b %Y"), datetime.strptime("31 Dec 2020", "%d %b %Y")]
    )
    html_string = "<pyforge:date_range>{dates}</pyforge:date_range>"
    expected_list = [
        "<DateRange",
        'defaultDates="[&quot;2020-12-',
        'updateVarName="_TpDr_tpec_TpExPr_dates_TPMDL_0"',
        "dates={_TpDr_tpec_TpExPr_dates_TPMDL_0}",
    ]
    helpers.test_control_html(gui, html_string, expected_list)
