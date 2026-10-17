// Interfaces, generic parameters, properties, methods, and literals.
interface Bucket<T> {
  values: T[];
  first(): T | undefined;
}

class Counter implements Bucket<number> {
  readonly values = [1, 2, 42];

  first(): number | undefined {
    for (const value of this.values) {
      if (value > 0) return value;
    }
    return undefined;
  }
}

function first<T>(items: T[]): T | undefined {
  return items[0];
}

try {
  const counter = new Counter();
  console.log(`ready: ${first(counter.values)}\n`);
} catch (error) {
  console.error(error);
}
