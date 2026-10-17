# Syntax preview examples

Open these files in Zed and switch between the six Pale Fire variants. They are small highlighting samples, not a shared application; running them is optional. Some languages require a Zed language extension. The TSX sample assumes React is available if you want to type-check it.

| File | What to compare |
| --- | --- |
| [C++](syntax.cpp) | Namespaces, numbers, primitive types, concepts, templates, macros, control flow |
| [Rust](syntax.rs) | Traits, lifetimes, generics, macros, control flow |
| [Python](syntax.py) | Type hints, constants, docstrings, interpolation, exceptions |
| [Ruby](syntax.rb) | Symbols, strings, constants, instance variables, exceptions |
| [Elixir](syntax.exs) | Modules, atoms, structs, guards, pattern matching, pipelines, sigils |
| [TypeScript](syntax.ts) | Interfaces, generics, properties, methods, control flow |
| [Go](syntax.go) | Packages, generics, interfaces, receivers, error handling |
| [JavaScript](syntax.js) | Private fields, async loops, regex, template strings |
| [React / TSX](syntax.tsx) | JSX tags, attributes, embedded expressions, hooks, types |
| [Java](Syntax.java) | Records, annotations, generic types, exceptions |
| [C#](syntax.cs) | Records, nullable types, pattern matching, interpolation |
| [Swift](syntax.swift) | Protocols, optionals, enums, generic types, interpolation |
| [HTML](syntax.html) | Tags, attributes, entities, embedded JavaScript |
| [CSS](syntax.css) | Selectors, custom properties, units, functions, media queries |
| [SQL](syntax.sql) | PostgreSQL CTEs, functions, quoted identifiers, CASE expressions |
| [ANSI contrast](contrast.sh) | Normal, bright, and dim terminal foregrounds; run with `bash examples/contrast.sh` |
| [Bash](syntax.sh) | Variables, arrays, arithmetic, patterns, heredocs |
| [JSON](syntax.json) | Keys, strings, escapes, numbers, booleans, null |
| [YAML](syntax.yaml) | Anchors, aliases, scalars, block strings |
| [TOML](syntax.toml) | Tables, dates, numeric formats, arrays |
| [Markdown](syntax.md) | Headings, emphasis, links, tables, fenced code |
| [ERB](syntax.html.erb) | Embedded Ruby, HTML, symbols, interpolation |

Check that namespaces and numbers, built-in types and functions, and named types and type parameters remain distinguishable where the language exposes those roles. Compare regular keywords with control-flow italics. Generic `keyword` captures remain upright, so the same word can appear differently across languages.

For a closer inspection, use `dev: open highlights tree view`. Compare semantic tokens off and combined when a language server is available; some distinctions require semantic tokens. Embedded languages and Markdown code fences also depend on the installed language support.
