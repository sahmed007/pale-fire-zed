# Pale Fire for Zed

A port of [Pale Fire](https://github.com/matklad/pale-fire), itself based on Zenburn, for the [Zed editor](https://zed.dev/).

Pale Fire keeps the original theme's restrained palette while providing broad syntax coverage across C++, Ruby, Go, Python, Rust, JavaScript, TypeScript, HTML, CSS, data formats, markup, shells, SQL, and other Zed languages. Ruby, Rails, and ERB receive additional testing so classes, constants, methods, variables, symbols, interpolation, and embedded templates remain easy to distinguish.

## Variants

- Pale Fire
- Pale Fire Darker
- Pale Fire High Contrast (brighter palette; the same 4.5:1 minimum)
- Pale Fire Stealth
- Pale Fire Light — warm ivory editor, coordinated light UI and terminal
- Pale Fire Paper — neutral off-white editor, stone-gray surfaces, and a matching light terminal

Pale Fire Light and Paper are original light adaptations of this palette. Both use dark ochre, olive, brick red, copper, teal, and plum. Light has warm ivory surfaces; Paper pairs neutral off-white surfaces with charcoal text.

## Highlights

- Workspace panels, title/status bars, tab strips/inactive tabs, and terminals share one background per variant. The code area, active tabs, line-number gutter, breadcrumbs, and editor subheaders share the editor background. Stealth uses the same color for all these surfaces and floating menus/dialogs; selection and interaction highlights remain visible.
- User-defined types use gray lavender, distinct from blue-green functions and methods.
- Built-in and primitive types use teal, distinct from blue-green functions.
- Namespaces and modules use blue-gray, distinct from violet named types, pale blue macros, and sage-green numbers.
- Properties use muted copper-orange, distinct from olive strings.
- Comments use neutral gray, with more prominent documentation comments (lighter in dark variants, darker in Light and Paper).
- Type parameters use pale desaturated violet, distinct from violet named types.
- Interfaces, traits, and C++ concepts use italic teal.
- Across languages, control-flow and exception keywords use italic straw gold wherever the grammar exposes those categories; generic keywords remain upright.
- Symbols and atoms use earthy red, distinct from straw-gold keywords, olive strings, and lavender types.
- The theme includes comprehensive Tree-sitter and semantic-token mappings for consistent cross-language highlighting.
- Ordinary punctuation recedes while operators and interpolation remain distinct.
- Cool selections, warm search matches, and a stronger active-match fill make editor states easier to locate.
- Diagnostic foregrounds have a separate 3:1 visibility check. Borders use intentionally subdued colors and are excluded from that check.
- Syntax highlighting does not use bold font weights.
- UI accents and terminal colors share the earthy red, sage, ochre, and dusty blue palette. Regular dark variants keep text close to High Contrast brightness, with their own backgrounds and saturation.
- Dark variants meet a 4.5:1 minimum and Light/Paper meet a stronger 5.5:1 minimum for the tested theme-controlled text/background pairs. See [coverage and limitations](docs/contrast.md); this is not a claim of full WCAG conformance for Zed.

The same italic policy applies to every language. Its appearance depends on the categories supplied by the grammar or language server: tokens reported only as generic `keyword` remain upright. Semantic highlighting follows [Zed's style mappings](https://zed.dev/docs/semantic-tokens) and can affect which style is applied; the theme does not change your semantic-token settings.

## Installation

Open Zed's Extensions page, search for **Pale Fire**, and select **Install**. Then open the theme selector and choose one of the six Pale Fire variants.

To test the repository as a development extension, run `zed: install dev extension` from the command palette and select the repository directory.

## Development

See [the changelog](CHANGELOG.md) for versioned release notes.

```sh
npm run build
npm run check
```

After rebuilding, click **Rebuild** on the installed Pale Fire development extension in Zed's Extensions page to refresh cached theme colors.

The generated theme is located at `themes/pale-fire.json`. Edit `scripts/build-theme.mjs`, then regenerate it. Validation checks schema coverage, selective italics, a minimum text contrast ratio of 4.5:1 for dark variants and 5.5:1 for Light/Paper across editor, UI, gutter, and default terminal states, and perceptual separation of key roles in every variant. The check reports each variant's worst contrast pair. Syntax, UI/player, and terminal palettes are independently configured. See the [contrast guide](docs/contrast.md) for the tested state matrix and exclusions.

For an editor review, open the files listed in [the examples guide](examples/README.md) and cycle through all six variants. Compare namespaces with numbers, built-in types with functions, and type parameters with named types; check control flow, strings, and language-specific constructs. For example, the C++ sample includes `std::vector<int>`, numeric literals, concepts, and macros. Repeat with semantic tokens off and combined, using `dev: open highlights tree view` to inspect the categories actually emitted. Type parameters may be reported as ordinary types without semantic tokens.

C++ capture coverage includes namespaces, modules, primitives (including the older `type.primitive` capture), concepts, macro definitions, and preprocessor directives. Zed's current default semantic rules do not map clangd's `concept` tokens, so concept styling relies on Tree-sitter captures in off/combined mode; not every concept reference receives that capture.

## License and credits

Pale Fire for Zed is licensed under [GNU GPLv3](LICENSE). See [ATTRIBUTION.md](ATTRIBUTION.md) for Pale Fire and Zenburn credits.
