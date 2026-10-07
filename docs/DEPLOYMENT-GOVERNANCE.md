# Deployment governance

Source commit, build, deployment, domain binding and independent public readback are separate states.

`SOURCE_REVIEWED → TESTED → BUILD_IDENTIFIED → DEPLOYED → CANONICAL_ROUTE_OBSERVED → INDEPENDENTLY_VERIFIED`

A failure at a later stage does not erase earlier evidence, but it prevents promotion. Rollback points to a known source/build/deployment identity.
