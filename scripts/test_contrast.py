"""Exercise contrast math and catch regressions beyond the editor background."""
import copy
import json
import unittest
from pathlib import Path

from contrast import composite, contrast_ratio, contrast_cases, MIN_TEXT_CONTRAST, text_ratio
from validate import validate_editor_states


class ContrastTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        themes = json.loads((Path(__file__).resolve().parent.parent / "themes/pale-fire.json").read_text())["themes"]
        cls.themes = themes
        cls.style = themes[0]["style"]
        cls.light_themes = {theme["name"]: theme["style"] for theme in themes if theme["appearance"] == "light"}

    def test_reference_ratios(self):
        self.assertEqual(contrast_ratio("#000000", "#FFFFFF"), 21)
        self.assertEqual(contrast_ratio("#FFFFFF", "#FFFFFF"), 1)
        self.assertAlmostEqual(contrast_ratio("#777777", "#FFFFFF"), 4.478089453577214)

    def test_alpha_composites_before_luminance(self):
        result = composite("#FFFFFF80", "#000000")
        self.assertEqual(result, (128 / 255,) * 3)
        self.assertEqual(text_ratio("#FFFFFF80", "#000000"), contrast_ratio(result, "#000000"))
        self.assertLess(text_ratio("#FFFFFF80", "#000000"), 7)

    def test_transparency_and_layer_order(self):
        self.assertEqual(composite("#FFFFFF00", "#123456"), composite("#123456", "#000000"))
        self.assertEqual(composite("#FFFFFF", "#000000"), (1, 1, 1))
        blue_on_red = composite("#0000FF80", composite("#FF000080", "#000000"))
        self.assertAlmostEqual(blue_on_red[0], (128 / 255) * (127 / 255))
        self.assertEqual(blue_on_red[2], 128 / 255)
        self.assertNotEqual(blue_on_red, composite("#FF000080", composite("#0000FF80", "#000000")))

    def test_threshold_is_not_rounded(self):
        # Construct a neutral foreground whose exact contrast is 4.4999:1.
        linear = 4.4999 * .05 - .05
        srgb = 1.055 * linear ** (1 / 2.4) - .055
        ratio = contrast_ratio((srgb,) * 3, "#000000")
        self.assertEqual(round(ratio, 2), 4.5)
        self.assertLess(ratio, MIN_TEXT_CONTRAST)

    def test_aa_threshold_accepts_readable_text_below_seven(self):
        self.assertEqual(MIN_TEXT_CONTRAST, 4.5)
        ratio = contrast_ratio("#808080", "#000000")
        self.assertGreaterEqual(ratio, MIN_TEXT_CONTRAST)
        self.assertLess(ratio, 7)

    def test_readable_text_coverage(self):
        cases = list(contrast_cases(self.style))
        names = {case[1] for case in cases}
        for name in ("syntax.comment", "text.muted", "text.placeholder", "ignored", "hidden",
                     "editor.line_number", "editor.invisible", "terminal.ansi.black",
                     "terminal.ansi.dim_red", "terminal.dim_foreground"):
            self.assertIn(name, names)
        self.assertNotIn("text.disabled", names)
        self.assertNotIn("icon.disabled", names)
        self.assertEqual({case[0] for case in cases}, {"editor", "gutter", "ui", "terminal"})

    def test_bright_selection_cannot_hide_behind_base_contrast(self):
        style = copy.deepcopy(self.style)
        style["players"][0]["selection"] = "#FFFFFFCC"
        failures = [c for c in contrast_cases(style) if c[3] < MIN_TEXT_CONTRAST and "players[0].selection" in c[2]]
        self.assertTrue(any(c[0] == "editor" for c in failures))
        self.assertTrue(any(c[0] == "terminal" for c in failures))

    def test_overlapping_translucent_highlights(self):
        style = copy.deepcopy(self.style)
        style["created.background"] = "#FFFFFF30"
        style["search.match_background"] = "#FFFFFF30"
        style["players"][0]["selection"] = "#FFFFFF30"
        failures = [c for c in contrast_cases(style) if c[3] < MIN_TEXT_CONTRAST]
        self.assertTrue(any(all(key in c[2] for key in ("created.background", "search.match_background", "players[0].selection")) for c in failures))

    def test_muted_ui_and_dim_terminal_regressions_fail(self):
        style = copy.deepcopy(self.style)
        style["text.placeholder"] = style["panel.background"]
        style["terminal.ansi.dim_blue"] = "#00000080"
        failures = [c for c in contrast_cases(style) if c[3] < MIN_TEXT_CONTRAST]
        self.assertTrue(any(c[1] == "text.placeholder" for c in failures))
        self.assertTrue(any(c[1] == "terminal.ansi.dim_blue" for c in failures))

    def test_dark_selection_fails_on_light_theme(self):
        for name, light in self.light_themes.items():
            with self.subTest(theme=name):
                style = copy.deepcopy(light)
                self.assertTrue(all(c[3] >= MIN_TEXT_CONTRAST for c in contrast_cases(style)))
                style["players"][0]["selection"] = "#000000CC"
                failures = [c for c in contrast_cases(style) if c[3] < MIN_TEXT_CONTRAST and "players[0].selection" in c[2]]
                self.assertTrue(any(c[0] == "editor" for c in failures))
                self.assertTrue(any(c[0] == "terminal" for c in failures))

    def test_overlapping_dark_highlights_on_light_theme(self):
        for name, light in self.light_themes.items():
            with self.subTest(theme=name):
                style = copy.deepcopy(light)
                for key in ("created.background", "search.match_background"):
                    style[key] = "#00000030"
                style["players"][0]["selection"] = "#00000030"
                failures = [c for c in contrast_cases(style) if c[3] < MIN_TEXT_CONTRAST]
                self.assertTrue(any(all(key in c[2] for key in ("created.background", "search.match_background", "players[0].selection")) for c in failures))

    def test_pale_terminal_foregrounds_fail_on_light_theme(self):
        for name, light in self.light_themes.items():
            with self.subTest(theme=name):
                style = copy.deepcopy(light)
                for key in ("terminal.ansi.white", "terminal.ansi.bright_white", "terminal.ansi.dim_white"):
                    style[key] = "#FFFFFF"
                failures = {c[1] for c in contrast_cases(style) if c[3] < MIN_TEXT_CONTRAST}
                for key in ("terminal.ansi.white", "terminal.ansi.bright_white", "terminal.ansi.dim_white"):
                    self.assertIn(key, failures)

    def test_editor_state_regressions(self):
        for theme in self.themes:
            with self.subTest(theme=theme["name"]):
                validate_editor_states(theme["style"])
                for mutation in ("search", "active", "selection", "punctuation", "diagnostic"):
                    style = copy.deepcopy(theme["style"])
                    if mutation == "search":
                        style["search.match_background"] = style["editor.background"]
                    elif mutation == "active":
                        style["search.active_match_background"] = style["search.match_background"]
                    elif mutation == "selection":
                        style["players"][0]["selection"] = style["editor.background"]
                    elif mutation == "punctuation":
                        style["syntax"]["punctuation"] = style["syntax"]["variable"]
                    else:
                        style["error.border"] = style["editor.background"]
                    with self.subTest(mutation=mutation), self.assertRaises(AssertionError):
                        validate_editor_states(style)

    def test_active_search_overlaps_are_covered(self):
        for theme in self.themes:
            with self.subTest(theme=theme["name"]):
                style = copy.deepcopy(theme["style"])
                overlay = "#00000030" if theme["appearance"] == "light" else "#FFFFFF30"
                style["error.background"] = overlay
                style["editor.document_highlight.read_background"] = overlay
                style["search.active_match_background"] = overlay
                style["players"][0]["selection"] = overlay
                failures = [c for c in contrast_cases(style) if c[3] < MIN_TEXT_CONTRAST]
                self.assertTrue(any(all(k in c[2] for k in ("error.background", "editor.document_highlight.read_background", "search.active_match_background", "players[0].selection")) for c in failures))

if __name__ == "__main__":
    unittest.main()
