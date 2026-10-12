# Copyright 2026 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generated PySTAC extension. Edit the source schema and regenerate to update."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Literal, TypeVar, cast

if TYPE_CHECKING:
    from collections.abc import Mapping

from pystac.extensions.base import (
    ExtensionManagementMixin,
    PropertiesExtension,
    SummariesExtension,
)

import pystac

SCHEMA_URI = "https://stac-extensions.github.io/access/v0.1.0/schema.json"
FIELD_TARGETS = {
    "access:availability": [
        "asset",
        "catalog",
        "collection",
        "item",
        "item_asset",
        "link",
        "summary",
    ],
    "access:instructions": [
        "asset",
        "catalog",
        "collection",
        "item",
        "item_asset",
        "link",
        "summary",
    ],
    "access:restrictions": [
        "asset",
        "catalog",
        "collection",
        "item",
        "item_asset",
        "link",
        "summary",
    ],
    "access:retrieval_time": [
        "asset",
        "catalog",
        "collection",
        "item",
        "item_asset",
        "link",
        "summary",
    ],
    "access:type": ["asset", "catalog", "collection", "item", "item_asset", "link", "summary"],
    "alternate": ["asset", "item_asset"],
    "assetTemplates": ["catalog", "collection"],
    "linkTemplates": ["catalog", "collection"],
}
FIELD_NAMES = {
    "availability": "access:availability",
    "instructions": "access:instructions",
    "restrictions": "access:restrictions",
    "retrieval_time": "access:retrieval_time",
    "type": "access:type",
    "alternate": "alternate",
    "assetTemplates": "assetTemplates",
    "linkTemplates": "linkTemplates",
}
TARGETS = ["asset", "catalog", "collection", "item", "item_asset", "link", "summary"]
T = TypeVar(
    "T",
    bound="pystac.Collection | pystac.Catalog | pystac.Item | pystac.Asset | pystac.ItemAssetDefinition | pystac.Link",
)


def _target_for(obj: object) -> str:
    """Identify supported STAC targets, checking Collection before its Catalog base."""
    target_types = (
        (pystac.Collection, "collection"),
        (pystac.Catalog, "catalog"),
        (pystac.Item, "item"),
        (pystac.Asset, "asset"),
        (pystac.ItemAssetDefinition, "item_asset"),
        (pystac.Link, "link"),
    )
    for object_type, target in target_types:
        if isinstance(obj, object_type):
            if target not in TARGETS:
                break
            return target
    raise pystac.ExtensionTypeError(f"Unsupported extension target: {type(obj).__name__}")


class _Unset:
    """Distinguish omitted arguments from explicit JSON null."""


_UNSET = _Unset()


def _encode(value: Any) -> Any:
    """Convert generated objects at any depth into plain JSON containers."""
    if isinstance(value, _Object):
        value = value.properties
    if isinstance(value, dict):
        return {key: _encode(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode(child) for child in value]
    return value


def _decode(value: Any, codec: Any) -> Any:
    """Wrap schema-declared objects while retaining live backing dictionaries."""
    if value is None or codec is None:
        return value
    kind, detail = codec
    if kind == "object":
        return _MODELS[detail].from_dict(value)
    if kind == "list":
        return _decode_list(value, detail)
    if kind == "map":
        return _decode_map(value, detail)
    raise ValueError(f"Unknown conversion: {kind}")


def _decode_list(value: Any, codec: Any) -> list[Any]:
    """Decode the elements of a schema-declared array."""
    if not isinstance(value, list):
        raise TypeError("Expected a JSON array")
    return [_decode(child, codec) for child in value]


def _decode_map(value: Any, codec: Any) -> dict[str, Any]:
    """Decode the values of a schema-declared object map."""
    if not isinstance(value, dict):
        raise TypeError("Expected a JSON object map")
    return {key: _decode(child, codec) for key, child in value.items()}


_O = TypeVar("_O", bound="_Object")


@dataclass
class _Object:
    """Live wrapper around JSON, following PySTAC value-object conventions."""

    _members: ClassVar[dict[str, str]] = {}
    properties: dict[str, Any]

    def __post_init__(self) -> None:
        """Require a JSON object as the live backing value."""
        if not isinstance(self.properties, dict):
            raise TypeError(f"{type(self).__name__} requires a dictionary")

    @classmethod
    def from_dict(cls: type[_O], properties: dict[str, Any], *, copy: bool = False) -> _O:
        """Wrap by reference, or request an independent copy."""
        from copy import deepcopy

        return cls(deepcopy(properties) if copy else properties)

    def to_dict(self) -> dict[str, Any]:
        """Return the live backing JSON dictionary, as PySTAC Render does."""
        return self.properties

    def _apply(self, values: Mapping[str, object]) -> None:
        """Check update names before changing the backing dictionary."""
        unknown = values.keys() - self._members.keys()
        if unknown:
            raise TypeError(f"Unknown fields: {sorted(unknown)}")
        for name, value in values.items():
            if not isinstance(value, _Unset):
                setattr(self, name, value)

    def clear(self, name: str) -> None:
        """Remove a member using its Python attribute name."""
        self.properties.pop(self._members[name], None)

    def set_null(self, name: str) -> None:
        """Store explicit JSON null using a Python member name."""
        self.properties[self._members[name]] = None

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.properties!r}>"


