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
from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from json import JSONEncoder
from pathlib import Path

import numpy
import pandas
from flask.json.provider import DefaultJSONProvider

from .._warnings import _warn
from ..icon import Icon
from ..utils import _date_to_string, _DoNotUpdate, _MapDict, _PyForgeBase
from ..utils.singleton import _Singleton


class JsonAdapter(ABC):
    """NOT DOCUMENTED"""
    def register(self):
        _PyForgeJsonAdapter().register(self)

    @abstractmethod
    def parse(self, o) -> t.Union[t.Any, None]:
        return None


class _DefaultJsonAdapter(JsonAdapter):
    def parse(self, o):
        if isinstance(o, Icon):
            return o._to_dict()
        if isinstance(o, _MapDict):
            return o._dict
        if isinstance(o, _PyForgeBase):
            return o.get()
        if isinstance(o, (datetime, date, time)):
            return _date_to_string(o)
        if isinstance(o, Path):
            return str(o)
        if isinstance(o, (timedelta, pandas.Timedelta)):
            return str(o)
        if isinstance(o, numpy.generic):
            return getattr(o, "tolist", lambda: o)()
        if isinstance(o, _DoNotUpdate):
            return None


class _PyForgeJsonAdapter(object, metaclass=_Singleton):
    def __init__(self) -> None:
        self._adapters: t.List[JsonAdapter] = []
        self.register(_DefaultJsonAdapter())

    def register(self, adapter: JsonAdapter):
        self._adapters.append(adapter)

    def parse(self, o):
        try:
            for adapter in reversed(self._adapters):
                if (output := adapter.parse(o)) is not None:
                    return output
            raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable (value: {o}).")
        except Exception as e:
            _warn("Exception while resolving JSON", e)
            return None


class _PyForgeJsonEncoder(JSONEncoder):
    def default(self, o):
        return _PyForgeJsonAdapter().parse(o)


class _PyForgeJsonProvider(DefaultJSONProvider):
    default = staticmethod(_PyForgeJsonAdapter().parse)  # type: ignore
    sort_keys = False
