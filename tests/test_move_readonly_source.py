import re
from types import MappingProxyType
from typing import Any
from typing import Dict

import pytest

from jsonpath import JSONPatch
from jsonpath import JSONPatchError


@pytest.mark.parametrize(
    ("source", "from_path", "parent_type"),
    [
        (MappingProxyType({"item": "payload"}), "/source/item", "mappingproxy"),
        (("payload",), "/source/0", "tuple"),
    ],
)
def test_move_readonly_source_preserves_destination(
    source: object, from_path: str, parent_type: str
) -> None:
    data: Dict[str, Any] = {"source": source, "destination": {}}
    operation = JSONPatch().move(from_=from_path, path="/destination/item")
    expected = f"unexpected operation on {parent_type!r} (move:0)"

    with pytest.raises(JSONPatchError, match=re.escape(expected)):
        operation.apply(data)

    assert data["destination"] == {}
    assert data["source"] is source
