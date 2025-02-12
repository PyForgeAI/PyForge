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

import os
import pathlib
from unittest import TestCase, mock

from pyforge.common.logger._pyforge_logger import _PyForgeLogger


class TestPyForgeLogger(TestCase):
    def test_pyforge_logger(self):
        _PyForgeLogger._get_logger().info("baz")
        _PyForgeLogger._get_logger().debug("qux")

    def test_pyforge_logger_configured_by_file(self):
        path = os.path.join(pathlib.Path(__file__).parent.resolve(), "logger.conf")
        with mock.patch.dict(os.environ, {"TAIPY_LOGGER_CONFIG_PATH": path}):
            _PyForgeLogger._get_logger().info("baz")
            _PyForgeLogger._get_logger().debug("qux")
