# Changelog

User-visible changes are recorded here for each release. Versions match
`extension.toml`; Git tags use the `v` prefix.

## Unreleased

## 0.2.1

### Changed

- Unified workspace panels, title/status bars, tab strips/inactive tabs, and terminal backgrounds in every variant. Stealth also uses one background for the editor, gutter, breadcrumbs, controls, and floating menus/dialogs, while retaining state highlights.
- Matched active tabs, line-number gutters, breadcrumbs, and editor subheaders to the code background in every variant, keeping the surrounding workspace distinct in non-Stealth variants.
- Rebalanced Light and Paper syntax hues for clearer role distinction with a 5.5:1 text-contrast minimum across tested states. Strengthened UI labels, diagnostic foregrounds, and terminal colors.
- Softened all opaque borders across all six variants, including focus, selection, diagnostic, and status outlines, using 25% original color in dark variants and 35% in Light/Paper, blended with each variant’s background. Transparent borders remain unchanged.
- Limited the separate 3:1 diagnostic visibility check to foregrounds; subdued diagnostic borders are now excluded.

## 0.2.0

### Added

- Pale Fire Light, with warm ivory surfaces and a coordinated light terminal.
- Pale Fire Paper, with neutral off-white surfaces and charcoal text.
- Cross-language syntax preview examples, including Elixir, and an ANSI terminal preview.
- Automated text-contrast, diagnostic visibility, and palette-separation checks, with documented coverage and limitations.

### Changed

- Refined all six palettes with earthy reds, olive strings, neutral gray comments, and more distinct syntax roles while preserving the Pale Fire and Zenburn character.
- Brightened text in the regular dark variants.
- Applied selective control-flow and exception italics across languages wherever grammar or semantic captures expose those categories.
- Made ordinary punctuation quieter while keeping operators and interpolation distinct.
- Improved selection and search visibility, including a stronger active search match on supported Zed versions.
- Gave diagnostics independent foregrounds, borders, and background fills.

### Fixed

- Improved separation of namespaces from numbers, strings from variables and properties, and built-in types from functions.
- Expanded syntax capture coverage, including C++ namespaces, primitives, concepts, macros, and preprocessor directives.
- Enforced a 4.5:1 minimum for tested theme-controlled text/background pairs and a separate 3:1 diagnostic-indicator minimum. See [coverage and limitations](docs/contrast.md); these checks do not establish full WCAG conformance for Zed.

## 0.1.0

### Added

- Initial release with Pale Fire, Pale Fire Darker, Pale Fire High Contrast, and Pale Fire Stealth.
- Shared Tree-sitter and semantic syntax mappings, theme generation, and schema validation.
