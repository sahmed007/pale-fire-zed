from collections import Counter
from typing import TypeVar

T = TypeVar("T")
LIMIT = 42


def first(items: list[T]) -> T | None:
    """Return the first item, if present."""
    for item in items:
        if item is not None:
            return item
    return None


try:
    counts = Counter([1, 2, 2])
    print(f"ready: {first(list(counts))}\n")
except ValueError as error:
    print(str(error))
