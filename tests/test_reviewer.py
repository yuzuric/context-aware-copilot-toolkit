"""Tests for code reviewer."""
from context_aware_copilot_toolkit.reviewer import CodeReviewer, Finding


def test_finding_severity():
    f = Finding(file="x.py", line=10, severity="warn", message="unused var")
    assert f.severity == "warn"
    assert f.rule == "general"


def test_diff_parsing():
    reviewer = CodeReviewer(model="mimo-7b", api_key="test")
    diff = """\
diff --git a/x.py b/x.py
+++ b/x.py
@@ -1,3 +1,4 @@
+import os
 def foo():
     pass
"""
    parsed = reviewer._parse_diff(diff)
    assert "x.py" in parsed
    assert any("import os" in code for _, code in parsed["x.py"])
