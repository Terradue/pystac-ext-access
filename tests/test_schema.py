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

"""Validate the upstream Access schema snapshot without network access.

The fixture is an unchanged copy of
https://raw.githubusercontent.com/stac-extensions/access/refs/heads/main/json-schema/schema.json.
Refresh tests/data/access-schema.json from that URL when updating the extension.
These tests validate the extension contract, not the STAC core schema.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft7Validator, FormatChecker, ValidationError

import pystac
from pystac.extensions.access import SCHEMA_URI, AccessExtension


@pytest.fixture(scope="module")
def schema() -> dict[str, object]:
    """Load the vendored upstream schema for deterministic validation."""
    schema_path = Path(__file__).parent / "data" / "access-schema.json"
    document: dict[str, object] = json.loads(schema_path.read_text(encoding="utf-8"))
    return document


@pytest.fixture(scope="module")
def validator(schema: dict[str, object]) -> Draft7Validator:
    """Enable format validation, including the schema's duration format."""
    return Draft7Validator(schema, format_checker=FormatChecker())


def test_schema_is_valid_draft7(schema: dict[str, object]) -> None:
    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    Draft7Validator.check_schema(schema)


def test_schema_identifier_matches_extension(schema: dict[str, object]) -> None:
    assert schema["$id"] == f"{SCHEMA_URI}#"
    assert AccessExtension.get_schema_uri() == SCHEMA_URI


@pytest.mark.parametrize("object_type", ["Catalog", "Collection", "Feature"])
def test_schema_accepts_supported_stac_types(validator: Draft7Validator, object_type: str) -> None:
    validator.validate({"type": object_type, "stac_extensions": [SCHEMA_URI], "properties": {}})


@pytest.mark.parametrize(
    "document",
    [
        {},
        {"type": "Catalog"},
        {"stac_extensions": [SCHEMA_URI]},
        {"type": "Catalog", "stac_extensions": []},
        {"type": "Catalog", "stac_extensions": ["https://example.com/schema.json"]},
        {"type": "Catalog", "stac_extensions": SCHEMA_URI},
        {"type": "FeatureCollection", "stac_extensions": [SCHEMA_URI]},
        {"type": "Feature", "stac_extensions": [SCHEMA_URI]},
    ],
)
def test_schema_rejects_invalid_extension_envelopes(
    validator: Draft7Validator, document: dict[str, object]
) -> None:
    with pytest.raises(ValidationError):
        validator.validate(document)


@pytest.mark.parametrize(
    "fields",
    [
        {"access:type": "open"},
        {"access:type": "embargoed"},
        {"access:type": "closed"},
        {"access:type": "restricted", "access:restrictions": ["registration"]},
        {
            "access:restrictions": [
                "agreement",
                "data_fee",
                "transfer_fee",
                "membership",
                "approval",
            ]
        },
        {"access:availability": "online"},
        {"access:availability": "nearline"},
        {"access:availability": "offline"},
        {"access:instructions": "Contact the provider."},
        {"access:retrieval_time": "PT1H"},
        {"other:field": "Additional namespaces are allowed."},
    ],
)
def test_schema_accepts_access_fields(
    validator: Draft7Validator, fields: dict[str, object]
) -> None:
    validator.validate({"type": "Catalog", "stac_extensions": [SCHEMA_URI], **fields})


@pytest.mark.parametrize(
    "fields",
    [
        {"access:type": "unknown"},
        {"access:type": None},
        {"access:type": "restricted"},
        {"access:restrictions": []},
        {"access:restrictions": ["registration", "registration"]},
        {"access:restrictions": ["unknown"]},
        {"access:restrictions": "registration"},
        {"access:availability": "unknown"},
        {"access:instructions": ""},
        {"access:instructions": 42},
        {"access:retrieval_time": "tomorrow"},
        {"access:retrieval_time": 42},
        {"access:unknown": "Unexpected access fields are forbidden."},
    ],
)
@pytest.mark.parametrize(
    "location",
    [
        "catalog",
        "collection",
        "item",
        "asset",
        "alternate",
        "item_asset",
        "asset_template",
        "link",
        "link_template",
    ],
)
def test_schema_rejects_invalid_fields_at_each_location(
    validator: Draft7Validator, fields: dict[str, object], location: str
) -> None:
    document: dict[str, object] = {"type": "Collection", "stac_extensions": [SCHEMA_URI]}
    placements: dict[str, dict[str, object]] = {
        "catalog": {"type": "Catalog", **fields},
        "collection": fields,
        "item": {"type": "Feature", "properties": fields},
        "asset": {"assets": {"data": fields}},
        "alternate": {"assets": {"data": {"alternate": {"mirror": fields}}}},
        "item_asset": {"item_assets": {"data": fields}},
        "asset_template": {"assetTemplates": {"data": fields}},
        "link": {"links": [fields]},
        "link_template": {"linkTemplates": [fields]},
    }
    document.update(placements[location])
    with pytest.raises(ValidationError):
        validator.validate(document)


def test_schema_accepts_nested_access_fields(validator: Draft7Validator) -> None:
    fields = {"access:type": "restricted", "access:restrictions": ["approval"]}
    validator.validate(
        {
            "type": "Collection",
            "stac_extensions": [SCHEMA_URI],
            "assets": {"data": {**fields, "alternate": {"mirror": fields}}},
            "item_assets": {"data": fields},
            "assetTemplates": {"data": fields},
            "links": [fields],
            "linkTemplates": [fields],
        }
    )


@pytest.mark.parametrize(
    ("summaries", "valid"),
    [
        ({"access:type": ["open", "restricted"]}, True),
        ({"access:restrictions": ["registration", "approval"]}, True),
        ({"access:instructions": ["Contact provider."]}, True),
        ({"access:availability": ["online", "offline"]}, True),
        ({"access:retrieval_time": ["PT1H", "P1D"]}, True),
        ({"access:retrieval_time": {"minimum": "PT1H", "maximum": "P1D"}}, True),
        ({"access:type": {"type": "string"}}, True),
        ({"access:type": ["unknown"]}, False),
        ({"access:restrictions": ["unknown"]}, False),
        ({"access:instructions": [""]}, False),
        ({"access:availability": ["unknown"]}, False),
        ({"access:retrieval_time": ["tomorrow"]}, False),
        ({"access:retrieval_time": {"minimum": "tomorrow"}}, False),
        ({"access:retrieval_time": {"maximum": "tomorrow"}}, False),
        ({"access:unknown": []}, False),
    ],
)
def test_schema_validates_collection_summaries(
    validator: Draft7Validator, summaries: dict[str, object], valid: bool
) -> None:
    document = {"type": "Collection", "stac_extensions": [SCHEMA_URI], "summaries": summaries}
    assert validator.is_valid(document) is valid


def test_extension_serializes_schema_valid_access_fields(validator: Draft7Validator) -> None:
    catalog = pystac.Catalog("example", "Example catalog")
    extension = AccessExtension.ext(catalog, add_if_missing=True)
    extension.type = "restricted"
    extension.restrictions = ["registration"]
    extension.availability = "nearline"
    extension.instructions = "Register with the provider."
    extension.retrieval_time = "PT1H"

    validator.validate(catalog.to_dict())
