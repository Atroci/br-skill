#!/usr/bin/env python3
"""Valida invariantes locais da BR Skill sem rede nem dependências externas."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = ROOT / "SKILL.md"
CHECKER_PATH = Path(__file__).resolve()
MARKDOWN_LINK = re.compile(r"\]\(\s*(?:<([^>]+)>|([^\s)]+))")
FRONTMATTER_FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$")

SENSITIVE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private-key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    (
        "github-token",
        re.compile(r"\b(?:gh[pousr]|github_pat)_[A-Za-z0-9_]{20,}\b"),
    ),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{15,}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    (
        "credential-assignment",
        re.compile(
            r'''(?i)\b(?:api[_-]?key|access[_-]?token|secret|password|passwd)\b\s*[:=]\s*["'][^"'\n]{8,}["']'''
        ),
    ),
    (
        "cpf",
        re.compile(r"\b\d{3}[.\s]?\d{3}[.\s]?\d{3}[-\s]?\d{2}\b"),
    ),
    (
        "cnpj",
        re.compile(r"\b\d{2}[.\s]?\d{3}[.\s]?\d{3}[/.\s]?\d{4}[-\s]?\d{2}\b"),
    ),
    (
        "email",
        re.compile(r"\b[A-Za-z0-9][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    ),
)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if path.is_file() and not path.is_symlink() and path.resolve() != CHECKER_PATH
    )


def check_frontmatter(errors: list[str]) -> None:
    text = read_text(SKILL_PATH)
    if text is None:
        errors.append("SKILL.md: arquivo ausente ou ilegível")
        return

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append("SKILL.md:1: frontmatter YAML ausente")
        return

    end = next((index for index, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if end is None:
        errors.append("SKILL.md:1: frontmatter YAML sem fechamento")
        return

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        match = FRONTMATTER_FIELD.match(line)
        if match:
            fields[match.group(1)] = match.group(2).strip()

    for field in ("name", "description"):
        if not fields.get(field):
            errors.append(f"SKILL.md:1: frontmatter sem campo {field}")


def check_links(errors: list[str]) -> None:
    for source in markdown_files():
        text = read_text(source)
        if text is None:
            continue

        in_fence = False
        for line_number, line in enumerate(text.splitlines(), 1):
            if re.match(r"^\s*```", line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            for match in MARKDOWN_LINK.finditer(line):
                target = (match.group(1) or match.group(2) or "").strip()
                parts = urlsplit(target)
                if parts.scheme or target.startswith("//") or not parts.path:
                    continue

                candidate = (source.parent / unquote(parts.path)).resolve()
                try:
                    candidate.relative_to(ROOT)
                except ValueError:
                    errors.append(f"{source.relative_to(ROOT)}:{line_number}: link relativo fora do repositório")
                    continue
                if not candidate.exists():
                    errors.append(f"{source.relative_to(ROOT)}:{line_number}: link relativo aponta para arquivo ausente")


def text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.is_symlink() or path.resolve() == CHECKER_PATH:
            continue
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        files.append(path)
    return sorted(files)


def check_sensitive_patterns(errors: list[str]) -> None:
    for path in text_files():
        text = read_text(path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for name, pattern in SENSITIVE_PATTERNS:
                if pattern.search(line):
                    errors.append(f"{path.relative_to(ROOT)}:{line_number}: padrão sensível detectado ({name})")


def main() -> int:
    errors: list[str] = []
    check_frontmatter(errors)
    check_links(errors)
    check_sensitive_patterns(errors)

    if errors:
        print(f"Falha: {len(errors)} problema(s) de qualidade.")
        for error in errors:
            print(error)
        return 1

    print("OK: frontmatter, links relativos, referências e padrões sensíveis validados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
