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

import inspect
import logging
from importlib import util

import pytest

if util.find_spec("playwright"):
    from playwright._impl._page import Page

from pyforge.gui import Gui


@pytest.mark.teste2e
def test_dict(page: "Page", gui: Gui, helpers):
    page_md = """
<|{a_dict[a_key]}|input|id=inp1|>
<|{a_dict.key}|input|id=inp2|>
<|test|button|on_action=on_action_1|id=btn1|>
<|test|button|on_action=on_action_2|id=btn2|>
"""
    a_key = "key"
    a_dict = {a_key: "PyForge"}  # noqa: F841

    def on_action_1(state):
        state.a_dict.key = "Hello"

    def on_action_2(state):
        state.a_dict[state.a_key] = "World"

    gui._set_frame(inspect.currentframe())
    gui.add_page(name="test", page=page_md)
    helpers.run_e2e(gui)
    page.goto("./test")
    page.expect_websocket()
    page.wait_for_selector("#inp1")

    assert_text(page, "PyForge", "PyForge")

    page.fill("input#inp1", "PyForge is the best")
    function_evaluated = True
    try:
        page.wait_for_function("document.querySelector('#inp2').value !== 'PyForge'")
    except Exception as e:
        function_evaluated = False
        logging.getLogger().debug(f"Function evaluation timeout.\n{e}")
    if function_evaluated:
        assert_text(page, "PyForge is the best", "PyForge is the best")

    page.fill("#inp2", "PyForge-Gui")
    function_evaluated = True
    try:
        page.wait_for_function("document.querySelector('#inp1').value !== 'PyForge is the best'")
    except Exception as e:
        function_evaluated = False
        logging.getLogger().debug(f"Function evaluation timeout.\n{e}")
    if function_evaluated:
        assert_text(page, "PyForge-Gui", "PyForge-Gui")

    page.click("#btn1")
    function_evaluated = True
    try:
        page.wait_for_function("document.querySelector('#inp1').value !== 'PyForge-Gui'")
    except Exception as e:
        function_evaluated = False
        logging.getLogger().debug(f"Function evaluation timeout.\n{e}")
    if function_evaluated:
        assert_text(page, "Hello", "Hello")

    page.click("#btn2")
    function_evaluated = True
    try:
        page.wait_for_function("document.querySelector('#inp1').value !== 'Hello'")
    except Exception as e:
        function_evaluated = False
        logging.getLogger().debug(f"Function evaluation timeout.\n{e}")
    if function_evaluated:
        assert_text(page, "World", "World")


def assert_text(page, inp1, inp2):
    assert page.input_value("input#inp1") == inp1
    assert page.input_value("input#inp2") == inp2
