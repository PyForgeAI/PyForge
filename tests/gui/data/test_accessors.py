import typing as t
from unittest.mock import Mock

from pyforge.gui import Gui
from pyforge.gui.data.data_accessor import (
    _DataAccessor,
    _DataAccessors,
    _InvalidDataAccessor,
)
from pyforge.gui.data.data_format import _DataFormat
from pyforge.gui.utils.types import _PyForgeData


class MyDataAccessor(_DataAccessor):
    @staticmethod
    def get_supported_classes() -> t.List[t.Type]:
        return [int]

    def get_data(
        self,
        var_name: str,
        value: t.Any,
        payload: t.Dict[str, t.Any],
        data_format: _DataFormat,
    ) -> t.Dict[str, t.Any]:
        return {"value": 2 * int(value)}

    def get_cols_description(self, var_name: str, value: t.Any) -> t.Dict[str, t.Dict[str, str]]:  # type: ignore
        pass

    def to_pandas(self, value: t.Any) -> t.Union[t.List[t.Any], t.Any]:
        pass

    def on_edit(self, value: t.Any, payload: t.Dict[str, t.Any]) -> t.Optional[t.Any]:
        pass

    def on_delete(self, value: t.Any, payload: t.Dict[str, t.Any]) -> t.Optional[t.Any]:
        pass

    def on_add(
        self,
        value: t.Any,
        payload: t.Dict[str, t.Any],
        new_row: t.Optional[t.List[t.Any]] = None,
    ) -> t.Optional[t.Any]:
        pass

    def to_csv(self, var_name: str, value: t.Any) -> t.Optional[str]:
        pass


def mock_pyforge_data(value):
    """Helper to mock _PyForgeData objects."""
    mock_data = Mock(spec=_PyForgeData)
    mock_data.get.return_value = value
    return mock_data


def test_custom_accessor(gui: Gui):
    """Test if get_data() uses the correct accessor."""
    data_accessors = _DataAccessors(gui)
    data = mock_pyforge_data(123)

    # Testing when accessor is not registered
    data_accessor = data_accessors._get_instance(mock_pyforge_data)  # type: ignore
    assert isinstance(
        data_accessor, _InvalidDataAccessor
    ), f"Expected _InvalidDataAccessor but got {type(data_accessor)}"
    result = data_accessors.get_data("var_name", data, {})
    assert result == {}

    # Testing when accessor is registered
    data_accessors._register(MyDataAccessor)

    result = data_accessors.get_data("var_name", data, {})
    assert isinstance(result, dict)
    assert result["value"] == 246

    data_accessors._unregister(MyDataAccessor)
