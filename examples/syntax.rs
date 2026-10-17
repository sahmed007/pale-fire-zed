use std::collections::HashMap;

// Compare types, generic parameters, lifetimes, methods, and numbers.
trait Measure {
    fn size(&self) -> usize;
}

struct Bucket<T> {
    items: Vec<T>,
}

impl<T> Measure for Bucket<T> {
    fn size(&self) -> usize {
        self.items.len()
    }
}

fn first<'a, T>(items: &'a [T]) -> Option<&'a T> {
    if items.is_empty() {
        return None;
    }
    items.first()
}

fn main() {
    let mut counts = HashMap::new();
    for value in [1, 2, 42] {
        counts.insert(value, "ready");
    }
    println!("{} entries", counts.len());
}
