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
import traceback
import typing as t
import warnings


class PyForgeGuiWarning(UserWarning):
    """NOT DOCUMENTED

    Warning category for PyForge warnings generated in user code.
    """

    _tp_debug_mode = False

    @staticmethod
    def set_debug_mode(debug_mode: bool):
        PyForgeGuiWarning._tp_debug_mode = (
            debug_mode if debug_mode else hasattr(sys, "gettrace") and sys.gettrace() is not None
        )


class PyForgeGuiAlwaysWarning(PyForgeGuiWarning):
    pass


def _warn(
    message: str,
    e: t.Optional[BaseException] = None,
    always_show: t.Optional[bool] = False,
):
    warnings.warn(
        (
            f"{message}:\n{''.join(traceback.format_exception(e))}"
            if e and PyForgeGuiWarning._tp_debug_mode
            else f"{message}:\n"
            + "".join(traceback.format_exception(None, e, e.__traceback__.tb_next if e.__traceback__ else None))
            if e
            else message
        ),
        PyForgeGuiWarning if not always_show else PyForgeGuiAlwaysWarning,
        stacklevel=2,
    )
