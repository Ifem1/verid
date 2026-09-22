# Architecture

Verid has a static browser frontend and exactly one GenLayer Intelligent Contract: `contracts/verid.py` / `Verid(gl.Contract)`. There is no backend database or off-chain authorization authority.

Profiles bind wallets to public surfaces. Challenges expire. Verified surfaces feed deterministic tiers. Proofs snapshot tier + verified public surfaces and expire. Gates store minimum tier, required surface types and maximum proof age. `join_gate` writes membership on-chain. `/g/[id]/room` renders only after a fresh `is_member` read.

Tier derivation: REVOKED → EXPIRED → CONFLICTED → STRONG (GitHub + another verified surface) → BASIC (one verified surface) → UNVERIFIED.
