# Verid reviewer guide

1. Confirm exactly one `class Verid(gl.Contract)`.
2. Confirm Studionet `61999`; reject `61997` / `studio-dev`.
3. Run `npm ci && npm run check && npm run contract:check`.
4. Review `docs/CONSENSUS.md`, `docs/SECURITY.md`, and `docs/CONTRACT_SURFACE.md`.
5. Verify no fake chain/product state or browser authorization.
6. Final Codex pass should run GenVM lint, Direct Mode/preflight where available, adversarial semantic review, deploy exact reviewed bytes, and verify deployment parity/live lifecycle.

Landing receipt/gate examples are explicitly illustrative and are not live evidence.
