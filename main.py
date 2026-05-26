"""
Code review CLI: analyzes diffs and emits actionable suggestions via MiMo.
"""
import argparse
import sys
from pathlib import Path
from context_aware_copilot_toolkit.reviewer import CodeReviewer
from context_aware_copilot_toolkit.config import load_config


def main() -> int:
    parser = argparse.ArgumentParser(description="AI code reviewer")
    parser.add_argument("--diff", type=Path, required=True, help="Path to diff file")
    parser.add_argument("--severity", default="warn", choices=["info", "warn", "error"])
    args = parser.parse_args()

    config = load_config("config.yaml")
    reviewer = CodeReviewer(model=config["model"], api_key=config["api_key"])

    diff_text = args.diff.read_text()
    findings = reviewer.review(diff_text, severity=args.severity)

    for f in findings:
        print(f"[{{f.severity.upper()}}] {{f.file}}:{{f.line}} {{f.message}}")

    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