class Alternate(_Object):
    """Generated nested value object; unknown JSON members are preserved."""

    _members: ClassVar[dict[str, str]] = {
        "availability": "access:availability",
        "instructions": "access:instructions",
        "restrictions": "access:restrictions",
        "retrieval_time": "access:retrieval_time",
        "type": "access:type",
    }

    @classmethod
    def create(
        cls,
        *,
        availability: Literal["online", "nearline", "offline"] | _Unset = _UNSET,
        instructions: str | _Unset = _UNSET,
        restrictions: list[
            Literal[
                "registration", "agreement", "data_fee", "transfer_fee", "membership", "approval"
            ]
        ]
        | _Unset = _UNSET,
        retrieval_time: str | _Unset = _UNSET,
        type: Literal["open", "embargoed", "restricted", "closed"] | _Unset = _UNSET,
    ) -> Alternate:
        """Create with typed members; omitted optionals are not written.

        Explicit None writes null. Validate the STAC object to check value constraints.
        """
        _values = {
            "access:availability": availability,
            "access:instructions": instructions,
            "access:restrictions": restrictions,
            "access:retrieval_time": retrieval_time,
            "access:type": type,
        }
        return cls(
            {key: _encode(value) for key, value in _values.items() if not isinstance(value, _Unset)}
        )

    def apply(
        self,
        *,
        availability: Literal["online", "nearline", "offline"] | _Unset | None = _UNSET,
        instructions: str | _Unset | None = _UNSET,
        restrictions: list[
            Literal[
                "registration", "agreement", "data_fee", "transfer_fee", "membership", "approval"
            ]
        ]
        | _Unset
        | None = _UNSET,
        retrieval_time: str | _Unset | None = _UNSET,
        type: Literal["open", "embargoed", "restricted", "closed"] | _Unset | None = _UNSET,
    ) -> None:
        """Update supplied members; omitted values are preserved and None removes."""
        self._apply(
            {
                "availability": availability,
                "instructions": instructions,
                "restrictions": restrictions,
                "retrieval_time": retrieval_time,
                "type": type,
            }
        )

    @property
    def availability(self) -> Literal["online", "nearline", "offline"] | None:
        "access:availability"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast(
            "Literal['online', 'nearline', 'offline'] | None",
            self.properties.get("access:availability"),
        )

    @availability.setter
    def availability(self, value: Literal["online", "nearline", "offline"] | None) -> None:
        if value is None:
            self.properties.pop("access:availability", None)
        else:
            self.properties["access:availability"] = _encode(value)

    @property
    def instructions(self) -> str | None:
        "access:instructions"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast("str | None", self.properties.get("access:instructions"))

    @instructions.setter
    def instructions(self, value: str | None) -> None:
        if value is None:
            self.properties.pop("access:instructions", None)
        else:
            self.properties["access:instructions"] = _encode(value)

    @property
    def restrictions(
        self,
    ) -> (
        list[
            Literal[
                "registration", "agreement", "data_fee", "transfer_fee", "membership", "approval"
            ]
        ]
        | None
    ):
        "access:restrictions"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast(
            "list[Literal['registration', 'agreement', 'data_fee', 'transfer_fee', 'membership', 'approval']] | None",
            self.properties.get("access:restrictions"),
        )

    @restrictions.setter
    def restrictions(
        self,
        value: list[
            Literal[
                "registration", "agreement", "data_fee", "transfer_fee", "membership", "approval"
            ]
        ]
        | None,
    ) -> None:
        if value is None:
            self.properties.pop("access:restrictions", None)
        else:
            self.properties["access:restrictions"] = _encode(value)

    @property
    def retrieval_time(self) -> str | None:
        "access:retrieval_time"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast("str | None", self.properties.get("access:retrieval_time"))

    @retrieval_time.setter
    def retrieval_time(self, value: str | None) -> None:
        if value is None:
            self.properties.pop("access:retrieval_time", None)
        else:
            self.properties["access:retrieval_time"] = _encode(value)

    @property
    def type(self) -> Literal["open", "embargoed", "restricted", "closed"] | None:
        "access:type"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast(
            "Literal['open', 'embargoed', 'restricted', 'closed'] | None",
            self.properties.get("access:type"),
        )

    @type.setter
    def type(self, value: Literal["open", "embargoed", "restricted", "closed"] | None) -> None:
        if value is None:
            self.properties.pop("access:type", None)
        else:
            self.properties["access:type"] = _encode(value)


