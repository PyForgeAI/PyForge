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


import warnings

import pytest

from pyforge.gui.utils.date import _string_to_date
from pyforge.gui.utils.types import _PyForgeBool, _PyForgeData, _PyForgeDate, _PyForgeNumber


def test_pyforge_data():
    tb = _PyForgeData("value", "hash")
    assert tb.get() == "value"
    assert tb.get_name() == "hash"
    tb.set("a value")
    assert tb.get() == "a value"
    assert tb.get_hash() == "_TpD"


def test_pyforge_bool():
    assert _PyForgeBool(0, "v").get() is False
    assert _PyForgeBool(1, "v").get() is True
    assert _PyForgeBool(False, "v").get() is False
    assert _PyForgeBool(True, "v").get() is True
    assert _PyForgeBool("", "v").get() is False
    assert _PyForgeBool("hey", "v").get() is True
    assert _PyForgeBool([], "v").get() is False
    assert _PyForgeBool(["an item"], "v").get() is True


def test_pyforge_number():
    with pytest.raises(TypeError):
        _PyForgeNumber("a string", "x").get()
    with warnings.catch_warnings(record=True):
        _PyForgeNumber("a string", "x").cast_value("a string")
    _PyForgeNumber(0, "x").cast_value(0)


def test_pyforge_date():
    assert _PyForgeDate(_string_to_date("2022-03-03 00:00:00 UTC"), "x").get() == "2022-03-03T00:00:00+00:00"
    assert _PyForgeDate("2022-03-03 00:00:00 UTC", "x").get() == "2022-03-03 00:00:00 UTC"
    assert _PyForgeDate(None, "x").get() is None
    _PyForgeDate("", "x").cast_value("2022-03-03 00:00:00 UTC")
    _PyForgeDate("", "x").cast_value(_string_to_date("2022-03-03 00:00:00 UTC"))
