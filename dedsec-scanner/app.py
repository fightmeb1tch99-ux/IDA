#!/usr/bin/env python3
"""DEDSEC Web UI — upload code, get audit report."""

import os
import tempfile
from pathlib import Path
from flask import Flask, request, render_template, jsonify
from scanner import scan_file

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    if "file" not in request.files and "code" not in request.form:
        return jsonify({"error": "No file or code provided"}), 400

    suffix = ".txt"
    if "file" in request.files and request.files["file"].filename:
        f = request.files["file"]
        suffix = Path(f.filename).suffix or ".txt"
        data = f.read()
    else:
        data = request.form.get("code", "").encode("utf-8")
        lang = request.form.get("lang", "c")
        suffix = {"c": ".c", "cpp": ".cpp", "py": ".py", "js": ".js"}.get(lang, ".txt")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)

    try:
        report = scan_file(tmp_path)
        return jsonify(report)
    finally:
        tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
