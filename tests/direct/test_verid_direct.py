import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


CONTRACT = str(Path(__file__).parents[2] / "contracts" / "verid.py")


def deploy(direct_deploy):
    return direct_deploy(CONTRACT, sdk_version="v0.2.16")


def mock_github(vm, challenge, login="alice", github_id=123, html_url=None, bio=None):
    body = {"login": login, "id": github_id,
            "html_url": html_url or f"https://github.com/{login}",
            "bio": bio if bio is not None else f"VERID {challenge}"}
    vm.mock_web(r"https://api\.github\.com/users/", {"status": 200, "body": json.dumps(body)})


def github_setup(vm, deploy_fn, alice, *, login="alice"):
    c = deploy(deploy_fn)
    vm.sender = alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    challenge = json.loads(c.get_profile(1))["challenge"]
    c.register_surface(1, "GITHUB", f"https://github.com/{login}")
    return c, challenge


@pytest.mark.parametrize("url", [
    "https://github.com/alice/repo", "https://github.com/alice?tab=repositories",
    "https://github.com/", "http://github.com/alice", "https://github.com/alice/",
])
def test_github_identity_rejects_noncanonical_urls(direct_vm, direct_deploy, direct_alice, url):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    with direct_vm.expect_revert("safe https URL" if url.startswith("http://") else "GitHub surface"):
        c.register_surface(1, "GITHUB", url)


@pytest.mark.parametrize("payload,expected", [
    ({"login": "alice", "id": 123, "html_url": "https://github.com/alice", "bio": "proof {challenge}"}, "VERIFIED"),
    ({"login": "other", "id": 123, "html_url": "https://github.com/other", "bio": "proof {challenge}"}, "CONFLICTED"),
    ({"login": "alice", "id": 123, "html_url": "https://github.com/other", "bio": "proof {challenge}"}, "CONFLICTED"),
    ({"login": "alice", "id": None, "html_url": "https://github.com/alice", "bio": "proof {challenge}"}, "UNVERIFIED"),
    ({"login": "alice", "id": 123, "html_url": "https://github.com/alice", "bio": "no challenge"}, "UNVERIFIED"),
    ({"login": "alice", "id": 123, "html_url": "https://github.com/alice", "bio": ""}, "UNVERIFIED"),
])
def test_github_canonical_json_material_facts(direct_vm, direct_deploy, direct_alice, payload, expected):
    c, challenge = github_setup(direct_vm, direct_deploy, direct_alice)
    data = {k: (v.format(challenge=challenge) if isinstance(v, str) else v) for k, v in payload.items()}
    direct_vm.mock_web(r"https://api\.github\.com/users/", {"status": 200, "body": json.dumps(data)})
    c.verify_surface(1, 0)
    surface = json.loads(c.get_profile(1))["surfaces"][0]
    assert surface["status"] == expected
    if expected == "VERIFIED":
        assert surface["canonical_login"] == "alice"
        assert surface["canonical_github_id"] == "123"
        assert surface["identity_relation"] == "MATCH"
        assert surface["authenticity"] == "FIRST_PARTY"


