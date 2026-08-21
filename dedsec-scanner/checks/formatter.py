"""clang-format style checker."""
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any


def check_clang_format(filepath: Path) -> Dict[str, Any]:
    result = {
        "name": "clang-format",
        "status": "skip",
        "issues": [],
        "message": "",
    }

    if not shutil.which("clang-format"):
        result["message"] = "clang-format not installed — skipped"
        return result

    try:
        # Check if file would change
        proc = subprocess.run(
            ["clang-format", "--dry-run", "--Werror", str(filepath)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if proc.returncode == 0:
            result["status"] = "pass"
            result["message"] = "Style OK"
        else:
            result["status"] = "fail"
            result["message"] = "Formatting issues detected"
            # Get diff
            diff = subprocess.run(
                ["clang-format", str(filepath)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            result["issues"].append({
                "severity": "style",
                "detail": "File does not match clang-format style",
                "hint": "Run: clang-format -i " + filepath.name,
            })
            if diff.stdout:
                result["formatted_preview"] = diff.stdout[:2000]
    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)

    return result
