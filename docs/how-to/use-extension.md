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

# Work with access metadata

The first examples continue from the Item created in the [tutorial](../tutorials/first-steps.md).

## Update or remove fields

```python
access = AccessExtension.ext(item)
access.apply(availability="online", retrieval_time=None)
assert access.type == "restricted"
assert "access:retrieval_time" not in item.properties

access.instructions = "Register, then download the dataset."
access.clear("instructions")
assert "access:instructions" not in item.properties
```

`ext(item)` requires the extension to be declared already. Use `add_if_missing=True` when first attaching it. `apply()` changes only supplied fields; assigning `None` removes a field. `clear()` takes the Python property name, such as `retrieval_time`, rather than the STAC field name.

Removing restrictions while keeping `type="restricted"` produces invalid metadata. Setters do not enforce this relationship; validate the resulting document.

## Read and override asset fields

```python
asset = pystac.Asset(href="https://example.org/data.tif", media_type="image/tiff")
item.add_asset("data", asset)
asset_access = AccessExtension.ext(asset)
assert asset_access.availability == "online"
asset_access.availability = "offline"
assert asset.extra_fields["access:availability"] == "offline"
assert access.availability == "online"

asset_access.availability = None
assert asset_access.availability == "online"
```

Attach an asset to its owner before wrapping it. An Item asset reads missing fields from the Item's properties; writes affect the asset only. Removing an override exposes the Item value again. Collection assets have no corresponding fallback.

## Describe alternate access

```python
from pystac.extensions.access import Alternate

asset_access.alternate = {
    "mirror": Alternate.from_dict({
        "href": "https://mirror.example.org/data.tif",
        "access:type": "open",
        "access:availability": "online",
    })
}
assert asset.extra_fields["alternate"]["mirror"]["access:type"] == "open"
```

`Alternate.create()` builds typed access fields. `from_dict()` also preserves other members such as `href`. Describing an alternate does not download it.

## Extend a Collection and its item asset definitions

This example is independent of the Item above:

```python
import pystac
from pystac.extensions.access import AccessExtension

collection = pystac.Collection(
    id="example-collection",
    description="Example collection with registration requirements",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent([[-180, -90, 180, 90]]),
        temporal=pystac.TemporalExtent([[None, None]]),
    ),
)
collection_access = AccessExtension.ext(collection, add_if_missing=True)
collection_access.apply(type="restricted", restrictions=["registration"])

collection.item_assets = {
    "data": pystac.ItemAssetDefinition({"type": "image/tiff", "roles": ["data"]})
}
definition = collection.item_assets["data"]
definition_access = AccessExtension.ext(definition)
definition_access.availability = "nearline"
```

Catalogs use the same `AccessExtension.ext(catalog, add_if_missing=True)` entry point. Catalog and Collection access fields are stored at the top level of their serialized documents.

## Describe links and templates

Continue with the Collection above:

```python
from pystac.extensions.access import Alternate, AssetFields

link = pystac.Link(rel="enclosure", target="https://example.org/download")
collection.add_link(link)
AccessExtension.ext(link).apply(type="restricted", restrictions=["agreement"])

collection_access.assetTemplates = {
    "data": AssetFields.create(availability="nearline", retrieval_time="PT1H")
}
collection_access.linkTemplates = [Alternate.create(type="open")]
```

Attach a Link to an owner before extending it. `assetTemplates` and `linkTemplates` retain their schema-defined camelCase names in the Python API and are supported on Catalogs and Collections. These helpers store metadata; they do not expand templates into assets or links.

## Set Collection summaries

```python
summaries = AccessExtension.summaries(collection)
summaries.type = ["open", "restricted"]
summaries.availability = ["online", "nearline"]
summaries.retrieval_time = pystac.RangeSummary("PT1H", "P1D")
assert collection.summaries.to_dict()["access:retrieval_time"] == {
    "minimum": "PT1H", "maximum": "P1D"
}
```

Summaries describe values across the Collection. They are separate from the Collection's own access fields. Set a summary property to `None` to remove it. See the [field reference](../reference/fields.md#collection-summaries) for supported representations.
