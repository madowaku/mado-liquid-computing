# 💧 MLC-M0.0 Liquid Computing Research Lab

An evidence-first, Python-based research harness for exploring whether droplet/liquid dynamics can perform useful computations.

**Current status: S0 synthetic logic baseline only.** This is not a computational fluid dynamics solver, a physical droplet experiment, or proof of a liquid logic gate. The fixed truth tables are implemented in Python. Synthetic output bit flips are injected as an independent test of the evidence pipeline.

## Quick start

```bash
python -m pip install -e . pytest
mlc --gate XOR --trials 100 --seed 42 --noise 0.05 --output runs
python -m pytest -q
```

Expected baseline: 93 correct out of 100 trials for the above seed, or **93% synthetic accuracy**. This number does not measure liquid hardware.

## Deliverables

- AND/OR/XOR reference truth tables and seeded bit-flip baseline
- Per-trial output with parameters, software backend ID, and explicit non-physical claim flag
- SHA-256 content-addressed JSON evidence files with verification and overwrite protection
- Automated Python tests and GitHub Actions CI
- [Evidence/claim contract](docs/RESEARCH_CONTRACT.md)
- [M0.1 MMFT intake specification](docs/M0.1_MMFT_INTAKE.md)

## Research tracks

1. **Logic**: truth tables, timing windows, error rates, reproducibility.
2. **Physics**: models/observations of channel/droplet dynamics with physical parameters.
3. **Device comparison**: energy, latency, throughput, fabrication, controller and measurement overhead.

## Source and next milestone

Candidate external simulator: [MMFT Simulator](https://github.com/cda-tum/mmft-simulator). It is **not** bundled or executed in M0.0. The next step is `MLC-M0.1 MMFT Adapter / Physical Droplet Evidence`, with independent physics-based reference checks.

## Provenance and research honesty

All saved evidence includes `backend=synthetic-bit-flip-baseline` and `physical_computing_demonstrated=false`. Do not promote S0 results to physical-computation claims. SHA-256 checksums verify result-file integrity, not experimental truth or sensor provenance.
