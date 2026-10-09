import json
import pytest
from liquid_lab.experiment import evidence_digest, logic_gate, run_experiment, save_evidence, verify_evidence


@pytest.mark.parametrize("gate,expected", [("AND", [0, 0, 0, 1]), ("OR", [0, 1, 1, 1]), ("XOR", [0, 1, 1, 0])])
def test_truth_tables(gate, expected):
    assert [logic_gate(gate, *p) for p in [(0, 0), (0, 1), (1, 0), (1, 1)]] == expected


def test_deterministic():
    assert run_experiment(seed=7, noise=0.3) == run_experiment(seed=7, noise=0.3)


def test_noise_limits():
    assert run_experiment(noise=0)["metrics"]["accuracy"] == 1
    assert run_experiment(noise=1)["metrics"]["accuracy"] == 0


def test_input_validation():
    for args in ({"noise": 1.1}, {"noise": float("nan")}, {"trials": 0}, {"trials": True}, {"gate": "NAND"}):
        with pytest.raises(ValueError):
            run_experiment(**args)
    with pytest.raises(ValueError):
        logic_gate("AND", 2, 1)


def test_evidence(tmp_path):
    evidence = run_experiment(trials=4)
    path = save_evidence(evidence, tmp_path)
    obj = json.loads(path.read_text())
    assert obj["result"] == evidence
    assert obj["sha256"] == evidence_digest(evidence)
    assert verify_evidence(path)
    original_bytes = path.read_bytes()
    assert save_evidence(evidence, tmp_path) == path
    assert path.read_bytes() == original_bytes


def test_tampering_detected(tmp_path):
    path = save_evidence(run_experiment(trials=4), tmp_path)
    payload = json.loads(path.read_text())
    payload["result"]["metrics"]["accuracy"] = 0
    path.write_text(json.dumps(payload))
    assert not verify_evidence(path)
    with pytest.raises(ValueError):
        save_evidence(run_experiment(trials=4), tmp_path)


def test_reference_example():
    result = run_experiment("XOR", 100, 42, 0.05)
    assert result["metrics"] == {"accuracy": 0.93, "correct": 93, "total": 100}
    assert result["physical_computing_demonstrated"] is False
