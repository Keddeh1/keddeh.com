# DOM and interaction acceptance

`tests/dom_audit.py` parses every generated route and fails for missing landmarks/metadata, broken internal links, placeholder links, unlabeled fields, missing focus/reduced-motion treatment, missing learning-form announcements, or incomplete page directory.

`tests/runtime.test.mjs` starts the live runtime and verifies health, route readback, durable interest registration, duplicate protection, invalid-input rejection, authenticated admin overlays and resulting page readback.

Rendered-browser/assistive-technology testing remains a deployment-stage check because static parsing cannot establish visual clipping, real focus visibility, touch behaviour, timing or AT interoperability.
