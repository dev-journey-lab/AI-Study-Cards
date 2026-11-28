#!/usr/bin/env python3
"""Minimal red-team / blue-team deterministic guardrail verification script.

Run:
    python3 scripts/verify_ai_guardrails.py
"""

from pathlib import Path
import re
import sys

ALLOWED_TOPICS = {"git", "api", "react", "security", "mcp"}
SECRET_PATTERN = re.compile(r"(sk-[A-Za-z0-9_-]{8,}|Bearer\s+[A-Za-z0-9._-]{8,})")


def validate_topic(raw) -> tuple[bool, str]:
    """Deterministic input gate: only allow known string topics."""
    if not isinstance(raw, str):
        return False, "400: topic must be a string"
    if len(raw) == 0 or len(raw) > 50:
        return False, "400: invalid topic length"
    if raw not in ALLOWED_TOPICS:
        return False, "403: topic not in allowlist"
    return True, "200: ok"


def validate_readonly_path(base_dir: Path, rel_path) -> tuple[bool, str]:
    """Deterministic path gate: reject non-strings, absolute paths, '..' and dotfiles."""
    if not isinstance(rel_path, str) or not rel_path:
        return False, "400: invalid path"
    p = Path(rel_path)
    if p.is_absolute() or ".." in p.parts:
        return False, "403: path traversal blocked"
    if any(part.startswith(".") for part in p.parts):
        return False, "403: hidden/dotfile blocked"
    resolved = (base_dir / p).resolve()
    try:
        resolved.relative_to(base_dir.resolve())
    except ValueError:
        return False, "403: escaped workspace"
    return True, "200: ok"


def redact_output(text: str) -> str:
    """Output guardrail: mask accidental secret patterns before returning to client."""
    return SECRET_PATTERN.sub("[REDACTED_SECRET]", str(text))[:2000]


def main() -> int:
    workspace = Path(__file__).resolve().parent.parent

    # 1. Red-team topic inputs (must be rejected)
    bad_topics = [["git"], {"topic": "git"}, "", "../.env", "git; rm -rf /", "a" * 51, None]
    for payload in bad_topics:
        ok, msg = validate_topic(payload)
        assert not ok, f"Expected reject for {payload!r}, got {msg}"

    # Valid topic
    ok, msg = validate_topic("git")
    assert ok, f"Expected allow for 'git', got {msg}"

    # 2. Red-team file paths (must be rejected)
    bad_paths = ["../.env", ".env", "/etc/passwd", "sub/../../secret.txt", ["index.html"], ""]
    for payload in bad_paths:
        ok, msg = validate_readonly_path(workspace, payload)
        assert not ok, f"Expected reject for path {payload!r}, got {msg}"

    # Valid workspace file
    ok, msg = validate_readonly_path(workspace, "index.html")
    assert ok, f"Expected allow for 'index.html', got {msg}"

    # 3. Output redaction check
    leaked = "Debug token: sk-live-1234567890abcdef and Bearer eyJhbGciOiJIUzI1NiJ9"
    cleaned = redact_output(leaked)
    assert "sk-live-" not in cleaned and "eyJhbGci" not in cleaned
    assert cleaned.count("[REDACTED_SECRET]") == 2

    print("ALL AI GUARDRAIL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
