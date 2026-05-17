from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def check_gate(metrics_path: Path, policy_path: Path) -> None:
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))

    metric_name = policy["offline"]["primary_metric"]
    min_absolute = float(policy["offline"]["thresholds"]["min_absolute"])
    observed = float(metrics[metric_name])

    print(f"model_gate: {metric_name}={observed:.4f}, threshold={min_absolute:.4f}")
    if observed < min_absolute:
        raise SystemExit(f"model_gate failed: {metric_name} below threshold")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate model metrics against policy.")
    parser.add_argument("--metrics", default="reports/offline_metrics.json")
    parser.add_argument("--policy", default="policies/model_policy.yaml")
    args = parser.parse_args()
    check_gate(Path(args.metrics), Path(args.policy))


if __name__ == "__main__":
    main()
