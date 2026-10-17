#!/usr/bin/env python3
"""Validate the generated Zed theme, manifest, and syntax capture coverage."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

from jsonschema import Draft7Validator

from contrast import MIN_TEXT_CONTRAST, contrast_cases, contrast_ratio, relative_luminance, diagnostic_indicator_cases

ROOT = Path(__file__).resolve().parent.parent
THEME_PATH = ROOT / "themes" / "pale-fire.json"
SCHEMA_PATH = ROOT / "scripts" / "vendor" / "zed-theme-v0.2.0.json"
MANIFEST_PATH = ROOT / "extension.toml"
EXPECTED_THEMES = {
    "Pale Fire",
    "Pale Fire Darker",
    "Pale Fire High Contrast",
    "Pale Fire Stealth",
    "Pale Fire Light",
    "Pale Fire Paper",
}
EXPECTED_ROLE_COLORS = {'Pale Fire': {'named_type': '#C6ACD5',
               'symbol': '#DE9392',
               'comment': '#A6A6A6',
               'doc': '#C7C7C7',
               'unsafe': '#E89F96',
               'string': '#AAAC8C'},
 'Pale Fire Darker': {'named_type': '#C4A9D4',
                      'symbol': '#DD8F8A',
                      'comment': '#A5A5A5',
                      'doc': '#C4C4C4',
                      'unsafe': '#E89C92',
                      'string': '#A7AA89'},
 'Pale Fire High Contrast': {'named_type': '#C9AFDA',
                             'symbol': '#E39590',
                             'comment': '#ABABAB',
                             'doc': '#CACACA',
                             'unsafe': '#EEA298',
                             'string': '#ACB08F'},
 'Pale Fire Stealth': {'named_type': '#C8AAD2',
                       'symbol': '#D39696',
                       'comment': '#A0A0A0',
                       'doc': '#C6C6C6',
                       'unsafe': '#DEA39C',
                       'string': '#ADA88E'},
 'Pale Fire Light': {'named_type': '#7D5487',
                     'symbol': '#A8413E',
                     'comment': '#636363',
                     'doc': '#515151',
                     'unsafe': '#A14740',
                     'string': '#5E6905'},
 'Pale Fire Paper': {'named_type': '#7D5487',
                     'symbol': '#A8413E',
                     'comment': '#636363',
                     'doc': '#515151',
                     'unsafe': '#A14740',
                     'string': '#5E6905'}}
NAMED_TYPE_CAPTURES = {
    "class", "enum", "struct", "type", "type.alias", "type.class",
    "type.class.definition", "type.definition", "type.enum", "type.enum.definition",
    "type.event", "type.struct", "type.struct.definition", "type.super", "type.union",
}
PERCEPTUAL_DISTANCE_RULES = {
    ("string", "variable"): 0.075,
    ("string", "number"): 0.075,
    ("string", "function"): 0.075,
    ("string", "type.builtin"): 0.075,
    ("string", "keyword"): 0.075,

    ("type", "function"): 0.12,
    ("namespace", "number"): 0.10,
    ("type.builtin", "function"): 0.075,
    ("type", "type.parameter"): 0.075,
    ("type.parameter", "string"): 0.075,
    ("symbol", "string"): 0.075,
    ("comment", "comment.doc"): 0.06,
    ("namespace", "type"): 0.075,
    ("namespace", "macro"): 0.075,
    ("keyword", "variable"): 0.075,
    ("property", "string"): 0.075,
    ("type.builtin", "comment"): 0.075,
    ("type.builtin", "comment.doc"): 0.075,
    ("symbol", "property"): 0.075,
    ("keyword", "symbol"): 0.10,
    ("keyword", "property"): 0.075,
    ("symbol", "type"): 0.075,
    ("symbol", "type.parameter"): 0.075,
}
CONTROL_FLOW_CAPTURES = {
    "keyword.control", "keyword.control.conditional", "keyword.control.repeat",
    "keyword.control.return", "keyword.conditional", "keyword.repeat",
    "keyword.return", "keyword.exception",
}
ITALIC_CAPTURES = CONTROL_FLOW_CAPTURES | {
    "concept", "interface", "type.interface", "type.interface.definition",
    "type.trait", "lifetime", "emphasis", "predictive",
}
COLOR = re.compile(r"^#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")

# Zed's documented captures, its default semantic-token style candidates,
# representative dotted captures from major grammars, and all captures used by
# the official Ruby extension that need more than a generic base fallback.
CAPTURES = {
    "concept", "function.special", "keyword.preproc", "type.primitive",
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
CAPTURES |= CONTROL_FLOW_CAPTURES


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


def validate_editor_states(style):
    # The published v0.2.0 schema omits this supported Zed field.
    active = style.get("search.active_match_background")
    assert isinstance(active, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", active), "active search fill must be an opaque RGB color"
    search = style["search.match_background"]
    assert active != search, "active and inactive search fills must differ"
    assert active != style["editor.background"], "active search must be visible"
    assert search != style["editor.background"], "search must be visible"
    for player in style["players"]:
        assert player["selection"] != style["editor.background"], "selection must be visible"
    syntax = style["syntax"]
    for capture in ("punctuation", "punctuation.bracket", "punctuation.delimiter"):
        assert syntax[capture]["color"] != syntax["variable"]["color"], "punctuation must have its own color"
        assert syntax[capture] == syntax["punctuation"], "ordinary punctuation must share a neutral style"
    for foreground, background, ratio in diagnostic_indicator_cases(style):
        assert ratio >= 3.0, f"{foreground} on {background}: {ratio:.6f}:1 < 3:1 indicator minimum"


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
    version = manifest["version"]
    assert isinstance(version, str) and re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version), "extension version must use major.minor.patch"
    assert version == load_json(ROOT / "package.json")["version"], "extension.toml and package.json versions must match"
    assert manifest["schema_version"] == 1, "unexpected manifest schema"
    assert "zed" not in manifest["name"].lower(), "marketplace name cannot contain Zed"

    names = {entry["name"] for entry in theme["themes"]}
    assert names == EXPECTED_THEMES, f"unexpected theme variants: {sorted(names)}"

    style_keys = None
    for entry in theme["themes"]:
        expected_appearance = "light" if entry["name"] in {"Pale Fire Light", "Pale Fire Paper"} else "dark"
        assert entry["appearance"] == expected_appearance, f"{entry['name']} has incorrect appearance"
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
        assert styles["string"]["color"] == expected["string"], f"{entry['name']} has an unexpected string color"
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

        italic_captures = {
            capture for capture, style in styles.items()
            if style.get("font_style") == "italic"
        }
        assert italic_captures == ITALIC_CAPTURES, (
            f"{entry['name']} has unexpected italic styling: "
            f"{sorted(italic_captures ^ ITALIC_CAPTURES)}"
        )
        for capture in CONTROL_FLOW_CAPTURES:
            assert styles[capture]["color"] == styles["keyword"]["color"], (
                f"{entry['name']} {capture} must retain the keyword color"
            )
        for first, second in (
            ("namespace", "module"), ("number", "constant.numeric"),
            ("type.builtin", "type.primitive"), ("concept", "type.interface"),
            ("function.special", "function.macro"), ("keyword.preproc", "preproc"),
            ("type.parameter", "type.parameter.definition"),
        ):
            assert styles[first] == styles[second], (
                f"{entry['name']} {first} and {second} must share a role"
            )

        validate_editor_states(entry["style"])
        cases = list(contrast_cases(entry["style"]))
        failures = [case for case in cases if case[3] < MIN_TEXT_CONTRAST]
        if failures:
            for section, foreground, background, ratio in sorted(failures, key=lambda case: case[3])[:20]:
                print(f"{entry['name']} [{section}] {foreground} on {background}: {ratio:.6f}:1 < {MIN_TEXT_CONTRAST:g}:1", file=sys.stderr)
            raise AssertionError(f"{entry['name']} has {len(failures)} failing text/background pairs")
        section, foreground, background, ratio = min(cases, key=lambda case: case[3])
        print(f"{entry['name']}: {len(cases)} text/background pairs; minimum {ratio:.6f}:1 "
              f"({foreground} on {background})")

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
