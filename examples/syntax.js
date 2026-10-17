// Private fields, async control flow, regex, and interpolation.
const LIMIT = 42;
const labelPattern = /^[a-z]+(?:-[a-z]+)*$/i;

class Counter {
  #value = 0;

  increment(step = 2) {
    this.#value += step;
    return this.#value;
  }
}

async function collect(items) {
  const counter = new Counter();
  try {
    for await (const { label, enabled = true } of items) {
      if (!enabled || !labelPattern.test(label)) continue;
      const value = counter.increment();
      console.log(`${label}: ${value}\n`);
      if (value >= LIMIT) break;
    }
  } catch (error) {
    console.error(error?.message ?? "unknown error");
  } finally {
    console.log("finished");
  }
}

void collect([{ label: "ready", enabled: true }]);
