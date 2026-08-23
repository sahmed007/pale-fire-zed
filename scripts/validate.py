#!/usr/bin/env python3
"""Validate the generated Zed theme, manifest, and syntax capture coverage."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parent.parent
THEME_PATH = ROOT / "themes" / "pale-fire.json"
SCHEMA_PATH = ROOT / "scripts" / "vendor" / "zed-theme-v0.2.0.json"
MANIFEST_PATH = ROOT / "extension.toml"
EXPECTED_THEMES = {
    "Pale Fire",
    "Pale Fire Darker",
    "Pale Fire High Contrast",
    "Pale Fire Stealth",
}
EXPECTED_ROLE_COLORS = {
    "Pale Fire": {"named_type": "#B4A5D1", "symbol": "#B9AF80", "comment": "#95B595", "doc": "#A9CAA9", "unsafe": "#E4AEAD"},
    "Pale Fire Darker": {"named_type": "#A78FD3", "symbol": "#AF9E51", "comment": "#568E58", "doc": "#75AE77", "unsafe": "#E69495"},
    "Pale Fire High Contrast": {"named_type": "#B3A1D6", "symbol": "#B9AC72", "comment": "#85AC86", "doc": "#9FC59F", "unsafe": "#ECAAAA"},
    "Pale Fire Stealth": {"named_type": "#A799C4", "symbol": "#ACA274", "comment": "#739673", "doc": "#89AD89", "unsafe": "#D49E9E"},
}
NAMED_TYPE_CAPTURES = {
    "class", "enum", "struct", "type", "type.alias", "type.class",
    "type.class.definition", "type.definition", "type.enum", "type.enum.definition",
    "type.event", "type.struct", "type.struct.definition", "type.super", "type.union",
}
PERCEPTUAL_DISTANCE_RULES = {
    ("type", "function"): 0.12,
    ("symbol", "string"): 0.075,
    ("comment", "comment.doc"): 0.06,
}
COLOR = re.compile(r"^#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")

# Zed's documented captures, its default semantic-token style candidates,
# representative dotted captures from major grammars, and all captures used by
# the official Ruby extension that need more than a generic base fallback.
CAPTURES = {
    "attribute", "boolean", "comment", "comment.doc", "comment.documentation",
    "constant", "constant.builtin", "constant.numeric", "constructor", "decorator",
    "diff.delta", "diff.minus", "diff.plus", "embedded", "emphasis",
    "emphasis.strong", "enum", "function", "function.annotation", "function.builtin",
    "function.call", "function.decorator", "function.definition", "function.macro",
    "function.method", "function.method.builtin", "function.method.definition", "hint",
    "interface", "keyword", "keyword.control", "keyword.control.conditional",
    "keyword.control.repeat", "keyword.control.return", "keyword.directive",
    "keyword.exception", "keyword.function", "keyword.import", "keyword.modifier",
    "keyword.operator", "label", "lifetime", "link_text", "link_uri", "macro",
    "module", "namespace", "number", "operator", "preproc", "predictive", "primary",
    "property", "property.definition", "punctuation", "punctuation.bracket",
    "punctuation.delimiter", "punctuation.list_marker", "punctuation.special", "string",
    "string.doc", "string.escape", "string.format", "string.regex", "string.regexp",
    "string.special", "string.special.path", "string.special.symbol", "struct", "symbol", "tag",
    "tag.doctype", "text.literal", "title", "type", "type.alias", "type.builtin",
    "type.class", "type.class.definition", "type.definition", "type.enum",
    "type.enum.definition", "type.enum.member", "type.event", "type.interface",
    "type.interface.definition", "type.parameter", "type.parameter.definition",
    "type.struct", "type.struct.definition", "type.super", "type.trait", "type.union",
    "unsafe", "unresolvedReference", "variable", "variable.builtin", "variable.member",
    "variable.mutable", "variable.parameter", "variable.parameter.keyword",
    "variable.special", "variable.special.instance", "variant",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def resolve_capture(capture: str, styles: dict) -> str | None:
    candidate = capture
    while candidate:
        if candidate in styles:
            return candidate
        candidate = candidate.rpartition(".")[0]
    return None


def relative_luminance(color: str) -> float:
    components = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        component / 12.92
        if component <= 0.04045
        else ((component + 0.055) / 1.055) ** 2.4
        for component in components
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first: str, second: str) -> float:
    lighter, darker = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def oklab(color: str) -> tuple[float, float, float]:
    red, green, blue = [
        int(color[index:index + 2], 16) / 255
        for index in (1, 3, 5)
    ]
    red, green, blue = [
        component / 12.92
        if component <= 0.04045
        else ((component + 0.055) / 1.055) ** 2.4
        for component in (red, green, blue)
    ]
    lightness = (0.4122214708 * red + 0.5363325363 * green + 0.0514459929 * blue) ** (1 / 3)
    medium = (0.2119034982 * red + 0.6806995451 * green + 0.1073969566 * blue) ** (1 / 3)
    short = (0.0883024619 * red + 0.2817188376 * green + 0.6299787005 * blue) ** (1 / 3)
    return (
        0.2104542553 * lightness + 0.793617785 * medium - 0.0040720468 * short,
        1.9779984951 * lightness - 2.428592205 * medium + 0.4505937099 * short,
        0.0259040371 * lightness + 0.7827717662 * medium - 0.8086757660 * short,
    )


def perceptual_distance(first: str, second: str) -> float:
    first_lab = oklab(first)
    second_lab = oklab(second)
    return sum((left - right) ** 2 for left, right in zip(first_lab, second_lab)) ** 0.5


def iter_colors(value, path="theme"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from iter_colors(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_colors(child, f"{path}[{index}]")
    elif isinstance(value, str) and value.startswith("#"):
        yield path, value


def main() -> int:
    theme = load_json(THEME_PATH)
    schema = load_json(SCHEMA_PATH)

    errors = sorted(Draft7Validator(schema).iter_errors(theme), key=lambda error: list(error.path))
    if errors:
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            print(f"schema: {location}: {error.message}", file=sys.stderr)
        return 1

    with MANIFEST_PATH.open("rb") as handle:
        manifest = tomllib.load(handle)
    assert manifest["id"] == "pale-fire-theme", "unexpected extension id"
    assert manifest["name"] == "Pale Fire", "unexpected extension name"
    assert manifest["version"] == "0.1.0", "unexpected extension version"
    assert manifest["schema_version"] == 1, "unexpected manifest schema"
    assert "zed" not in manifest["name"].lower(), "marketplace name cannot contain Zed"

    names = {entry["name"] for entry in theme["themes"]}
    assert names == EXPECTED_THEMES, f"unexpected theme variants: {sorted(names)}"

    style_keys = None
    for entry in theme["themes"]:
        styles = entry["style"]["syntax"]
        assert len(styles) >= 100, f"{entry['name']} has an incomplete syntax map"
        bold_styles = sorted(capture for capture, style in styles.items() if "font_weight" in style)
        assert not bold_styles, f"{entry['name']} contains bold styles: {', '.join(bold_styles)}"
        missing = sorted(capture for capture in CAPTURES if resolve_capture(capture, styles) is None)
        assert not missing, f"{entry['name']} has unresolved captures: {', '.join(missing)}"
        current_keys = set(styles)
        if style_keys is None:
            style_keys = current_keys
        else:
            assert current_keys == style_keys, f"{entry['name']} syntax keys differ from the family"

        expected = EXPECTED_ROLE_COLORS[entry["name"]]
        named_type_color = styles["type"]["color"]
        symbol_color = styles["symbol"]["color"]
        assert named_type_color == expected["named_type"], f"{entry['name']} has an unexpected named-type color"
        assert symbol_color == expected["symbol"], f"{entry['name']} has an unexpected symbol color"
        assert styles["comment"]["color"] == expected["comment"], f"{entry['name']} has an unexpected comment color"
        assert styles["comment.doc"]["color"] == expected["doc"], f"{entry['name']} has an unexpected documentation color"
        assert styles["unsafe"]["color"] == expected["unsafe"], f"{entry['name']} has an unexpected unsafe color"

        mismatched_named_types = sorted(
            capture for capture in NAMED_TYPE_CAPTURES
            if styles[capture]["color"] != named_type_color
        )
        assert not mismatched_named_types, (
            f"{entry['name']} has inconsistent named-type captures: "
            f"{', '.join(mismatched_named_types)}"
        )

        function_color = styles["function"]["color"]
        builtin_type_color = styles["type.builtin"]["color"]
        string_color = styles["string"]["color"]
        assert named_type_color != function_color, f"{entry['name']} types collapse into functions"
        assert named_type_color != builtin_type_color, f"{entry['name']} named and built-in types collapse"
        assert named_type_color != styles["type.parameter"]["color"], (
            f"{entry['name']} named types collapse into type parameters"
        )
        assert symbol_color != string_color, f"{entry['name']} symbols collapse into strings"
        assert symbol_color != named_type_color, f"{entry['name']} symbols collapse into named types"
        assert symbol_color != function_color, f"{entry['name']} symbols collapse into functions"
        assert styles["string.special.symbol"]["color"] == symbol_color, (
            f"{entry['name']} special symbols do not use the symbol role"
        )
        assert styles["constructor"]["color"] == function_color, (
            f"{entry['name']} constructors do not use the function role"
        )
        for capture in ("type.interface", "type.interface.definition", "type.trait"):
            assert styles[capture]["color"] == builtin_type_color, (
                f"{entry['name']} {capture} does not use the teal contract-type role"
            )
            assert styles[capture].get("font_style") == "italic", (
                f"{entry['name']} {capture} is not italic"
            )

        background = entry["style"]["editor.background"]
        for capture, style in styles.items():
            ratio = contrast_ratio(background, style["color"])
            assert ratio >= 4.5, f"{entry['name']} {capture} contrast is only {ratio:.2f}:1"

        for (first, second), minimum in PERCEPTUAL_DISTANCE_RULES.items():
            distance = perceptual_distance(styles[first]["color"], styles[second]["color"])
            assert distance >= minimum, (
                f"{entry['name']} {first} and {second} are perceptually too close "
                f"({distance:.3f} < {minimum:.3f})"
            )

    invalid_colors = [(path, value) for path, value in iter_colors(theme) if not COLOR.fullmatch(value)]
    assert not invalid_colors, f"invalid colors: {invalid_colors}"

    print(
        f"Validated {len(theme['themes'])} themes, {len(style_keys or [])} syntax styles, "
        f"and {len(CAPTURES)} representative captures against Zed theme schema v0.2.0."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
