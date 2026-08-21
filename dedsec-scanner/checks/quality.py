"""Basic code quality metrics."""
import re
from pathlib import Path
from typing import Dict, Any


def check_code_quality(filepath: Path) -> Dict[str, Any]:
    result = {
        "name": "quality",
        "status": "pass",
        "issues": [],
        "metrics": {},
        "message": "",
    }

    try:
        text = filepath.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        total = len(lines)
        blank = sum(1 for l in lines if not l.strip())
        comments = sum(1 for l in lines if l.strip().startswith(("//", "#", "/*", "*")))
        code_lines = total - blank - comments
        long_lines = [i + 1 for i, l in enumerate(lines) if len(l) > 120]
        todo = [i + 1 for i, l in enumerate(lines) if re.search(r"\b(TODO|FIXME|XXX|HACK)\b", l, re.I)]

        result["metrics"] = {
            "total_lines": total,
            "code_lines": code_lines,
            "blank_lines": blank,
            "comment_lines": comments,
            "long_lines_count": len(long_lines),
            "todo_count": len(todo),
        }

        issues = []
        if len(long_lines) > 5:
            issues.append({
                "severity": "style",
                "detail": f"{len(long_lines)} lines longer than 120 chars",
                "lines": long_lines[:10],
            })
        if todo:
            issues.append({
                "severity": "info",
                "detail": f"{len(todo)} TODO/FIXME markers",
                "lines": todo[:10],
            })
        if code_lines > 0 and comments / max(code_lines, 1) < 0.05 and code_lines > 50:
            issues.append({
                "severity": "info",
                "detail": "Very low comment ratio",
            })

        result["issues"] = issues
        if issues:
            result["status"] = "warn"
            result["message"] = f"{len(issues)} quality note(s)"
        else:
            result["message"] = "Quality looks fine"
    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)

    return result
