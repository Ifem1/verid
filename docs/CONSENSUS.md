# Consensus

Challenge substring presence alone is not Verid verification.

For each declared public surface, leader and validators independently fetch the same URL, check the exact challenge, derive identity relationship, derive first-party authenticity/context, and ground any excerpt in fetched content.

`gl.vm.run_nondet_unsafe` uses an independent validator. Proof-affecting `reachable`, `challenge_present`, `identity_relation`, and `authenticity` must be reproduced; material disagreement fails validation. If the leader returns an excerpt, the validator independently fetches the body and requires that excerpt to occur in its body, without requiring validators to choose the same excerpt.

VERIFIED requires reachable + challenge present + MATCH + FIRST_PARTY. MISMATCH or NOT_FIRST_PARTY becomes CONFLICTED. Everything else remains UNVERIFIED. Final proof tier is deterministic contract logic, never a model-selected field.
