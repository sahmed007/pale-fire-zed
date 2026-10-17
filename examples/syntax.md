# Pale Fire preview

Compare **strong text**, *emphasis*, ~~deleted text~~, and `inline_code(42)`.

## Links and lists

[Zed editor](https://zed.dev/) supports language-aware highlighting.

- Namespaces should differ from numbers.
- Strings should differ from symbols.
  - Nested items should remain readable.

1. Select a theme variant.
2. Compare the code below.

> A blockquote with *emphasis* and `inline code`.

| Role | Example |
| --- | --- |
| Number | `42` |
| Namespace | `std` |

```cpp
std::vector<int> values{1, 2, 42};
for (int value : values) {
    if (value == 2) continue;
}
```

```python
def first(items):
    return next(iter(items), None)
```

---

- [x] Review literals
- [ ] Review embedded code
