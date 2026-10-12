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

# Python API

Import the extension from `pystac.extensions.access`. Use `AccessExtension.ext()` to wrap STAC objects and `AccessExtension.summaries()` for Collection summaries.

::: pystac.extensions.access
    options:
      members:
        - AccessExtension
        - Alternate
        - AssetFields
        - SummariesAccessExtension
        - SCHEMA_URI
      inherited_members:
        - from_dict
        - to_dict
        - clear
        - set_null
      show_root_heading: true
      show_signature_annotations: true
