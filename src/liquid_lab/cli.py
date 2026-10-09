"""CLI for synthetic logic-gate baseline evidence."""
import argparse
import json
from .experiment import run_experiment, save_evidence, verify_evidence


def main() -> None:
    parser = argparse.ArgumentParser(description="MLC synthetic research baseline (not fluid physics)")
    parser.add_argument("--gate", choices=["AND", "OR", "XOR"], default="XOR")
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--noise", type=float, default=0.0)
    parser.add_argument("--output", default="runs")
    args = parser.parse_args()
    result = run_experiment(args.gate, args.trials, args.seed, args.noise)
    path = save_evidence(result, args.output)
    if not verify_evidence(path):
        raise RuntimeError("Evidence integrity verification failed")
    print(json.dumps({"evidence": str(path), "metrics": result["metrics"], "backend": result["backend"], "physical_computing_demonstrated": False}, indent=2))


if __name__ == "__main__":
    main()
