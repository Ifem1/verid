# Verid reviewer guide

1. Confirm exactly one `class Verid(gl.Contract)`.
2. Confirm Studionet `61999` and reject any non-Studionet network.
3. Run `npm ci && npm run check && npm run contract:check`.
4. Review `docs/CONSENSUS.md`, `docs/SECURITY.md`, and `docs/CONTRACT_SURFACE.md`.
5. Verify no fake chain/product state or browser authorization.
6. Final Linux CI `35787515861` passed GenVM lint, GenVM validation, schema generation, the real Direct Mode suite, preflight, and frontend checks.

Landing receipt/gate examples are explicitly illustrative and are not live evidence.

## Final closure evidence

- Final source commit: `281ff29a2585adeb4d9294bb8b5c678053a9a7b0`
- Final source: 19,691 bytes; Git blob `e4986586e37a5c1c616a1da5a9a391dc263f13d0`; SHA-256 `7b1d2087745582eb15ac8acf844a2028d849d5100ef199bcbd6b8a9ad721c0de`
- Final Studionet 61999 contract: `0x12f2136e0d372038E72Beb54511c72fF372c694d`
- Deployment transaction: `0xd2d9c0b20927fb006cd2b2ad340220140cfaffa59d7dc16d6dee97372546e818`; finalized with `MAJORITY_AGREE`; authoritative execution-result certification is recorded as UNKNOWN because the receipt omits the top-level execution result.
- Deployed source was retrieved through `gen_getContractCode`, base64-decoded, and compared byte-for-byte: 19,691 bytes, SHA-256 `7b1d2087745582eb15ac8acf844a2028d849d5100ef199bcbd6b8a9ad721c0de`, Git blob `e4986586e37a5c1c616a1da5a9a391dc263f13d0`; exact parity.
- Direct Mode: 18/18 passing. Frontend tests: 15/15 passing. Production build and preflight pass. Final Linux CI `35787515861` passed GenVM lint, validation, and schema generation.
- Frontend production deployment: `https://verid-sigma.vercel.app`.
- Prior live semantic-path evidence from the superseded deployment: profile creation `0x0df6d45b59da1b774f533b6a0d12fa39032b55c6893de5c3c31bc5ea1d0192b7`; challenge issuance `0x8aba05d70dcf02ebbbc7a9c3a52a7862020daf5e24cf491ff2135a06f2e37aea`; surface registration `0xb87e77f5ffb562da08631a4189c6f22f4a6d7fa351c3c65b6de3cd53087e6a6a`; semantic verification `0xeb5a8d54133e05679cf29fab093eadcde41f6673f5161e311c6a940e3559fe68`.
- That superseded-deployment run exercised profile creation, challenge issuance, surface registration, and semantic verification live. Its semantic readback was `UNVERIFIED` with `identity_relation=UNRESOLVED` and `authenticity=UNRESOLVED`. No proof, gate membership, or room access success is claimed from that run. The current parity-correct contract preserves the same reviewed logic and is covered by the 18/18 Direct Mode suite.