class AssetFields(_Object):
    """Generated nested value object; unknown JSON members are preserved."""

    _members: ClassVar[dict[str, str]] = {
        "availability": "access:availability",
        "instructions": "access:instructions",
        "restrictions": "access:restrictions",
        "retrieval_time": "access:retrieval_time",
        "type": "access:type",
        "alternate": "alternate",
    }

    @classmethod
    def create(
        cls,
        *,
        availability: Literal["online", "nearline", "offline"] | _Unset = _UNSET,
        instructions: str | _Unset = _UNSET,
        restrictions: list[
            Literal[
                "registration", "agreement", "data_fee", "transfer_fee", "membership", "approval"
            ]
        ]
        | _Unset = _UNSET,
        retrieval_time: str | _Unset = _UNSET,
        type: Literal["open", "embargoed", "restricted", "closed"] | _Unset = _UNSET,
        alternate: dict[str, Alternate] | _Unset = _UNSET,
    ) -> AssetFields:
        """Create with typed members; omitted optionals are not written.

        Explicit None writes null. Validate the STAC object to check value constraints.
        """
        _values = {
            "access:availability": availability,
            "access:instructions": instructions,
            "access:restrictions": restrictions,
            "access:retrieval_time": retrieval_time,
            "access:type": type,
            "alternate": alternate,
        }
        return cls(
            {key: _encode(value) for key, value in _values.items() if not isinstance(value, _Unset)}
        )

    def apply(
        self,
        *,
        availability: Literal["online", "nearline", "offline"] | _Unset | None = _UNSET,
        instructions: str | _Unset | None = _UNSET,
        restrictions: list[
            Literal[
                "registration", "agreement", "data_fee", "transfer_fee", "membership", "approval"
            ]
        ]
        | _Unset
        | None = _UNSET,
        retrieval_time: str | _Unset | None = _UNSET,
        type: Literal["open", "embargoed", "restricted", "closed"] | _Unset | None = _UNSET,
        alternate: dict[str, Alternate] | _Unset | None = _UNSET,
    ) -> None:
        """Update supplied members; omitted values are preserved and None removes."""
        self._apply(
            {
                "availability": availability,
                "instructions": instructions,
                "restrictions": restrictions,
                "retrieval_time": retrieval_time,
                "type": type,
                "alternate": alternate,
            }
        )

    @property
    def availability(self) -> Literal["online", "nearline", "offline"] | None:
        "access:availability"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast(
            "Literal['online', 'nearline', 'offline'] | None",
            self.properties.get("access:availability"),
        )

    @availability.setter
    def availability(self, value: Literal["online", "nearline", "offline"] | None) -> None:
        if value is None:
            self.properties.pop("access:availability", None)
        else:
            self.properties["access:availability"] = _encode(value)

    @property
    def instructions(self) -> str | None:
        "access:instructions"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast("str | None", self.properties.get("access:instructions"))

    @instructions.setter
    def instructions(self, value: str | None) -> None:
        if value is None:
            self.properties.pop("access:instructions", None)
        else:
            self.properties["access:instructions"] = _encode(value)

    @property
    def restrictions(
        self,
    ) -> (
        list[
            Literal[
                "registration", "agreement", "data_fee", "transfer_fee", "membership", "approval"
            ]
        ]
        | None
    ):
        "access:restrictions"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast(
            "list[Literal['registration', 'agreement', 'data_fee', 'transfer_fee', 'membership', 'approval']] | None",
            self.properties.get("access:restrictions"),
        )

    @restrictions.setter
    def restrictions(
        self,
        value: list[
            Literal[
                "registration", "agreement", "data_fee", "transfer_fee", "membership", "approval"
            ]
        ]
        | None,
    ) -> None:
        if value is None:
            self.properties.pop("access:restrictions", None)
        else:
            self.properties["access:restrictions"] = _encode(value)

    @property
    def retrieval_time(self) -> str | None:
        "access:retrieval_time"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast("str | None", self.properties.get("access:retrieval_time"))

    @retrieval_time.setter
    def retrieval_time(self, value: str | None) -> None:
        if value is None:
            self.properties.pop("access:retrieval_time", None)
        else:
            self.properties["access:retrieval_time"] = _encode(value)

    @property
    def type(self) -> Literal["open", "embargoed", "restricted", "closed"] | None:
        "access:type"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast(
            "Literal['open', 'embargoed', 'restricted', 'closed'] | None",
            self.properties.get("access:type"),
        )

    @type.setter
    def type(self, value: Literal["open", "embargoed", "restricted", "closed"] | None) -> None:
        if value is None:
            self.properties.pop("access:type", None)
        else:
            self.properties["access:type"] = _encode(value)

    @property
    def alternate(self) -> dict[str, Alternate] | None:
        "alternate"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast(
            "dict[str, Alternate] | None",
            _decode(self.properties.get("alternate"), ["map", ["object", "Alternate"]]),
        )

    @alternate.setter
    def alternate(self, value: dict[str, Alternate] | None) -> None:
        if value is None:
            self.properties.pop("alternate", None)
        else:
            self.properties["alternate"] = _encode(value)


