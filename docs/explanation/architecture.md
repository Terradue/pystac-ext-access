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

# Scope, architecture, and validation

## Access conditions and availability

The upstream specification separates [access barriers](https://github.com/stac-extensions/access#accesstype) from [availability](https://github.com/stac-extensions/access#accessavailability). A dataset may require approval yet be ready to download, or be open to everyone but need retrieval first.

Availability describes the client's workflow, rather than the storage technology:

| Value | What the client needs to do |
| --- | --- |
| `online` | Download the data directly. |
| `nearline` | Request the download and wait while that request triggers retrieval; no separate order is needed. |
| `offline` | Explicitly initiate retrieval, for example through an order, before downloading. |

`access:retrieval_time` estimates the wait for nearline or offline data. The specification says to ignore it for online data.

## How Access fits with other STAC metadata

The [upstream guidance](https://github.com/stac-extensions/access#relationship-with-other-extensions) distinguishes several responsibilities:

- **Access** describes eligibility, barriers, instructions, and availability.
- **Authentication** describes the technical authentication process, such as token endpoints and OAuth flows.
- **Order** describes a transaction, such as retrieving an offline product.
- **License** describes permitted uses of the data after access is obtained; it does not replace access conditions.

For example, registration instructions belong in Access metadata, while the protocol for obtaining a token belongs in the Authentication extension. Links can direct users to registration, access-request, payment, or terms-of-service pages using the specification's [relation types](https://github.com/stac-extensions/access#relation-types).

## Package structure

The distribution is named `pystac-ext-access`, while the import path is `pystac.extensions.access`. The package shares PySTAC's extension namespace.

`AccessExtension.ext()` wraps a Catalog, Collection, Item, Asset, ItemAssetDefinition, or Link. `AccessExtension.summaries()` wraps Collection summaries. These wrappers update the original objects, which serialize through PySTAC's normal `to_dict()` method.

## Metadata storage

| Object | Storage |
| --- | --- |
| Item | `properties` |
| Catalog or Collection | `extra_fields`, serialized at the top level |
| Asset or Link | `extra_fields` |
| ItemAssetDefinition | `properties` |
| Collection summaries | `summaries` |

Assets belonging to an Item fall back to the Item's properties when an access field is missing locally. Setters and removal operations change only the asset. Other wrappers do not inherit access fields from their owners or parent catalogs.

Nested `Alternate` and `AssetFields` values preserve JSON members and provide live wrappers over stored dictionaries. They do not resolve URLs or expand templates.

## Validation boundaries

The wrapper checks supported targets and field names. Type annotations help callers choose values, but setters do not enforce the complete schema. Neither `apply()` nor `to_dict()` validates the resulting STAC document. `apply()` checks names and target compatibility first, then assigns fields; it is not a transactional validation API.

For full STAC and extension validation, install PySTAC's validation extra:

```bash
python -m pip install "pystac[validation]>=1,<2"
```

Then call `item.validate()` or `collection.validate()` on a complete STAC object. Validation can retrieve remote schemas, so their URLs must be reachable or supplied through an application-configured validator. For explicit `jsonschema` validation, enable a `FormatChecker` with duration support to check `access:retrieval_time`.

The repository's schema integrity tests run offline against `tests/data/access-schema.json`, copied from the upstream `main` branch. They check Draft 7 schema validity, the extension identifier, valid and invalid field values, nested locations, summaries, and extension serialization. They validate the Access contract alone, rather than the full STAC core schema, and do not detect later upstream changes until the snapshot is refreshed.

## Schema versions and generated code

The extension registers `https://stac-extensions.github.io/access/v0.1.0/schema.json`. `has_extension()` checks for that exact identifier. The module provides no migration hooks for older or alternative identifiers.

The Python implementation is generated. Schema-derived changes belong in the authoritative schema and generation workflow; generated classes should not be edited by hand. The field reference documents the currently generated API, including target restrictions and camelCase template properties.

Access metadata describes availability and conditions of access. Authentication, authorization, payments, and data retrieval remain the responsibility of the application and data provider.
