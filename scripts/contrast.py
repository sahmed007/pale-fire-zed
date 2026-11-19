"""Explicit theme text/background pairs for WCAG 2.2 SC 1.4.3.

Colors are composited in encoded sRGB, then linearized for luminance. No
intermediate channel rounding or contrast rounding is used for pass/fail.
See docs/contrast.md for coverage, rendering assumptions, and exclusions.
"""
from functools import lru_cache
from itertools import product

MIN_TEXT_CONTRAST = 4.5
MIN_LIGHT_TEXT_CONTRAST = 5.5


def minimum_text_contrast(appearance):
    return MIN_LIGHT_TEXT_CONTRAST if appearance == "light" else MIN_TEXT_CONTRAST


def failing_text_cases(cases, appearance):
    minimum = minimum_text_contrast(appearance)
    return [case for case in cases if case[3] < minimum]


UI_SURFACES = (
    "background", "surface.background", "elevated_surface.background",
    "panel.background", "status_bar.background", "title_bar.background",
    "title_bar.inactive_background", "toolbar.background", "tab_bar.background",
    "tab.active_background", "tab.inactive_background", "editor.subheader.background",
)
UI_STATES = (
    "element.background", "element.hover", "element.active", "element.selected",
    "ghost_element.background", "ghost_element.hover", "ghost_element.active",
    "ghost_element.selected", "drop_target.background",
)
UI_TEXT = (
    "text", "text.accent", "text.muted", "text.placeholder", "link_text.hover",
    "icon", "icon.accent", "icon.muted", "icon.placeholder",
)
STATUS_TEXT = (
    "conflict", "created", "deleted", "error", "hidden", "hint", "ignored",
    "info", "modified", "predictive", "renamed", "success", "unreachable", "warning",
)
EDITOR_BASES = (
    "editor.background", "editor.active_line.background", "editor.highlighted_line.background",
)
DOCUMENT_STATES = (
    "editor.document_highlight.bracket_background",
    "editor.document_highlight.read_background",
    "editor.document_highlight.write_background",
)
# Disabled controls are inoperative, not just unfocused/muted. Guides and borders
# are non-text; they are not evidence of full WCAG conformance.
EXEMPT_TEXT = {"text.disabled", "icon.disabled"}


@lru_cache(maxsize=None)
def rgb(color):
    if isinstance(color, tuple):
        return color[:3]
    return tuple(int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))


@lru_cache(maxsize=None)
def composite(foreground, background):
    front, back = rgb(foreground), rgb(background)
    alpha = int(foreground[7:9], 16) / 255 if isinstance(foreground, str) and len(foreground) == 9 else 1.0
    return tuple(f * alpha + b * (1 - alpha) for f, b in zip(front, back))


@lru_cache(maxsize=None)
def relative_luminance(color):
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb(color)]
    return sum(c * weight for c, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


@lru_cache(maxsize=None)
def contrast_ratio(first, second):
    lighter, darker = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def text_ratio(foreground, background):
    return contrast_ratio(composite(foreground, background), background)


def editor_backgrounds(style):
    """Single states and overlapping diff/diagnostic, document, search, selection.

    All permutations collapse to this set for the shipped opaque overlays.
    The layered paths also exercise alpha if a future edit adds transparency.
    """
    selections = [(f"players[{i}].selection", p["selection"]) for i, p in enumerate(style["players"])]
    contexts = [(f"{key}.background", style[f"{key}.background"]) for key in STATUS_TEXT]
    contexts += [(key, style[key]) for key in DOCUMENT_STATES + ("drop_target.background",)]
    for base_key in EDITOR_BASES:
        base = composite(style[base_key], style["editor.background"])
        yield base_key, base
        for context, document, search, selection in product(
            [(None, None)] + contexts,
            [(None, None)] + [(key, style[key]) for key in DOCUMENT_STATES],
            [(None, None)] + [(key, style[key]) for key in ("search.match_background", "search.active_match_background")],
            [(None, None)] + selections,
        ):
            label, background = base_key, base
            for key, color in (context, document, search, selection):
                if color is not None:
                    background = composite(color, background)
                    label += f" + {key}"
            yield label, background


def unique_backgrounds(pairs):
    seen = set()
    for label, color in pairs:
        if color not in seen:
            seen.add(color)
            yield label, color


def contrast_cases(style):
    """Yield (section, foreground description, background description, ratio)."""
    backgrounds = list(unique_backgrounds(editor_backgrounds(style)))
    foregrounds = [(f"syntax.{key}", value["color"]) for key, value in style["syntax"].items()]
    foregrounds += [(key, style[key]) for key in ("editor.foreground", "editor.invisible") + STATUS_TEXT]
    for fg_name, fg in foregrounds:
        for bg_name, bg in backgrounds:
            yield "editor", fg_name, bg_name, text_ratio(fg, bg)

    gutter_backgrounds = [("editor.gutter.background", rgb(style["editor.gutter.background"]))]
    gutter_backgrounds += [(key, rgb(style[key])) for key in EDITOR_BASES]
    for fg in ("editor.line_number", "editor.active_line_number"):
        for bg_name, bg in gutter_backgrounds:
            yield "gutter", fg, bg_name, text_ratio(style[fg], bg)

    surfaces = []
    for key in UI_SURFACES:
        bg = composite(style[key], style["background"])
        surfaces.append((key, bg))
        for state in UI_STATES:
            surfaces.append((f"{key} + {state}", composite(style[state], bg)))
    surfaces = list(unique_backgrounds(surfaces))
    for fg in UI_TEXT + STATUS_TEXT:
        for bg_name, bg in surfaces:
            yield "ui", fg, bg_name, text_ratio(style[fg], bg)
            if fg in STATUS_TEXT:
                status_bg = composite(style[f"{fg}.background"], bg)
                yield "ui", fg, f"{bg_name} + {fg}.background", text_ratio(style[fg], status_bg)
    for i, player in enumerate(style["players"]):
        for bg_name, bg in surfaces:
            yield "ui", f"players[{i}].cursor/label", bg_name, text_ratio(player["cursor"], bg)
            yield "ui", "text", f"{bg_name} + players[{i}].background", text_ratio(style["text"], composite(player["background"], bg))

    terminal_bgs = ["terminal.background", "terminal.ansi.background"]
    terminal_fg = [key for key in style if key.startswith("terminal.") and key not in terminal_bgs]
    for fg in terminal_fg:
        for bg in terminal_bgs:
            yield "terminal", fg, bg, text_ratio(style[fg], rgb(style[bg]))
        # Zed uses player selection backgrounds for terminal selections too.
        for i, player in enumerate(style["players"]):
            bg = composite(player["selection"], style["terminal.background"])
            yield "terminal", fg, f"terminal.background + players[{i}].selection", text_ratio(style[fg], bg)


def diagnostic_indicator_cases(style):
    """Limited 3:1 check for diagnostic foregrounds against adjacent surfaces."""
    backgrounds = list(editor_backgrounds(style))
    for key in UI_SURFACES:
        base = composite(style[key], style['background'])
        backgrounds.append((key, base))
        backgrounds.extend((f'{key} + {state}', composite(style[state], base)) for state in UI_STATES)
    backgrounds = list(unique_backgrounds(backgrounds))
    for role in ('error', 'warning', 'info', 'hint'):
        adjacent = backgrounds + [(f'{role}.background', composite(style[f'{role}.background'], style['background']))]
        for label, background in adjacent:
            yield role, label, text_ratio(style[role], background)
