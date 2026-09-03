#!/usr/bin/env python3
"""Static validation for the IDA Dracula theme."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_THEME = ROOT / "themes" / "dracula" / "theme.css"
COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
DEF_RE = re.compile(r"@def\s+([A-Za-z_][\w-]*)\s+([^;]+);")
REF_RE = re.compile(r"\$\{([A-Za-z_][\w-]*)\}")
QPROPERTY_RE = re.compile(r"\bqproperty-[A-Za-z0-9_-]+\b")
HEX_RE = re.compile(r"#[0-9A-Fa-f]+")

REQUIRED_DEFINITIONS = {
    "dracula_bg": "#282A36",
    "dracula_current": "#44475A",
    "dracula_fg": "#F8F8F2",
    "dracula_comment": "#6272A4",
    "dracula_cyan": "#8BE9FD",
    "dracula_green": "#50FA7B",
    "dracula_orange": "#FFB86C",
    "dracula_pink": "#FF79C6",
    "dracula_purple": "#BD93F9",
    "dracula_red": "#FF5555",
    "dracula_yellow": "#F1FA8C",
}

REQUIRED_SELECTORS = (
    "CustomIDAMemo",
    "CustomIDAMemo[debugging=",
    "GraphMiniView",
    "TextArrows",
    "TCpuRegs",
    "navband_t",
    "text_area_t",
    "chooser_widget_t",
    "log_widget_t",
    "diff_fringe_t",
)


def fail(message: str) -> None:
    raise ValueError(message)


def parse_hex(value: str) -> tuple[int, int, int]:
    value = value.strip()
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        fail(f"expected #RRGGBB color, got {value!r}")
    return tuple(int(value[index : index + 2], 16) for index in (1, 3, 5))  # type: ignore[return-value]


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    channels = []
    for channel in rgb:
        normalized = channel / 255.0
        channels.append(
            normalized / 12.92
            if normalized <= 0.04045
            else ((normalized + 0.055) / 1.055) ** 2.4
        )
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(first: str, second: str) -> float:
    one = relative_luminance(parse_hex(first))
    two = relative_luminance(parse_hex(second))
    lighter, darker = max(one, two), min(one, two)
    return (lighter + 0.05) / (darker + 0.05)


def validate(theme: Path, ida_dir: Path | None) -> None:
    if not theme.is_file():
        fail(f"theme not found: {theme}")

    source = theme.read_text(encoding="utf-8")
    clean = COMMENT_RE.sub("", source)

    if not re.search(r'^\s*@importtheme\s+"dark"\s*;', clean):
        fail('theme must begin by importing IDA\'s "dark" theme')

    depth = 0
    for offset, character in enumerate(clean):
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth < 0:
                fail(f"unexpected closing brace at byte {offset}")
    if depth:
        fail(f"unbalanced braces: final depth is {depth}")

    definitions: dict[str, str] = {}
    for name, value in DEF_RE.findall(clean):
        if name in definitions:
            fail(f"duplicate @def: {name}")
        definitions[name] = value.strip()

    undefined = sorted(set(REF_RE.findall(clean)) - definitions.keys())
    if undefined:
        fail("undefined theme variables: " + ", ".join(undefined))

    for name, expected in REQUIRED_DEFINITIONS.items():
        actual = definitions.get(name)
        if actual is None or actual.upper() != expected.upper():
            fail(f"{name} must be {expected}, got {actual!r}")

    malformed_hex = sorted(
        color for color in set(HEX_RE.findall(clean)) if len(color) not in (4, 7, 9)
    )
    if malformed_hex:
        fail("malformed hex colors: " + ", ".join(malformed_hex))

    for selector in REQUIRED_SELECTORS:
        if selector not in clean:
            fail(f"required selector is missing: {selector}")

    qproperties = set(QPROPERTY_RE.findall(clean))
    if not qproperties:
        fail("no IDA qproperty declarations found")

    if ida_dir is not None:
        base = ida_dir / "themes" / "_base" / "theme.css"
        dark = ida_dir / "themes" / "dark" / "theme.css"
        missing_files = [str(path) for path in (base, dark) if not path.is_file()]
        if missing_files:
            fail("IDA theme files not found: " + ", ".join(missing_files))
        ida_source = "\n".join(path.read_text(encoding="utf-8") for path in (base, dark))
        supported = set(QPROPERTY_RE.findall(ida_source))
        unknown = sorted(qproperties - supported)
        if unknown:
            fail(
                f"{len(unknown)} properties are absent from {ida_dir}: "
                + ", ".join(unknown)
            )

    background = definitions["dracula_bg"]
    ratios = {
        "foreground/background": contrast(definitions["dracula_fg"], background),
        "comment/background": contrast(definitions["dracula_comment"], background),
        "cyan/background": contrast(definitions["dracula_cyan"], background),
        "green/background": contrast(definitions["dracula_green"], background),
        "pink/background": contrast(definitions["dracula_pink"], background),
        "yellow/background": contrast(definitions["dracula_yellow"], background),
    }
    if ratios["foreground/background"] < 7.0:
        fail("primary foreground contrast is below 7:1")
    if ratios["comment/background"] < 3.0:
        fail("comment contrast is below 3:1")

    print(f"OK: {theme}")
    print(f"  variables: {len(definitions)}")
    print(f"  IDA properties: {len(qproperties)}")
    if ida_dir is not None:
        print(f"  property reference: {ida_dir}")
    print("  contrast: " + ", ".join(f"{name}={ratio:.2f}:1" for name, ratio in ratios.items()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theme", type=Path, default=DEFAULT_THEME)
    parser.add_argument(
        "--ida-dir",
        type=Path,
        default=Path(os.environ["IDA_DIR"]) if os.environ.get("IDA_DIR") else None,
        help="optional IDA installation used to verify qproperty names",
    )
    args = parser.parse_args()
    try:
        validate(args.theme.resolve(), args.ida_dir.resolve() if args.ida_dir else None)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
