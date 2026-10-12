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

# Access PySTAC extension

`pystac-ext-access` is a `pystac` Python implementation of the [STAC Access Extension Specification](https://github.com/stac-extensions/access), reads and writes STAC access metadata using the `access:` prefix. Describe whether data is open or restricted, what users must do to obtain it, and whether it is available immediately.

Import the API from `pystac.extensions.access`. The implementation uses the [Access v0.1.0 schema identifier](https://stac-extensions.github.io/access/v0.1.0/schema.json). The Python package version is independent of the specification version.

## Why describe access?

A dataset can be discoverable in a STAC catalog while still requiring registration, payment, or retrieval from an archive. The [upstream Access specification](https://github.com/stac-extensions/access) makes these conditions explicit so users can understand what obtaining the data involves. Access fields on Catalogs, Collections, and Items describe the data, rather than access to the STAC metadata itself.

Access conditions can differ between copies: a provider might require registration while a mirror offers a direct download. Assets and alternate assets can describe those differences. Free data that requires an account is still `restricted`; price alone does not determine whether access is `open`.

The upstream extension is currently classified as **Proposal**. See [access concepts](explanation/architecture.md#access-conditions-and-availability) for the distinction between access barriers, download availability, and related STAC metadata.

## Start here

```bash
pip install pystac-ext-access
```

- [Create an Item with access metadata](tutorials/first-steps.md).
- [Update access fields, assets, links, and Collection metadata](how-to/use-extension.md).
- [Look up field constraints](reference/fields.md) and the [Python API](reference/api.md).
- [Understand storage and validation](explanation/architecture.md).

The extension supports Catalogs, Collections, Items, Assets, ItemAssetDefinitions, and Links, plus Collection summaries. It describes access conditions; it does not authenticate users, retrieve data, or enforce access control.