@pytest.mark.parametrize("body", ["not-json", "{}", "null"])
def test_github_unavailable_or_malformed_response_is_nonpositive(direct_vm, direct_deploy, direct_alice, body):
    c, _ = github_setup(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_web(r"https://api\.github\.com/users/", {"status": 200, "body": body})
    c.verify_surface(1, 0)
    assert json.loads(c.get_profile(1))["surfaces"][0]["status"] != "VERIFIED"


def test_github_validator_rejects_leader_lies_and_independent_source_disagreement(direct_vm, direct_deploy, direct_alice):
    c, challenge = github_setup(direct_vm, direct_deploy, direct_alice)
    mock_github(direct_vm, challenge)
    c.verify_surface(1, 0)
    good = {"reachable": True, "canonical_login_match": True, "canonical_profile_match": True,
            "challenge_present": True, "canonical_login": "alice", "canonical_profile_url": "https://github.com/alice",
            "canonical_github_id": "123", "canonical_bio": f"VERID {challenge}",
            "identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": f"VERID {challenge}"}
    for field, lie in (("canonical_login", "mallory"), ("challenge_present", False), ("canonical_github_id", "999")):
        forged = dict(good)
        forged[field] = lie
        assert direct_vm.run_validator(leader_result=forged) is False
    direct_vm.clear_mocks()
    mock_github(direct_vm, challenge, login="mallory", html_url="https://github.com/mallory")
    assert direct_vm.run_validator() is False


def test_github_verification_is_invalidated_by_fresh_challenge(direct_vm, direct_deploy, direct_alice):
    c, challenge = github_setup(direct_vm, direct_deploy, direct_alice)
    mock_github(direct_vm, challenge)
    c.verify_surface(1, 0)
    assert json.loads(c.get_profile(1))["surfaces"][0]["status"] == "VERIFIED"
    c.issue_challenge(1, 600)
    surface = json.loads(c.get_profile(1))["surfaces"][0]
    assert surface["status"] == "PENDING"
    assert surface["verification_cycle"] == -1


def test_profile_ownership_and_label(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("profile label required"):
        c.create_profile("")
    c.create_profile("Alice")
    with direct_vm.expect_revert("wallet already has a profile"):
        c.create_profile("Again")
    with direct_vm.prank(direct_bob):
        c.create_profile("Bob")
    with direct_vm.prank(direct_bob):
        with direct_vm.expect_revert("profile owner only"):
            c.issue_challenge(1, 600)


def test_challenge_ids_are_monotonic_and_domain_bound(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    first = json.loads(c.get_profile(1))
    c.issue_challenge(1, 600)
    second = json.loads(c.get_profile(1))
    assert second["challenge_id"] == first["challenge_id"] + 1
    assert second["verification_cycle"] == first["verification_cycle"] + 1
    assert second["challenge"] != first["challenge"]
    assert "61999" not in second["challenge"]


def test_surface_registration_validation(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    with direct_vm.expect_revert("unsupported public surface"):
        c.register_surface(1, "SOCIAL", "https://example.com/a")
    with direct_vm.expect_revert("safe https URL"):
        c.register_surface(1, "GITHUB", "http://example.com/a")
    c.issue_challenge(1, 600)
    c.register_surface(1, "GITHUB", "https://github.com/alice")
    with direct_vm.expect_revert("surface already registered"):
        c.register_surface(1, "GITHUB", "https://github.com/alice")


def test_basic_verification_and_fresh_cycle_invalidation(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    challenge = json.loads(c.get_profile(1))["challenge"]
    url = "https://example.com/alice"
    c.register_surface(1, "WEBSITE", url)
    direct_vm.mock_web("example.com/alice", {"status": 200, "body": "Official Alice page " + challenge})
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 0)
    assert json.loads(c.get_profile(1))["tier"] == "BASIC"
    c.issue_challenge(1, 600)
    assert json.loads(c.get_profile(1))["tier"] == "UNVERIFIED"


def test_unreachable_and_malformed_output_do_not_verify(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    c.register_surface(1, "WEBSITE", "https://unreachable.example/page")
    direct_vm.mock_llm(".*", "not-json")
    c.verify_surface(1, 0)
    assert json.loads(c.get_profile(1))["surfaces"][0]["status"] != "VERIFIED"


def test_independent_authority_required_for_strong(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    p = json.loads(c.get_profile(1))
    challenge = p["challenge"]
    c.register_surface(1, "GITHUB", "https://github.com/alice")
    c.register_surface(1, "PROJECT", "https://github.com/alice/verid-project")
    mock_github(direct_vm, challenge)
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 0)
    c.verify_surface(1, 1)
    assert json.loads(c.get_profile(1))["tier"] != "STRONG"


@pytest.mark.parametrize("second_url", [
    "https://www.github.com/alice/project",
    "https://gist.github.com/alice/abc",
])
def test_github_authority_family_cannot_inflate_strong(direct_vm, direct_deploy, direct_alice, second_url):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    challenge = json.loads(c.get_profile(1))["challenge"]
    c.register_surface(1, "GITHUB", "https://github.com/alice")
    c.register_surface(1, "PROJECT", second_url)
    mock_github(direct_vm, challenge)
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 0)
    c.verify_surface(1, 1)
    assert json.loads(c.get_profile(1))["tier"] != "STRONG"


def test_independent_example_authority_can_be_strong(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    challenge = json.loads(c.get_profile(1))["challenge"]
    c.register_surface(1, "GITHUB", "https://github.com/alice")
    c.register_surface(1, "WEBSITE", "https://example.com/alice")
    mock_github(direct_vm, challenge)
    direct_vm.mock_web("example.com", {"status": 200, "body": challenge})
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 0)
    c.verify_surface(1, 1)
    assert json.loads(c.get_profile(1))["tier"] == "STRONG"


def test_positive_result_requires_grounded_nonempty_excerpt(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    challenge = json.loads(c.get_profile(1))["challenge"]
    c.register_surface(1, "WEBSITE", "https://example.com/alice")
    direct_vm.mock_web("example.com", {"status": 200, "body": "Official page " + challenge})
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": ""}))
    c.verify_surface(1, 0)
    assert json.loads(c.get_profile(1))["surfaces"][0]["status"] != "VERIFIED"


def test_proof_lineage_and_revocation(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    challenge = json.loads(c.get_profile(1))["challenge"]
    c.register_surface(1, "WEBSITE", "https://example.com/alice")
    direct_vm.mock_web("example.com", {"status": 200, "body": challenge})
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 0)
    c.issue_proof(1, 600)
    proof = json.loads(c.get_proof(1))
    assert proof["verification_cycle"] == 1
    assert proof["challenge_id"] == 1
    c.revoke_profile(1)
    assert json.loads(c.get_proof(1))["status"] == "REVOKED"


def _strong_setup(c, vm, alice):
    vm.sender = alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    challenge = json.loads(c.get_profile(1))["challenge"]
    c.register_surface(1, "GITHUB", "https://github.com/alice")
    c.register_surface(1, "WEBSITE", "https://example.com/alice")
    mock_github(vm, challenge)
    vm.mock_web("example.com", {"status": 200, "body": challenge})
    vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 0)
    c.verify_surface(1, 1)
    c.issue_proof(1, 600)
    c.create_gate("Strong room", "STRONG", "GITHUB", "WEBSITE", 300)
    return json.loads(c.get_profile(1)), 1


def _warp_after(vm, seconds):
    current = datetime.fromisoformat(vm._datetime.replace("Z", "+00:00"))
    timestamp = (current + timedelta(seconds=seconds)).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    vm.warp(timestamp)
    import genlayer.gl as gl
    if isinstance(getattr(gl, "message_raw", None), dict):
        gl.message_raw["datetime"] = timestamp


def test_gate_rejects_basic_missing_surface_and_wrong_wallet(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    challenge = json.loads(c.get_profile(1))["challenge"]
    c.register_surface(1, "WEBSITE", "https://example.com/alice")
    direct_vm.mock_web("example.com", {"status": 200, "body": challenge})
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 0)
    c.issue_proof(1, 600)
    c.create_gate("Strong", "STRONG", "GITHUB", "", 604800)
    assert c.is_eligible(1, 1, direct_alice) is False
    with direct_vm.expect_revert("proof does not satisfy gate"):
        c.join_gate(1, 1)
    with direct_vm.prank(direct_bob):
        assert c.is_eligible(1, 1, direct_bob) is False
        with direct_vm.expect_revert("proof does not satisfy gate"):
            c.join_gate(1, 1)


def test_valid_strong_membership_revocation_and_expiry(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    profile, gate_id = _strong_setup(c, direct_vm, direct_alice)
    assert profile["tier"] == "STRONG"
    wallet = profile["wallet"]
    assert c.is_eligible(gate_id, 1, wallet) is True
    c.join_gate(gate_id, 1)
    assert c.is_member(gate_id, wallet) is True
    _warp_after(direct_vm, 301)
    assert c.is_member(gate_id, wallet) is False


def test_revocation_invalidates_membership_and_old_proof_cannot_rejoin(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    _strong_setup(c, direct_vm, direct_alice)
    c.join_gate(1, 1)
    c.revoke_profile(1)
    assert c.is_member(1, direct_alice) is False
    with direct_vm.expect_revert("proof does not satisfy gate"):
        c.join_gate(1, 1)


def test_fresh_replacement_proof_restores_eligibility(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    _strong_setup(c, direct_vm, direct_alice)
    old = json.loads(c.get_proof(1))
    c.issue_challenge(1, 600)
    direct_vm.clear_mocks()
    p = json.loads(c.get_profile(1))
    challenge = p["challenge"]
    c.register_surface(1, "GITHUB", "https://github.com/alice-refresh")
    c.register_surface(1, "WEBSITE", "https://example.com/alice-refresh")
    mock_github(direct_vm, challenge, login="alice-refresh")
    direct_vm.mock_web("example.com/alice-refresh", {"status": 200, "body": challenge})
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 2)
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 3)
    assert json.loads(c.get_profile(1))["tier"] == "STRONG"
    c.issue_proof(1, 600)
    fresh = json.loads(c.get_proof(2))
    assert old["proof_id"] == 1 and fresh["proof_id"] == 2
    assert fresh["challenge_id"] == old["challenge_id"] + 1
    assert c.is_eligible(1, 2, fresh["wallet"]) is True


@pytest.mark.parametrize("bad", [
    {"identity_relation": "MISMATCH", "authenticity": "FIRST_PARTY", "excerpt": "x"},
    {"identity_relation": "MATCH", "authenticity": "NOT_FIRST_PARTY", "excerpt": "x"},
    {"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": "not-present"},
])
def test_validator_material_or_excerpt_disagreement_fails(direct_vm, direct_deploy, direct_alice, bad):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    challenge = json.loads(c.get_profile(1))["challenge"]
    c.register_surface(1, "WEBSITE", "https://example.com/alice")
    direct_vm.mock_web("example.com", {"status": 200, "body": "Official " + challenge})
    direct_vm.mock_llm(".*", json.dumps(bad))
    c.verify_surface(1, 0)
    assert json.loads(c.get_profile(1))["surfaces"][0]["status"] != "VERIFIED"


def test_proof_tier_is_rederivable_from_stored_evidence(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    profile, _ = _strong_setup(c, direct_vm, direct_alice)
    proof = json.loads(c.get_proof(1))
    assert proof["tier"] == "STRONG"
    assert {x["type"] for x in proof["verified_surfaces"]} == {"GITHUB", "WEBSITE"}
    assert proof["tier"] == "STRONG" if {x["type"] for x in proof["verified_surfaces"]} == {"GITHUB", "WEBSITE"} else False


@pytest.mark.parametrize("url", [
    "https://alice.github.io/proof",
    "https://raw.githubusercontent.com/alice/project/main/proof.html",
])
def test_github_control_plane_does_not_count_as_independent(direct_vm, direct_deploy, direct_alice, url):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 600)
    challenge = json.loads(c.get_profile(1))["challenge"]
    c.register_surface(1, "GITHUB", "https://github.com/alice")
    c.register_surface(1, "WEBSITE", url)
    mock_github(direct_vm, challenge)
    direct_vm.mock_web("github.io", {"status": 200, "body": challenge})
    direct_vm.mock_web("raw.githubusercontent.com", {"status": 200, "body": challenge})
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 0)
    c.verify_surface(1, 1)
    p = json.loads(c.get_profile(1))
    assert p["surfaces"][0]["authority"] == "github"
    assert p["surfaces"][1]["authority"] == "github"
    assert p["tier"] == "BASIC"


def test_staggered_evidence_age_cannot_elevate_omitted_stale_surface(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_deploy)
    direct_vm.sender = direct_alice
    c.create_profile("Alice")
    c.issue_challenge(1, 7 * 24 * 60 * 60)
    challenge = json.loads(c.get_profile(1))["challenge"]
    c.register_surface(1, "GITHUB", "https://github.com/alice-staggered")
    c.register_surface(1, "WEBSITE", "https://alice.example.com/staggered")

    mock_github(direct_vm, challenge, login="alice-staggered")
    c.verify_surface(1, 0)

    _warp_after(direct_vm, 6 * 24 * 60 * 60)
    direct_vm.clear_mocks()
    direct_vm.mock_web("alice.example.com/staggered", {"status": 200, "body": "Official website " + challenge})
    direct_vm.mock_llm(".*", json.dumps({"identity_relation": "MATCH", "authenticity": "FIRST_PARTY", "excerpt": challenge}))
    c.verify_surface(1, 1)

    _warp_after(direct_vm, 25 * 24 * 60 * 60)
    c.issue_proof(1, 600)
    proof = json.loads(c.get_proof(1))
    stored_types = {x["type"] for x in proof["verified_surfaces"]}
    assert stored_types == {"WEBSITE"}
    assert proof["tier"] == "BASIC"
    assert proof["tier"] != "STRONG"
    assert len(proof["verified_surfaces"]) == 1
    assert proof["verified_surfaces"][0]["type"] == "WEBSITE"
