# Verid reviewer guide

1. Confirm exactly one `class Verid(gl.Contract)`.
2. Confirm Studionet `61999` and reject any non-Studionet network.
3. Run `npm ci && npm run check && npm run contract:check`.
4. Review `docs/CONSENSUS.md`, `docs/SECURITY.md`, and `docs/CONTRACT_SURFACE.md`.
5. Verify no fake chain/product state or browser authorization.
6. The current release runs GenVM lint, the real Direct Mode suite, preflight and frontend checks. Schema generation is attempted in CI; local Windows SDK extraction may be unavailable when the cached GenVM artifact is locked.

Landing receipt/gate examples are explicitly illustrative and are not live evidence.

## Final closure evidence

- Final source commit: `281ff29a2585adeb4d9294bb8b5c678053a9a7b0`
- Final source: 20,018 bytes; SHA-256 `240abb1f32bb5e65196133792f1b7f9ac5f143912957895adf1b98ccae493246`
- Final Studionet 61999 contract: `0xeE4Df291A9e8B4f5b2B90b3F6eeAe578818E0B0B`
- Deployment transaction: `0xf42e4c8876ed300b59cc96ca87e6822b7e622f90eab57564e323d4ce8b7427dd`; finalized with `MAJORITY_AGREE`; authoritative execution-result certification is recorded as UNKNOWN because the receipt omits the top-level execution result.
- Deployed source was retrieved through `gen_getContractCode`, base64-decoded, and compared byte-for-byte: 20,018 bytes and SHA-256 `240abb1f32bb5e65196133792f1b7f9ac5f143912957895adf1b98ccae493246`; exact parity.
- Direct Mode: 18/18 passing. Frontend tests: 7/7 passing. Production build and preflight pass. GenVM lint checks pass; SDK validation/schema generation remain subject to the Windows cache-permission limitation documented above.
- Frontend production deployment: `https://verid-sigma.vercel.app`, Vercel deployment `dpl_3vdPvUDVNGNtcuXLRjvNaUXixNHw`.
- Live final-CA evidence: profile creation `0x0df6d45b59da1b774f533b6a0d12fa39032b55c6893de5c3c31bc5ea1d0192b7`; challenge `0x8aba05d70dcf02ebbbc7a9c3a52a7862020daf5e24cf491ff2135a06f2e37aea`; surface registration `0xb87e77f5ffb562da08631a4189c6f22f4a6d7fa351c3c65b6de3cd53087e6a6a`; semantic verification `0xeb5a8d54133e05679cf29fab093eadcde41f6673f5161e311c6a940e3559fe68`.
- Final live readback: profile 1 exists, challenge id 1 and verification cycle 1 are present, the Vercel surface is reachable and contains the challenge, but the semantic result is `UNVERIFIED` with `identity_relation=UNRESOLVED` and `authenticity=UNRESOLVED`. No proof, gate membership, or room access is claimed from this run.
