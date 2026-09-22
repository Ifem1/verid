# Verid reviewer guide

1. Confirm exactly one `class Verid(gl.Contract)`.
2. Confirm Studionet `61999` and reject any non-Studionet network.
3. Run `npm ci && npm run check && npm run contract:check`.
4. Review `docs/CONSENSUS.md`, `docs/SECURITY.md`, and `docs/CONTRACT_SURFACE.md`.
5. Verify no fake chain/product state or browser authorization.
6. The current release runs GenVM lint, the real Direct Mode suite, preflight and frontend checks. Schema generation is attempted in CI; local Windows SDK extraction may be unavailable when the cached GenVM artifact is locked.

Landing receipt/gate examples are explicitly illustrative and are not live evidence.
