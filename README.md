# KEDDEH.COM governed frontage

Canonical GitHub source for the KEDDEH.COM public information estate and its live capture/control runtime.

This repository separates **content**, **rendering**, **static build**, **live runtime**, **evidence**, and **deployment**. A successful build is not a public deployment receipt.

## Run

```bash
npm run build
npm test
npm start
```

The live runtime adds `POST /api/interest`, `GET /api/health`, and authenticated `PATCH /api/admin/content`. No client page contains the administrator token.

Every public route states its audience, purpose, primary action, evidence boundary, and next step. Every displayed control resolves to a real route/handler or an explicit unavailable state.
