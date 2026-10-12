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

# Create an Item with access metadata

Install the package using the [installation guide](../how-to/install.md). This example describes an imaginary dataset that requires registration and takes an hour to retrieve.

## Create and extend an Item

```python
from datetime import datetime, timezone

import pystac
from pystac.extensions.access import AccessExtension

item = pystac.Item(
    id="example-access",
    geometry=None,
    bbox=None,
    datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    properties={"title": "Example dataset"},
)
access = AccessExtension.ext(item, add_if_missing=True)
access.apply(
    type="restricted",
    restrictions=["registration"],
    availability="nearline",
    retrieval_time="PT1H",
    instructions="Register with the provider before requesting this dataset.",
)

assert access.type == "restricted"
assert item.properties["access:retrieval_time"] == "PT1H"
assert AccessExtension.get_schema_uri() in item.stac_extensions
```

`add_if_missing=True` registers the extension on the Item. The wrapper mutates the Item in place. `retrieval_time` is an ISO 8601 duration string; `PT1H` means one hour. The schema requires a non-empty restrictions list when `access:type` is `restricted`.

## Serialize and read back

Continue in the same Python session:

```python
import json

payload = item.to_dict()
print(json.dumps(payload, indent=2))
restored_item = pystac.Item.from_dict(payload)
restored = AccessExtension.ext(restored_item)
assert restored.restrictions == ["registration"]
assert restored.retrieval_time == "PT1H"
```

Serialization does not perform JSON Schema validation. See [validation boundaries](../explanation/architecture.md#validation-boundaries) before exporting documents.

Continue with the [how-to guide](../how-to/use-extension.md) to update fields and describe access to individual assets. `apply()` preserves fields whose arguments are omitted.
