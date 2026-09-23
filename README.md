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
- Deployment: recorded in `verid-manifest.json` only after exact-source parity verification
- Frontend address: must equal the canonical deployed address; blank configuration is invalid for a release

No fake users, proofs, memberships, transaction hashes, explorer links, contract address, simulation mode, mock consensus, or localStorage authorization are used.

## Product routes

`/`, `/start`, `/me`, `/p/[id]`, `/p/[id]/challenge`, `/p/[id]/verify`, `/proof/[id]`, `/gates`, `/g/[id]`, `/g/[id]/room`.

## Protocol

`wallet → profile → challenge → publish → register evidence → GenLayer semantic verification → deterministic tier → proof → gate → on-chain membership`

Challenge substring presence alone is insufficient. Validators independently fetch the declared surface and reproduce proof-affecting challenge presence, identity relationship, and first-party authenticity. Evidence excerpts are grounded in fetched content. Monotonic challenge IDs bind the Studionet domain, wallet, profile, request ID and expiry. Verification is cycle-bound, proof evidence is capped at 30 days, and STRONG requires GitHub plus a qualifying surface on a different canonical host.

The frontend uses an injected wallet, never auto-connects, tracks account/chain/disconnect events, can add/switch Studionet, blocks wrong-chain writes again before signature, distinguishes explicit FINISHED_WITH_RETURN from explicit failure and unknown finalized execution, and re-reads contract state. Gate-room access is authorized only by a fresh `is_member` read.

## Checks

```bash
npm ci
npm run check
npm run contract:check
```

Checks include Python compilation, GenVM lint, schema generation, the real `gltest` Direct Mode suite, frontend tests/build and preflight. Current deployment and parity metadata are recorded in `verid-manifest.json`.

Current canonical deployment: `0x4A430f7326DEdcd796df149Ce5d31223c5943d92` on Studionet 61999, deployment transaction `0x3ea54a4abee79a9da8a3c973c04779ad5912572c72ec67ff6c2124e34d09d479`. The exact committed source is 20,134 bytes with SHA-256 `caca027a0253142bee2f5793a508c76b645907b61815ca9c626345caf22184c4`; deployed-source parity is exact-byte-match. The documented live semantic attempt honestly remained `UNVERIFIED` with unresolved identity/authenticity, so no proof or gate success is claimed.

See `REVIEW.md` and `docs/`.
