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

import typing as t
from enum import Enum
from inspect import isclass

from .data import Decimator
from .utils import (
    _PyForgeBase,
    _PyForgeBool,
    _PyForgeContent,
    _PyForgeContentHtml,
    _PyForgeContentImage,
    _PyForgeData,
    _PyForgeDate,
    _PyForgeDateRange,
    _PyForgeDict,
    _PyForgeLoNumbers,
    _PyForgeLov,
    _PyForgeLovValue,
    _PyForgeNumber,
    _PyForgeTime,
    _PyForgeToJson,
)


class _WsType(Enum):
    ACTION = "A"
    MULTIPLE_UPDATE = "MU"
    REQUEST_UPDATE = "RU"
    DATA_UPDATE = "DU"
    UPDATE = "U"
    ALERT = "AL"
    BLOCK = "BL"
    NAVIGATE = "NA"
    CLIENT_ID = "ID"
    APP_ID = "AID"
    MULTIPLE_MESSAGE = "MS"
    DOWNLOAD_FILE = "DF"
    PARTIAL = "PR"
    ACKNOWLEDGEMENT = "ACK"
    GET_MODULE_CONTEXT = "GMC"
    GET_DATA_TREE = "GDT"
    GET_ROUTES = "GR"
    FAVICON = "FV"
    BROADCAST = "BC"
    LOCAL_STORAGE = "LS"


NumberTypes = {"int", "int64", "float", "float64"}


class PropertyType(Enum):
    """
    All the possible element property types.

    This is used when creating custom visual elements, where you have
    to indicate the type of each property.

    Some types are 'dynamic', meaning that if the property value is modified, it
    is automatically handled by PyForge and propagated to the entire application.

    See `ElementProperty^` for more details.
    """

    any = "any"
    """
    The property holds a value of any serializable type.
    """
    dynamic_any = "dynamicany"
    """
    The property is dynamic and holds a value of any serializable type.
    """
    boolean = "boolean"
    """
    The property holds a Boolean value.
    """
    toHtmlContent = _PyForgeContentHtml
    content = _PyForgeContent
    data = _PyForgeData
    date = _PyForgeDate
    date_range = _PyForgeDateRange
    dict = "dict"
    time = _PyForgeTime
    """
    The property holds a dictionary.
    """
    dynamic_date = "dynamicdate"
    """
    The property is dynamic and holds a date.
    """
    dynamic_dict = _PyForgeDict
    """
    The property is dynamic and holds a dictionary.
    """
    dynamic_number = _PyForgeNumber
    """
    The property is dynamic and holds a number.
    """
    dynamic_lo_numbers = _PyForgeLoNumbers
    """
    The property is dynamic and holds a list of numbers.
    """
    dynamic_boolean = _PyForgeBool
    """
    The property is dynamic and holds a Boolean value.
    """
    dynamic_list = "dynamiclist"
    """
    The property is dynamic and holds a list.

    The React component must have two parameters: "<propertyName>" that must be a list of object, and
    "default<PropertyName>" that must be a string, set to the JSON representation of the initial value
    of the property.
    """
    dynamic_string = "dynamicstring"
    """
    The property is dynamic and holds a string.
    """
    function = "function"
    """
    The property holds a reference to a function.
    """
    image = _PyForgeContentImage
    json = "json"
    single_lov = "singlelov"
    lov = _PyForgeLov
    lov_no_default = "lovnodefault"
    """
    The property holds a LoV (list of values).
    """
    lov_value = _PyForgeLovValue
    """
    The property holds a value in a LoV (list of values).
    """
    number = "number"
    """
    The property holds a number.
    """
    react = "react"
    broadcast = "broadcast"
    string = "string"
    """
    The property holds a string.
    """
    string_or_number = "string|number"
    """
    The property holds a string or a number.

    This is typically used to handle CSS dimension values, where a unit can be used.
    """
    boolean_or_list = "boolean|list"
    slider_value = "number|number[]|lovValue"
    toggle_value = "boolean|lovValue"
    string_list = "stringlist"
    decimator = Decimator
    """
    The property holds an inner attributes that is defined by a library and cannot be overridden by the user.
    """
    inner = "inner"
    to_json = _PyForgeToJson


@t.overload  # noqa: F811
def _get_pyforge_type(a_type: None) -> None: ...


@t.overload
def _get_pyforge_type(a_type: t.Type[_PyForgeBase]) -> t.Type[_PyForgeBase]:  # noqa: F811
    ...


@t.overload
def _get_pyforge_type(a_type: PropertyType) -> t.Type[_PyForgeBase]:  # noqa: F811
    ...


@t.overload
def _get_pyforge_type(  # noqa: F811
    a_type: t.Optional[t.Union[t.Type[_PyForgeBase], t.Type[Decimator], PropertyType]],
) -> t.Optional[t.Union[t.Type[_PyForgeBase], t.Type[Decimator], PropertyType]]: ...


def _get_pyforge_type(  # noqa: F811
    a_type: t.Optional[t.Union[t.Type[_PyForgeBase], t.Type[Decimator], PropertyType]],
) -> t.Optional[t.Union[t.Type[_PyForgeBase], t.Type[Decimator], PropertyType]]:
    if a_type is None:
        return None
    if isinstance(a_type, PropertyType) and not isinstance(a_type.value, str):
        return a_type.value
    if isclass(a_type) and not isinstance(a_type, PropertyType) and issubclass(a_type, _PyForgeBase):
        return a_type
    if a_type == PropertyType.boolean:
        return _PyForgeBool
    elif a_type == PropertyType.number:
        return _PyForgeNumber
    return None
