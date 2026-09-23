# Verid

**Prove the public accounts you control.**

Verid is an expiring public account-control proof protocol for GenLayer Studionet. A wallet publishes a challenge on declared public identity surfaces, validators independently fetch those surfaces and establish first-party identity context, and deterministic contract logic derives proof tier and gate eligibility.

Verid is **not KYC** and does not collect passports, government ID, biometrics, private email, phone numbers, home addresses, or dates of birth.

## Status

- Network: **GenLayer Studionet**
- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com`
- Canonical source: `contracts/verid.py`
- Contract: exactly one `Verid(gl.Contract)`
- Deployment: current address and its finality/parity status are recorded in `verid-manifest.json`
- Frontend address: must equal the canonical deployed address; blank configuration is invalid for a release

No fake users, proofs, memberships, transaction hashes, explorer links, contract address, simulation mode, mock consensus, or localStorage authorization are used.

## Product routes

`/`, `/start`, `/me`, `/p/[id]`, `/p/[id]/challenge`, `/p/[id]/verify`, `/proof/[id]`, `/gates`, `/g/[id]`, `/g/[id]/room`.

## Protocol

`wallet → profile → challenge → publish → register evidence → GenLayer semantic verification → deterministic tier → proof → gate → on-chain membership`

Challenge substring presence alone is insufficient. Validators independently fetch the declared surface and reproduce proof-affecting challenge presence, identity relationship, and first-party authenticity. Evidence excerpts are grounded in fetched content. Monotonic challenge IDs bind the Studionet domain, wallet, profile, request ID and expiry. Verification is cycle-bound, proof evidence is capped at 30 days, and STRONG requires GitHub plus a qualifying surface on a different canonical host.

The frontend uses an injected wallet and silently restores an already-authorized account through `eth_accounts`; only an explicit Connect action requests wallet permission. It tracks account, chain, and disconnect events, can add or switch Studionet, and gates room access on a fresh `is_member` read. GitHub identity claims use canonical public GitHub user JSON and deterministic login, profile URL, ID, and bio checks. Other supported public surfaces use GenLayer semantic consensus.

## Checks

```bash
npm ci
npm run check
npm run contract:check
```

Checks include Python compilation, GenVM lint, schema generation, the real `gltest` Direct Mode suite, frontend tests/build and preflight. Current deployment and parity metadata are recorded in `verid-manifest.json`.

The configured Studionet contract is `0xD4d621bBD288496cab9f7f5Ec23C579816D84EB3`, transaction `0x579901dc9706ec0d13c88b55224309ee191107b4bbfb7cb5140dbfae3bdb6f65`. It is accepted but not verified finalized, and deployed-source parity is not proven. The previous `0x4A430f7326DEdcd796df149Ce5d31223c5943d92` is a superseded historical deployment. Do not treat this release as production-ready until corrected source is deployed after green checks and exact byte parity is established.

See `REVIEW.md` and `docs/`.
