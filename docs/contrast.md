# Text contrast and palette review

Pale Fire targets **WCAG 2.2 SC 1.4.3 (Contrast Minimum)** for theme-controlled readable text: at least **4.5:1** at normal text sizes in every variant. This is a measured text-contrast claim, not full WCAG AA conformance for Zed. Keyboard interaction, focus indicators, screen-reader support, and other accessibility requirements are outside this theme's text-contrast audit.

The [W3C criterion](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) sets the 4.5:1 threshold and exempts genuinely inactive controls. Muted text, comments, placeholders, ignored files, and dim terminal output are readable content and are included here.

## Tested foreground/background matrix

The executable source of truth is `scripts/contrast.py`. `npm run check` validates the generated theme and prints each variant's worst pair. It checks the actual output colors, not the generator's intended palette.

| Area | Foregrounds | Backgrounds and states |
| --- | --- | --- |
| Editor | Every syntax capture, default text, whitespace markers, predictive text, diagnostic/status colors | Editor, active line, highlighted line, document read/write/bracket highlights, inactive/active search matches, drop target, diagnostic and diff fills, all eight player selections |
| Overlapping editor states | The same editor text | Context/diff/diagnostic fill, then document highlight, inactive or active search, and selection, including omitted layers |
| Gutter | Regular and active line numbers | Gutter and editor line backgrounds |
| UI | Normal, accent, muted, placeholder and link text; icons; readable status colors | Main surface, panel, elevated surface, status/title/tool/tab bars, tabs, editor subheader; normal, hover, active, selected, ghost and drop-target states |
| Status UI | Conflict, created, deleted, error, hidden, hint, ignored, info, modified, predictive, renamed, success, unreachable, warning | UI surfaces/states and each status's own fill |
| Collaboration | Player cursor/label colors and default label text | UI surfaces/states and player backgrounds |
| Terminal | Default, bright, dim, and all normal/bright/dim ANSI foregrounds | Default terminal backgrounds and all player selection backgrounds |

Identical resolved backgrounds are deduplicated; the report names the first equivalent state. The shipped highlight/selection fills are opaque. Overlapping opaque fills resolve to the topmost fill, so their order does not create additional colors beyond the matrix. Transparency, including transparent status backgrounds, is still composited before measurement. Tests also exercise overlapping translucent layers to catch future regressions.

sRGB channels are alpha-composited without intermediate rounding, linearized for relative luminance, and compared using `(lighter + 0.05) / (darker + 0.05)`. Pass/fail uses the unrounded result. Displayed report values are rounded only for readability.

## Current measured minima

| Variant | Unique text/background pairs | Minimum | Foreground on background |
| --- | ---: | ---: | --- |
| Pale Fire | 3,715 | 4.656856:1 | `terminal.ansi.dim_black` on `terminal.background + players[6].selection` |
| Pale Fire Darker | 3,715 | 4.652244:1 | `terminal.ansi.dim_black` on `terminal.background + players[4].selection` |
| Pale Fire High Contrast | 3,715 | 4.655757:1 | `terminal.ansi.dim_black` on `terminal.background + players[1].selection` |
| Pale Fire Stealth | 3,715 | 4.651030:1 | `terminal.ansi.dim_black` on `terminal.background + players[3].selection` |
| Pale Fire Light | 3,639 | 4.650108:1 | `syntax.constant.numeric` on `editor.background + players[0].selection` |
| Pale Fire Paper | 3,639 | 4.650108:1 | `syntax.constant.numeric` on `editor.background + players[0].selection` |

Refresh this table from `npm run check` whenever the palette or coverage changes. These results cover defined color pairs; they do not measure a font's rasterized edge pixels.

## Palette choices

Namespaces use dusty steel blue, named types gray lavender, macros clearer blue, built-in types teal, and functions subdued blue-green. Keywords use straw gold; properties use copper-orange, strings olive, and symbolic values earthy red. Type parameters use pale desaturated violet. Elixir atoms and Ruby symbols already emit `string.special.symbol`, so they share that role without a language-specific palette.

Regression checks require at least 0.10 OKLab distance between keywords and symbols, and 0.075 between keywords and properties and between symbols and strings, named types, or type parameters. Strings also require at least 0.075 distance from variables, numbers, functions, built-in types, and keywords. These checks complement visual review of adjacent tokens.

Comments are neutral gray; documentation comments are lighter gray in dark variants and darker gray in Light and Paper. Strings inherit the former ordinary-comment olive palette, keeping literals distinct from neutral identifiers. This keeps them readable at 4.5:1 without adding italics to whole comments. The existing selective control-flow, interface/trait/concept, and lifetime italics remain unchanged.

The four dark variants retain their existing backgrounds. The three regular dark variants move readable foregrounds 80% toward High Contrast’s OKLab lightness while preserving hue and chroma where the sRGB gamut allows. Darker gets its character from its darker background, Stealth retains softer saturation, and High Contrast retains its brighter palette; all four share the 4.5:1 floor. Decorative colors and selection/highlight fills are configured separately so brighter text does not brighten its backdrop. UI diagnostics, player accents, and normal/bright/dim ANSI colors use coordinated earthy red, ochre, sage, and dusty blue families. UI, terminal, and syntax colors are stored independently. Dark variants use low-luminance opaque highlight fills; Light and Paper use pale opaque fills. Overlapping states do not accumulate into a contrasting backdrop that washes out the code.

Pale Fire Light uses a warm ivory editor (`#F5F1E8`), deeper ivory panels (`#EBE6DC`), and lighter elevated surfaces (`#FCF9F2`). Its syntax hues follow the dark family with independently tuned lightness and chroma; all separation thresholds and the 4.5:1 floor remain in force.

