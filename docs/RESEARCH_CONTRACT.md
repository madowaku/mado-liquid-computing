# Evidence and claim contract (MLC-M0.0)

## Objective
Investigate whether liquid droplets can physically implement information processing, with falsifiable hypotheses and reproducible measurements.

## Claim levels

| Level | Allowed claim | Evidence required |
|---|---|---|
| S0 | Software truth-table baseline | Runnable code, fixed seed, input/output, checksums |
| S1 | Physics-based simulation | Model equations, parameters, simulator version, independent reference checks |
| S2 | Physical-device observation | Raw sensor data, apparatus, controls, calibration, repeat trials |
| S3 | Competitive physical computation | S2 plus device-level energy, latency, throughput, error rate and fair system baseline |

The M0.0 backend is **S0 only**. Successful logic tests or high accuracy of the synthetic baseline are not evidence of liquid logic.

## Minimum measurements for M0.1+
- Input encoding and output readout that are physically specified
- Device geometry and dimensions; fluid properties; boundary conditions
- Timestamped state traces and sensor uncertainties
- Null controls and repeat trials across configurations
- Separation of actuator/controller computation from liquid-mediated computation
- Failures and excluded trials retained in an append-only audit trail

## Integrity limits
SHA-256 detects accidental/tampered payload changes but does **not** authenticate source instruments, guarantee that observations came from real liquid, or prevent deletion of files. Preserve original raw data and independent provenance where available.
