<!--
Copyright 2026 Terradue

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Access fields

The implementation targets the [Access v0.1.0 schema](https://stac-extensions.github.io/access/v0.1.0/schema.json). The repository tests preserve an upstream schema snapshot in `tests/data/access-schema.json`.

## Common fields

These fields apply to Catalogs, Collections, Items, Assets, ItemAssetDefinitions, and Links.

| STAC field | Python property | Schema constraint |
| --- | --- | --- |
| `access:type` | `type` | `open`, `embargoed`, `restricted`, or `closed`. |
| `access:restrictions` | `restrictions` | Non-empty list of unique values: `registration`, `agreement`, `data_fee`, `transfer_fee`, `membership`, or `approval`. |
| `access:instructions` | `instructions` | Non-empty string explaining how to obtain access. |
| `access:availability` | `availability` | `online`, `nearline`, or `offline`. |
| `access:retrieval_time` | `retrieval_time` | ISO 8601 duration string, for example `PT1H` or `P1D`. Requires format checking during validation. |

All common fields are optional except that `access:type="restricted"` requires `access:restrictions`. The schema rejects unknown `access:` fields but permits other namespaces. The extension inserts no default field values.

These are schema constraints, not setter checks. Python annotations describe accepted types, but setters do not enforce enums, duration syntax, or cross-field requirements at runtime.

## Nested structures

| STAC field and Python property | Python value | Supported wrapper targets |
| --- | --- | --- |
| `alternate` | `dict[str, Alternate]` | Asset, ItemAssetDefinition |
| `assetTemplates` | `dict[str, AssetFields]` | Catalog, Collection |
| `linkTemplates` | `list[Alternate]` | Catalog, Collection |

`Alternate` wraps the common access fields. `AssetFields` wraps the common fields plus `alternate`. Both support `create()`, `from_dict()`, `to_dict()`, `apply()`, `clear()`, and `set_null()`.

`from_dict()` wraps its input by reference by default; pass `copy=True` for an independent deep copy. `to_dict()` returns the live backing dictionary. Unknown members are preserved, with their validity determined by the schema. Nested objects read through extension getters also wrap the stored dictionaries.

## Updates, missing values, and null

Getters return `None` for absent fields, subject to Item asset fallback. Setting a property to `None` removes it. `apply()` preserves omitted fields and removes fields explicitly passed as `None`. Unknown or inapplicable field names are rejected before an extension `apply()` begins assigning values.

`clear("retrieval_time")` removes the stored field. `set_null("retrieval_time")` writes explicit JSON null instead. The common Access field schemas do not permit null, so this low-level operation produces metadata that fails schema validation.

## Collection summaries

`AccessExtension.summaries(collection, add_if_missing=True)` exposes the five common fields as summary properties.

Summary arrays contain the corresponding field values; `restrictions` contains individual restriction strings rather than lists of strings. The schema also allows object summaries. Retrieval-time objects validate `minimum` and `maximum` as duration strings. The summary wrapper reads objects containing both bounds as `pystac.RangeSummary` and preserves other object summaries as dictionaries.

See [working examples](../how-to/use-extension.md) and the [Python API](api.md).