_MODELS: dict[str, type[_Object]] = {
    "Alternate": Alternate,
    "AssetFields": AssetFields,
}


class AccessExtension(
    PropertiesExtension,
    ExtensionManagementMixin[pystac.Item | pystac.Collection | pystac.Catalog],
    Generic[T],
):
    """Typed property wrapper; use ext() to check/register the extension.

    Setters preserve JSON representations, including date/time strings and nested
    dictionaries. None removes a property; set_null() explicitly writes JSON null.
    Validate the owning STAC object to enforce full schema constraints.
    """

    def __init__(self, obj: T, target: str) -> None:
        """Bind a schema-supported STAC object's metadata for live updates."""
        self.obj: T = obj
        self._target = target
        self.additional_read_properties: list[dict[str, Any]] | None = None
        if isinstance(obj, (pystac.Item, pystac.ItemAssetDefinition)):
            self.properties = obj.properties
        else:
            self.properties = obj.extra_fields
        if isinstance(obj, pystac.Asset) and isinstance(obj.owner, pystac.Item):
            self.additional_read_properties = [obj.owner.properties]

    @classmethod
    def get_schema_uri(cls) -> str:
        """The canonical schema identifier used for extension registration."""
        return SCHEMA_URI

    @classmethod
    def has_extension(cls, obj: pystac.STACObject) -> bool:
        """Check this exact schema version; migrations are not generated."""
        return SCHEMA_URI in (obj.stac_extensions or [])

    @classmethod
    def ext(cls, obj: T, add_if_missing: bool = False) -> AccessExtension[T]:
        """Wrap a schema-supported object and optionally register its extension."""
        target = _target_for(obj)
        if isinstance(obj, (pystac.Asset, pystac.ItemAssetDefinition, pystac.Link)):
            cls.ensure_owner_has_extension(obj, add_if_missing)
        else:
            cls.ensure_has_extension(obj, add_if_missing)
        return cls(obj, target)

    def _check_field(self, key: str) -> None:
        if self._target not in FIELD_TARGETS[key]:
            raise pystac.ExtensionTypeError(f"{key} does not apply to {self._target}")

    def clear(self, name: str) -> None:
        """Remove a field using its generated Python attribute name."""
        key = FIELD_NAMES[name]
        self._check_field(key)
        self.properties.pop(key, None)

    def set_null(self, name: str) -> None:
        """Write explicit JSON null; schema validation checks whether it is permitted."""
        key = FIELD_NAMES[name]
        self._check_field(key)
        self._set_property(key, None, pop_if_none=False)

    def apply(self, **values: Any) -> None:
        """Update only supplied fields; omitted fields are preserved.

        Keys are generated Python attribute names. Unknown or inapplicable fields
        are rejected before mutation. Validate the STAC object to check values afterwards.
        """
        for name in values:
            if name not in FIELD_NAMES:
                raise TypeError(f"Unknown extension field: {name}")
            self._check_field(FIELD_NAMES[name])
        for name, value in values.items():
            setattr(self, name, value)

    @property
    def availability(self) -> Literal["online", "nearline", "offline"] | None:
        "access:availability"
        self._check_field("access:availability")
        if "access:availability" in self.properties:
            return cast(
                "Literal['online', 'nearline', 'offline'] | None",
                self.properties["access:availability"],
            )
        return cast(
            "Literal['online', 'nearline', 'offline'] | None",
            self._get_property("access:availability", object),
        )

    @availability.setter
    def availability(self, value: Literal["online", "nearline", "offline"] | None) -> None:
        self._check_field("access:availability")
        self._set_property("access:availability", _encode(value))

    @property
    def instructions(self) -> str | None:
        "access:instructions"
        self._check_field("access:instructions")
        if "access:instructions" in self.properties:
            return cast("str | None", self.properties["access:instructions"])
        return cast("str | None", self._get_property("access:instructions", object))

    @instructions.setter
    def instructions(self, value: str | None) -> None:
        self._check_field("access:instructions")
        self._set_property("access:instructions", _encode(value))

    @property
    def restrictions(
        self,
    ) -> (
        list[
            Literal[
                "registration", "agreement", "data_fee", "transfer_fee", "membership", "approval"
            ]
        ]
        | None
    ):
        "access:restrictions"
        self._check_field("access:restrictions")
        if "access:restrictions" in self.properties:
            return cast(
                "list[Literal['registration', 'agreement', 'data_fee', 'transfer_fee', 'membership', 'approval']] | None",
                self.properties["access:restrictions"],
            )
        return cast(
            "list[Literal['registration', 'agreement', 'data_fee', 'transfer_fee', 'membership', 'approval']] | None",
            self._get_property("access:restrictions", object),
        )

    @restrictions.setter
    def restrictions(
        self,
        value: list[
            Literal[
                "registration", "agreement", "data_fee", "transfer_fee", "membership", "approval"
            ]
        ]
        | None,
    ) -> None:
        self._check_field("access:restrictions")
        self._set_property("access:restrictions", _encode(value))

    @property
    def retrieval_time(self) -> str | None:
        "access:retrieval_time"
        self._check_field("access:retrieval_time")
        if "access:retrieval_time" in self.properties:
            return cast("str | None", self.properties["access:retrieval_time"])
        return cast("str | None", self._get_property("access:retrieval_time", object))

    @retrieval_time.setter
    def retrieval_time(self, value: str | None) -> None:
        self._check_field("access:retrieval_time")
        self._set_property("access:retrieval_time", _encode(value))

    @property
    def type(
        self,
    ) -> Literal["open", "embargoed", "restricted", "closed"] | Literal["restricted"] | None:
        "access:type"
        self._check_field("access:type")
        if "access:type" in self.properties:
            return cast(
                "Literal['open', 'embargoed', 'restricted', 'closed'] | Literal['restricted'] | None",
                self.properties["access:type"],
            )
        return cast(
            "Literal['open', 'embargoed', 'restricted', 'closed'] | Literal['restricted'] | None",
            self._get_property("access:type", object),
        )

    @type.setter
    def type(
        self,
        value: Literal["open", "embargoed", "restricted", "closed"] | Literal["restricted"] | None,
    ) -> None:
        self._check_field("access:type")
        self._set_property("access:type", _encode(value))

    @property
    def alternate(self) -> dict[str, Alternate] | None:
        "alternate"
        self._check_field("alternate")
        if "alternate" in self.properties:
            return cast(
                "dict[str, Alternate] | None",
                _decode(self.properties["alternate"], ["map", ["object", "Alternate"]]),
            )
        return cast(
            "dict[str, Alternate] | None",
            _decode(self._get_property("alternate", object), ["map", ["object", "Alternate"]]),
        )

    @alternate.setter
    def alternate(self, value: dict[str, Alternate] | None) -> None:
        self._check_field("alternate")
        self._set_property("alternate", _encode(value))

    @property
    def assetTemplates(self) -> dict[str, AssetFields] | None:
        "assetTemplates"
        self._check_field("assetTemplates")
        if "assetTemplates" in self.properties:
            return cast(
                "dict[str, AssetFields] | None",
                _decode(self.properties["assetTemplates"], ["map", ["object", "AssetFields"]]),
            )
        return cast(
            "dict[str, AssetFields] | None",
            _decode(
                self._get_property("assetTemplates", object), ["map", ["object", "AssetFields"]]
            ),
        )

    @assetTemplates.setter
    def assetTemplates(self, value: dict[str, AssetFields] | None) -> None:
        self._check_field("assetTemplates")
        self._set_property("assetTemplates", _encode(value))

    @property
    def linkTemplates(self) -> list[Alternate] | None:
        "linkTemplates"
        self._check_field("linkTemplates")
        if "linkTemplates" in self.properties:
            return cast(
                "list[Alternate] | None",
                _decode(self.properties["linkTemplates"], ["list", ["object", "Alternate"]]),
            )
        return cast(
            "list[Alternate] | None",
            _decode(self._get_property("linkTemplates", object), ["list", ["object", "Alternate"]]),
        )

    @linkTemplates.setter
    def linkTemplates(self, value: list[Alternate] | None) -> None:
        self._check_field("linkTemplates")
        self._set_property("linkTemplates", _encode(value))

    @classmethod
    def summaries(
        cls, obj: pystac.Collection, add_if_missing: bool = False
    ) -> SummariesAccessExtension:
        """Wrap schema-declared Collection summaries and optionally register the extension."""
        if not isinstance(obj, pystac.Collection):
            raise pystac.ExtensionTypeError("Summaries require a Collection")
        cls.ensure_has_extension(obj, add_if_missing)
        return SummariesAccessExtension(obj)


