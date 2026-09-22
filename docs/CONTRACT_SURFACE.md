# Contract surface

Writes: `create_profile`, `issue_challenge`, `register_surface`, `verify_surface`, `issue_proof`, `revoke_profile`, `create_gate`, `join_gate`.

Views: `get_profile`, `get_profile_for_wallet`, `get_profile_count`, `get_proof`, `get_proof_count`, `get_gate`, `get_gate_count`, `is_eligible`, `is_member`.

The browser calls these methods directly. There is no alternate backend state model.
