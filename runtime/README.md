# KEDDEH Runtime Platform

This directory contains the formal runtime package for the KEDDEH.COM stack.

## Runtime layout

- `local-runtime/` — custom runtime engine, KEX/BRAINK/IL-LLM modules, mesh and signature logic
- `services/` — orchestrated service-level runtime management
- `manifest.json` — runtime manifest for build/deploy operations

## Operational intent

- custom runtime-first deployment
- no GitHub package dependency model
- resilient local execution with KEX/BRAINK/IL-LLM
- HTTPS/TCP/UDP service envelope around web and DNS stack