class SummariesAccessExtension(SummariesExtension):
    """Collection summaries; ranges, lists and JSON Schema objects are preserved."""

    @property
    def availability(self) -> list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None:
        value = self.summaries.to_dict().get("access:availability")
        if isinstance(value, dict) and "minimum" in value and "maximum" in value:
            return self.summaries.get_range("access:availability")
        return value

    @availability.setter
    def availability(
        self, value: list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None
    ) -> None:
        self.summaries.remove("access:availability")
        self._set_summary("access:availability", value)

    @property
    def instructions(self) -> list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None:
        value = self.summaries.to_dict().get("access:instructions")
        if isinstance(value, dict) and "minimum" in value and "maximum" in value:
            return self.summaries.get_range("access:instructions")
        return value

    @instructions.setter
    def instructions(
        self, value: list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None
    ) -> None:
        self.summaries.remove("access:instructions")
        self._set_summary("access:instructions", value)

    @property
    def restrictions(self) -> list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None:
        value = self.summaries.to_dict().get("access:restrictions")
        if isinstance(value, dict) and "minimum" in value and "maximum" in value:
            return self.summaries.get_range("access:restrictions")
        return value

    @restrictions.setter
    def restrictions(
        self, value: list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None
    ) -> None:
        self.summaries.remove("access:restrictions")
        self._set_summary("access:restrictions", value)

    @property
    def retrieval_time(self) -> list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None:
        value = self.summaries.to_dict().get("access:retrieval_time")
        if isinstance(value, dict) and "minimum" in value and "maximum" in value:
            return self.summaries.get_range("access:retrieval_time")
        return value

    @retrieval_time.setter
    def retrieval_time(
        self, value: list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None
    ) -> None:
        self.summaries.remove("access:retrieval_time")
        self._set_summary("access:retrieval_time", value)

    @property
    def type(self) -> list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None:
        value = self.summaries.to_dict().get("access:type")
        if isinstance(value, dict) and "minimum" in value and "maximum" in value:
            return self.summaries.get_range("access:type")
        return value

    @type.setter
    def type(self, value: list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None) -> None:
        self.summaries.remove("access:type")
        self._set_summary("access:type", value)
