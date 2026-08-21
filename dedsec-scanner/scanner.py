#!/usr/bin/env python3
"""
DEDSEC Code Audit System
Scan source files for style, memory, security and quality issues.
"""

import argparse
import json
import sys
from pathlib import Path
from checks import (
    check_clang_format,
    check_memory_issues,
    check_security,
    check_code_quality,
)

BANNER = r"""
 ____  _____ ____  ____  _____ ____ 
|  _ \| ____|  _ \/ ___|| ____/ ___|
| | | |  _| | | | \___ \|  _|| |    
| |_| | |___| |_| |___) | |__| |___ 
|____/|_____|____/|____/|_____\____|
        CODE AUDIT SYSTEM v1.0
"""


def scan_file(filepath: Path) -> dict:
    return {
        "file": str(filepath),
        "checks": {
            "clang_format": check_clang_format(filepath),
            "memory": check_memory_issues(filepath),
            "security": check_security(filepath),
            "quality": check_code_quality(filepath),
        },
    }


def print_report(report: dict, verbose: bool = False):
    print(BANNER)
    print(f"[*] TARGET: {report['file']}\n")

    status_icon = {
        "pass": "[+]",
        "fail": "[-]",
        "critical": "[!]",
        "warn": "[~]",
        "skip": "[ ]",
        "error": "[x]",
    }

    for name, check in report["checks"].items():
        icon = status_icon.get(check["status"], "[?]")
        print(f"  {icon} {name.upper():<14} {check['status'].upper():<10} {check['message']}")
        if verbose or check["status"] in ("fail", "critical", "warn"):
            for issue in check.get("issues", [])[:15]:
                line = issue.get("line", "?")
                sev = issue.get("severity", "")
                detail = issue.get("detail", "")
                code = issue.get("code", "")
                print(f"       L{line:>4} [{sev}] {detail}")
                if code:
                    print(f"             > {code}")
        print()

    # Summary
    statuses = [c["status"] for c in report["checks"].values()]
    if "critical" in statuses:
        print("[!] CRITICAL ISSUES FOUND — fix immediately")
        return 2
    if "fail" in statuses:
        print("[-] Issues found")
        return 1
    print("[+] All clear")
    return 0


def main():
    parser = argparse.ArgumentParser(description="DEDSEC Code Audit System")
    parser.add_argument("file", help="Source file to scan")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        print(f"[!] File not found: {path}", file=sys.stderr)
        sys.exit(1)

    report = scan_file(path)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        statuses = [c["status"] for c in report["checks"].values()]
        sys.exit(2 if "critical" in statuses else 1 if "fail" in statuses else 0)
    else:
        code = print_report(report, args.verbose)
        sys.exit(code)


if __name__ == "__main__":
    main()
