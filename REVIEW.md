# Verid reviewer guide

1. Confirm exactly one `class Verid(gl.Contract)`.
2. Confirm Studionet `61999` and reject any non-Studionet network.
3. Run `npm ci && npm run check && npm run contract:check`.
4. Review `docs/CONSENSUS.md`, `docs/SECURITY.md`, and `docs/CONTRACT_SURFACE.md`.
5. Verify no fake chain/product state or browser authorization.
6. Final Linux CI `35787515861` passed GenVM lint, GenVM validation, schema generation, the real Direct Mode suite, preflight, and frontend checks.

Landing receipt/gate examples are explicitly illustrative and are not live evidence.

## Final closure evidence

- Final source commit: `5d0009502b7f39a05fc15a7b8b9f5577d3dbd895`
- Final source: 20,134 bytes; Git blob `e13006fbd5b584726d4dbfb5b33a7b3f13d86ae3`; SHA-256 `caca027a0253142bee2f5793a508c76b645907b61815ca9c626345caf22184c4`
- Final Studionet 61999 contract: `0x4A430f7326DEdcd796df149Ce5d31223c5943d92`
- Deployment transaction: `0x3ea54a4abee79a9da8a3c973c04779ad5912572c72ec67ff6c2124e34d09d479`; finalized with `MAJORITY_AGREE`; authoritative execution-result certification is recorded as UNKNOWN because the receipt omits the top-level execution result.
- Deployed source was retrieved through `gen_getContractCode`, base64-decoded, and compared byte-for-byte: 20,134 bytes, SHA-256 `caca027a0253142bee2f5793a508c76b645907b61815ca9c626345caf22184c4`, Git blob `e13006fbd5b584726d4dbfb5b33a7b3f13d86ae3`; exact parity.
- Direct Mode: 22/22 passing. Frontend tests: 15/15 passing. Production build and preflight pass. Final Linux CI confirms GenVM lint, validation, and schema generation.

### Steward fix

Proof tiers derive from exactly the fresh evidence set stored in each proof, so omitted stale evidence cannot elevate a tier. GitHub, GitHub Pages, and GitHubusercontent hosts are one shared control plane for STRONG independence. Focused Direct Mode regressions cover both invariants: the staggered fresh/stale evidence regression and the shared GitHub control-plane regression.
- Frontend production deployment: `https://verid-sigma.vercel.app`.
- Prior live semantic-path evidence from the superseded deployment: profile creation `0x0df6d45b59da1b774f533b6a0d12fa39032b55c6893de5c3c31bc5ea1d0192b7`; challenge issuance `0x8aba05d70dcf02ebbbc7a9c3a52a7862020daf5e24cf491ff2135a06f2e37aea`; surface registration `0xb87e77f5ffb562da08631a4189c6f22f4a6d7fa351c3c65b6de3cd53087e6a6a`; semantic verification `0xeb5a8d54133e05679cf29fab093eadcde41f6673f5161e311c6a940e3559fe68`.
- That superseded-deployment run exercised profile creation, challenge issuance, surface registration, and semantic verification live. Its semantic readback was `UNVERIFIED` with `identity_relation=UNRESOLVED` and `authenticity=UNRESOLVED`. No proof, gate membership, or room access success is claimed from that run. The current parity-correct contract preserves the same reviewed logic and is covered by the 22/22 Direct Mode suite.