Pale Fire Paper uses neutral off-white (`#F4F4F0`), stone-gray panels (`#E8E8E3`), and lighter elevated surfaces (`#FCFCF9`). It keeps Light’s syntax hues with neutral charcoal identifiers (`#3D3E3B`) and a matching light terminal. Both light variants run the dark-selection, overlapping-highlight, and pale-terminal-foreground regression tests.

In dark variants, ANSI black is a readable gray foreground. In both light variants, ANSI white is a readable dark gray, and bright ANSI colors use stronger saturation rather than becoming pale. Dim ANSI colors are explicit opaque colors rather than low-opacity versions of normal colors. This deliberately changes the traditional terminal palette to honor the requested foreground contrast target.

## Editor-state visibility

Each variant explicitly defines local and collaboration selections, inactive and active search matches, document highlights, and diagnostic fills. The local selection uses blue-gray; search uses ochre, with a stronger active-match fill. Document highlights remain quieter. Opaque fills prevent cumulative washout. Selection colors apply to terminal selections too, while terminal foregrounds remain unchanged.

Ordinary punctuation, brackets, and delimiters use a dedicated neutral halfway between variable and comment OKLab lightness. Operators retain normal text strength; keyword operators retain keyword color. Escape/interpolation markers keep their blue accents. Existing italics are unchanged.

Diagnostic error/warning foregrounds use stronger earthy red/ochre; info and hints retain quieter blue/sage. Foregrounds, borders, and fills are independent of unrelated diff/status colors. `diagnostic_indicator_cases` checks diagnostic colors and borders at least 3:1 against editor states, UI surfaces/states, and their own fills. This is a limited color-pair check, not a measurement of rasterized underlines or a claim of full WCAG conformance.

`search.active_match_background` is supported by Zed 1.24.2 and the [Zed theme color definitions](https://github.com/zed-industries/zed/blob/main/crates/theme/src/styles/colors.rs), but is absent from the vendored v0.2.0 schema. Validation explicitly requires an opaque RGB value and a different color from inactive matches. Older Zed builds may ignore this key and retain their default active-match behavior.

Regression checks reject invisible selection/search fills, identical active/inactive match fills, punctuation mapped back to variables, and low-contrast diagnostic borders. Text checks include active-match overlap with document highlights, diagnostics, and selections. Numerical checks complement live visibility review.

## Exclusions and limits

- `text.disabled` and `icon.disabled` represent inoperative controls and are exempt. An unfocused tab or muted label is not disabled and remains covered.
- Borders, indent/wrap guides, scrollbar tracks, and other non-text decoration are not part of the 4.5:1 text claim. Only diagnostic foregrounds and borders receive the separate 3:1 adjacent-background check described below; this is not a general non-text contrast or full WCAG conformance claim.
- Application-selected ANSI backgrounds, inverse video, true-color terminal output, images, and external content can create pairs outside the default-background matrix. ANSI colors serve as both foregrounds and backgrounds, so no universal terminal contrast guarantee is possible.
- User overrides, semantic rules with custom colors, and opacity/dimming applied by Zed outside the theme can change the result. Test with unmodified theme colors. The theme does not alter user settings.
- A theme can style only the categories a grammar or language server exposes. Color distance between roles is a separate heuristic, not a WCAG requirement or a guarantee of distinguishability for every color-vision condition.

## Manual review

Use the [language examples](../examples/README.md) to compare qualified names, signatures, property access, and pattern matching in all six variants. Inspect comments, line numbers, placeholders, selections, search results, and diagnostics as well as ordinary code. Compare semantic tokens off and combined where available. `dev: open highlights tree view` shows which categories are actually applied.

Run `bash examples/contrast.sh` in Zed's terminal to inspect normal, bright, and dim ANSI text on the default background. Select some output to review selected terminal text.

After `npm run build`, use **Rebuild** on the installed Pale Fire development extension in Zed's Extensions page. Reloading extensions alone may leave old theme colors cached. Use the theme selector's arrow-key previews, then Escape to restore your original theme without saving a preference change.

## Review record

The editor-state update was rebuilt in Zed 1.24.2. Search results were previewed in all six variants; C++ and TypeScript punctuation and visible diagnostics were inspected, and Elixir selections/interpolation and selected ANSI output were checked in light and dark previews. These are qualitative spot checks, not an exhaustive rendering of every matrix case. Previews were cancelled to preserve the selected theme.

Pale Fire Paper was rebuilt and previewed against Light in Ruby, TypeScript, C++, and Elixir, including documentation comments, visible diagnostics, selected code, and normal/bright/dim terminal output with selection. Theme previews were cancelled to preserve the original selection.

Pale Fire Light was rebuilt and previewed in Zed on Ruby, TypeScript, C++, and Elixir, including documentation comments, visible diagnostics, selected code, and normal/bright/dim terminal output with selection. Previews were cancelled to preserve the original theme choice.

The olive-string/gray-comment update was rebuilt and spot-checked in C++, Elixir, Ruby, and TypeScript. Existing contrast minima remain unchanged. UI, terminal colors, other syntax roles, and italics were verified unchanged; hint, diff-addition, and predictive colors are now independent of comment colors.

The brighter regular variants were rebuilt as a development extension and previewed in Zed using C++, Elixir, Ruby, and TypeScript samples, plus normal/bright/dim terminal text and selected output. Previews were cancelled to preserve the original theme selection. Theme previews are qualitative spot checks, not pixel-based contrast measurements.

Every collaboration color, diagnostic/diff fill combination, UI surface/state, and normal/bright/dim terminal foreground is checked by the numeric matrix. Semantic-token settings were not changed; comparisons with both off and combined modes remain a manual review option.
