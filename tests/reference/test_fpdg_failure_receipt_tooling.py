from types import SimpleNamespace

from tools.run_reference_suite_with_fpdg_receipt import FpdgFailurePlugin, load_bindings


def test_relative_entropy_failure_maps_to_exact_idt_claim_and_test_coordinate():
    plugin = FpdgFailurePlugin(load_bindings())
    path = "tests/reference/test_local_clock_relative_entropy.py"
    report = SimpleNamespace(
        failed=True,
        nodeid=f"{path}::test_exponential_kl_reduces_exactly_to_phi_of_lapse",
        when="call",
        location=(path, 10, "test_exponential_kl_reduces_exactly_to_phi_of_lapse"),
        longrepr=None,
    )

    plugin.pytest_runtest_logreport(report)

    assert len(plugin.failures) == 1
    failure = plugin.failures[0]
    assert failure["claim_id"] == "IDT.CLOCK.RELATIVE_ENTROPY_05D"
    assert failure["source_locator"]["path"] == path
    assert failure["source_locator"]["line_start"] == 11
    assert failure["source_locator"]["test_id"].endswith("::test_exponential_kl_reduces_exactly_to_phi_of_lapse")
    assert "claim-source:formalism/05D_local_clock_relative_entropy_potential.md" in failure["evidence_refs"]


def test_unmapped_failure_keeps_exact_test_coordinate_without_claim_guess():
    plugin = FpdgFailurePlugin(load_bindings())
    path = "tests/reference/test_zeta_collatz_joint_discriminator.py"
    report = SimpleNamespace(
        failed=True,
        nodeid=f"{path}::test_unmapped",
        when="call",
        location=(path, 7, "test_unmapped"),
        longrepr="assertion failed",
    )

    plugin.pytest_runtest_logreport(report)

    failure = plugin.failures[0]
    assert "claim_id" not in failure
    assert failure["source_locator"]["path"] == path
    assert failure["source_locator"]["line_start"] == 8


def test_collection_failure_is_recorded_with_binding_when_known():
    plugin = FpdgFailurePlugin(load_bindings())
    path = "tests/reference/test_temporal_primitive_activity.py"
    report = SimpleNamespace(
        failed=True,
        nodeid=path,
        location=(path, 3, "<module>"),
        longrepr="import failed",
    )

    plugin.pytest_collectreport(report)

    failure = plugin.failures[0]
    assert failure["claim_id"] == "IDT.TEMPORAL.PRIMITIVE"
    assert failure["source_locator"]["line_start"] == 4
    assert "pytest-phase:collection" in failure["evidence_refs"]
