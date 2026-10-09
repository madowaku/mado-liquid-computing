"""Deterministic software baselines; this module does not model fluid physics."""
from __future__ import annotations

import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "mlc-evidence-0.0.1"
GATES = ("AND", "OR", "XOR")


def logic_gate(gate: str, a: int, b: int) -> int:
    """Evaluate a reference Boolean gate (not a physical device)."""
    if gate not in GATES:
        raise ValueError(f"Unknown gate: {gate}")
    if a not in (0, 1) or b not in (0, 1):
        raise ValueError("inputs must be binary (0 or 1)")
    if gate == "AND":
        return a & b
    if gate == "OR":
        return a | b
    return a ^ b


def run_experiment(gate: str = "XOR", trials: int = 100, seed: int = 42, noise: float = 0.0) -> dict:
    """Replay a fixed truth table with independent synthetic bit-flip errors."""
    if gate not in GATES:
        raise ValueError("gate must be AND, OR or XOR")
    if not isinstance(trials, int) or isinstance(trials, bool) or trials < 1:
        raise ValueError("trials must be an integer >= 1")
    if not 0 <= noise <= 1:  # Also rejects NaN.
        raise ValueError("noise must be between 0 and 1")
    rng = random.Random(seed)
    cases = ((0, 0), (0, 1), (1, 0), (1, 1))
    observations = []
    for i in range(trials):
        a, b = cases[i % 4]
        expected = logic_gate(gate, a, b)
        observed = expected ^ int(rng.random() < noise)
        observations.append({
            "trial": i, "a": a, "b": b,
            "expected": expected, "observed": observed,
            "correct": observed == expected,
        })
    correct = sum(row["correct"] for row in observations)
    return {
        "schema_version": SCHEMA_VERSION,
        "track": "logic",
        "backend": "synthetic-bit-flip-baseline",
        "physical_computing_demonstrated": False,
        "parameters": {"gate": gate, "trials": trials, "seed": seed, "noise": noise},
        "metrics": {"accuracy": correct / trials, "correct": correct, "total": trials},
        "observations": observations,
    }


def evidence_digest(result: dict) -> str:
    canonical = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def verify_evidence(path: str | Path) -> bool:
    """Verify that the stored SHA-256 commits to the stored result payload."""
    try:
        envelope = json.loads(Path(path).read_text(encoding="utf-8"))
        return envelope["sha256"] == evidence_digest(envelope["result"])
    except (OSError, ValueError, TypeError, KeyError):
        return False


def save_evidence(result: dict, output_dir: str | Path) -> Path:
    """Write content-addressed evidence; never silently overwrite an existing run."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    digest = evidence_digest(result)
    path = output / f"{digest}.json"
    if path.exists():
        if not verify_evidence(path):
            raise ValueError(f"Existing evidence failed integrity check: {path}")
        if json.loads(path.read_text(encoding="utf-8"))["result"] != result:
            raise ValueError(f"Existing evidence differs from result: {path}")
        return path
    envelope = {"created_at": datetime.now(timezone.utc).isoformat(), "sha256": digest, "result": result}
    # Exclusive creation avoids overwriting the same address in parallel runs.
    try:
        with path.open("x", encoding="utf-8") as stream:
            json.dump(envelope, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
    except FileExistsError:
        if not verify_evidence(path):
            raise ValueError(f"Concurrent evidence failed integrity check: {path}")
    return path
