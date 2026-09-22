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
- Deployment: **not yet performed in Stage One**
- Frontend address: intentionally blank until verified deployment

No fake users, proofs, memberships, transaction hashes, explorer links, contract address, simulation mode, mock consensus, or localStorage authorization are used.

## Product routes

`/`, `/start`, `/me`, `/p/[id]`, `/p/[id]/challenge`, `/p/[id]/verify`, `/proof/[id]`, `/gates`, `/g/[id]`, `/g/[id]/room`.

## Protocol

`wallet → profile → challenge → publish → register evidence → GenLayer semantic verification → deterministic tier → proof → gate → on-chain membership`

Challenge substring presence alone is insufficient. Validators independently fetch the declared surface and reproduce proof-affecting challenge presence, identity relationship, and first-party authenticity. Evidence excerpts are grounded in fetched content. The contract—not the model—derives UNVERIFIED/BASIC/STRONG/CONFLICTED/EXPIRED/REVOKED.

The frontend uses an injected wallet, never auto-connects, tracks account/chain/disconnect events, can add/switch Studionet, blocks wrong-chain writes again before signature, distinguishes explicit FINISHED_WITH_RETURN from explicit failure and unknown finalized execution, and re-reads contract state. Gate-room access is authorized only by a fresh `is_member` read.

## Checks

```bash
npm ci
npm run check
npm run contract:check
```

If available, also run `genvm-lint check contracts/verid.py`. Deep Direct Mode/adversarial contract audit and deployment-parity verification remain for the final Codex pass.

See `REVIEW.md` and `docs/`.
