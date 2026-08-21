"""Memory leak / unsafe memory pattern detector (static)."""
import re
from pathlib import Path
from typing import Dict, Any, List

PATTERNS = [
    (r"\bmalloc\s*\(", "malloc without visible free — possible leak"),
    (r"\bcalloc\s*\(", "calloc without visible free — possible leak"),
    (r"\brealloc\s*\(", "realloc — check for leak on failure"),
    (r"\bnew\s+\w+", "C++ new — ensure matching delete"),
    (r"\bnew\s*\[", "C++ new[] — ensure matching delete[]"),
    (r"\bstrcpy\s*\(", "strcpy is unsafe — use strncpy/strlcpy"),
    (r"\bstrcat\s*\(", "strcat is unsafe — use strncat"),
    (r"\bgets\s*\(", "gets is dangerous — never use"),
    (r"\bsprintf\s*\(", "sprintf is unsafe — use snprintf"),
    (r"\bmemcpy\s*\([^)]+\)", "memcpy — verify bounds"),
]


def check_memory_issues(filepath: Path) -> Dict[str, Any]:
    result = {
        "name": "memory",
        "status": "pass",
        "issues": [],
        "message": "",
    }

    try:
        text = filepath.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        issues: List[Dict] = []

        for i, line in enumerate(lines, 1):
            for pat, msg in PATTERNS:
                if re.search(pat, line):
                    issues.append({
                        "line": i,
                        "severity": "memory",
                        "code": line.strip()[:120],
                        "detail": msg,
                    })

        # Simple heuristic: malloc count vs free count
        mallocs = len(re.findall(r"\b(malloc|calloc|realloc)\s*\(", text))
        frees = len(re.findall(r"\bfree\s*\(", text))
        news = len(re.findall(r"\bnew\s+", text))
        deletes = len(re.findall(r"\bdelete\s+", text))

        if mallocs > frees:
            issues.append({
                "line": 0,
                "severity": "memory",
                "detail": f"Possible leak: {mallocs} alloc vs {frees} free",
            })
        if news > deletes:
            issues.append({
                "line": 0,
                "severity": "memory",
                "detail": f"Possible leak: {news} new vs {deletes} delete",
            })

        result["issues"] = issues
        if issues:
            result["status"] = "fail"
            result["message"] = f"{len(issues)} memory-related warning(s)"
        else:
            result["message"] = "No obvious memory issues"
    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)

    return result
