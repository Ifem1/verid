import json
from pathlib import Path

import pytest


CONTRACT = str(Path(__file__).parents[2] / "contracts" / "verid.py")


def deploy(direct_deploy):
    return direct_deploy(CONTRACT, sdk_version="v0.2.16")


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
    c.register_surface(1, "GITHUB", "https://github.com/alice/verid")
    with direct_vm.expect_revert("surface already registered"):
        c.register_surface(1, "GITHUB", "https://github.com/alice/verid")


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
    c.register_surface(1, "GITHUB", "https://github.com/alice/verid")
    c.register_surface(1, "PROJECT", "https://github.com/alice/verid-project")
    direct_vm.mock_web("github.com", {"status": 200, "body": "official " + challenge})
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
    c.register_surface(1, "GITHUB", "https://github.com/alice/verid")
    c.register_surface(1, "PROJECT", second_url)
    direct_vm.mock_web("github.com", {"status": 200, "body": challenge})
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
    c.register_surface(1, "GITHUB", "https://github.com/alice/verid")
    c.register_surface(1, "WEBSITE", "https://example.com/alice")
    direct_vm.mock_web("github.com", {"status": 200, "body": challenge})
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
