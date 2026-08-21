"""Security pattern scanner."""
import re
from pathlib import Path
from typing import Dict, Any, List

RULES = [
    (r"\bsystem\s*\(", "high", "system() — command injection risk"),
    (r"\bpopen\s*\(", "high", "popen() — command injection risk"),
    (r"\bexec[lvpe]*\s*\(", "high", "exec* — command injection risk"),
    (r"\beval\s*\(", "high", "eval() — code injection risk"),
    (r"\bexec\s*\(", "high", "exec() — code injection risk"),
    (r"password\s*=\s*['\"][^'\"]+['\"]", "critical", "Hardcoded password"),
    (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "critical", "Hardcoded API key"),
    (r"secret\s*=\s*['\"][^'\"]+['\"]", "critical", "Hardcoded secret"),
    (r"AKIA[0-9A-Z]{16}", "critical", "Possible AWS Access Key"),
    (r"-----BEGIN (RSA |OPENSSH )?PRIVATE KEY-----", "critical", "Private key in source"),
    (r"\bmd5\s*\(", "medium", "MD5 is weak — use SHA-256+"),
    (r"\bsha1\s*\(", "medium", "SHA1 is weak"),
    (r"verify\s*=\s*False", "high", "SSL verification disabled"),
    (r"curl_easy_setopt.*CURLOPT_SSL_VERIFYPEER\s*,\s*0", "high", "SSL verify disabled"),
    (r"\bstrcpy\s*\(", "medium", "Buffer overflow risk (strcpy)"),
    (r"\bgets\s*\(", "critical", "gets() — buffer overflow, never use"),
    (r"SELECT\s+.*\s+FROM\s+.*\+|\"\s*\+|f\".*SELECT", "high", "Possible SQL injection"),
    (r"innerHTML\s*=", "medium", "XSS risk via innerHTML"),
    (r"dangerouslySetInnerHTML", "medium", "React XSS risk"),
    (r"pickle\.loads?\s*\(", "high", "pickle can execute arbitrary code"),
    (r"yaml\.load\s*\([^)]*\)", "high", "yaml.load without Loader is unsafe"),
    (r"subprocess\.(call|run|Popen).*shell\s*=\s*True", "high", "shell=True — injection risk"),
]


def check_security(filepath: Path) -> Dict[str, Any]:
    result = {
        "name": "security",
        "status": "pass",
        "issues": [],
        "message": "",
    }

    try:
        text = filepath.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        issues: List[Dict] = []

        for i, line in enumerate(lines, 1):
            for pat, severity, msg in RULES:
                if re.search(pat, line, re.IGNORECASE):
                    issues.append({
                        "line": i,
                        "severity": severity,
                        "code": line.strip()[:120],
                        "detail": msg,
                    })

        result["issues"] = issues
        if any(i["severity"] == "critical" for i in issues):
            result["status"] = "critical"
            result["message"] = f"{len(issues)} security issue(s) — CRITICAL found"
        elif issues:
            result["status"] = "fail"
            result["message"] = f"{len(issues)} security warning(s)"
        else:
            result["message"] = "No obvious security issues"
    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)

    return result
