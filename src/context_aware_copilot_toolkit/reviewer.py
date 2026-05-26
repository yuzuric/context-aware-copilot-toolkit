"""Code review engine: parses diffs and queries MiMo for issues."""
import re
from dataclasses import dataclass
from .client import MiMoClient


@dataclass
class Finding:
    file: str
    line: int
    severity: str  # info | warn | error
    message: str
    rule: str = "general"


class CodeReviewer:
    SEVERITY_LEVELS = {"info": 0, "warn": 1, "error": 2}

    def __init__(self, model: str, api_key: str):
        self.client = MiMoClient(model=model, api_key=api_key)

    def review(self, diff: str, severity: str = "warn") -> list[Finding]:
        threshold = self.SEVERITY_LEVELS[severity]
        files = self._parse_diff(diff)
        findings: list[Finding] = []

        for file, hunks in files.items():
            prompt = self._build_prompt(file, hunks)
            response = self.client.chat_sync(prompt)
            for f in self._extract_findings(response, file):
                if self.SEVERITY_LEVELS[f.severity] >= threshold:
                    findings.append(f)

        return findings

    def _parse_diff(self, diff: str) -> dict[str, list[tuple[int, str]]]:
        result: dict[str, list[tuple[int, str]]] = {}
        current_file = None
        current_line = 0
        for line in diff.split("\n"):
            if line.startswith("+++ b/"):
                current_file = line[6:]
                result[current_file] = []
            elif line.startswith("@@"):
                m = re.search(r"\+(\d+)", line)
                if m:
                    current_line = int(m.group(1))
            elif line.startswith("+") and current_file and not line.startswith("+++"):
                result[current_file].append((current_line, line[1:]))
                current_line += 1
        return result

    def _build_prompt(self, file: str, hunks: list[tuple[int, str]]) -> str:
        body = "\n".join(f"{ln}: {code}" for ln, code in hunks)
        return f"Review this diff in {file}:\n{body}\n\nReturn findings as: SEVERITY|LINE|RULE|MESSAGE"

    def _extract_findings(self, response: str, file: str) -> list[Finding]:
        findings = []
        for line in response.strip().split("\n"):
            parts = line.split("|", 3)
            if len(parts) == 4:
                sev, ln, rule, msg = [p.strip() for p in parts]
                if sev.lower() in self.SEVERITY_LEVELS:
                    findings.append(Finding(file=file, line=int(ln), severity=sev.lower(), message=msg, rule=rule))
        return findings
