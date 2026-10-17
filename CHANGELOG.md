# Changelog

User-visible changes are recorded here for each release. Versions match
`extension.toml`; Git tags use the `v` prefix.

## Unreleased

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
