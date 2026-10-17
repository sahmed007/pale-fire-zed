#include <concepts>
#include <stdexcept>
#include <vector>

#define SCALE(value) ((value) * 2)

// Namespaces, primitives, named types, and literals should read differently.
namespace sample {
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <Numeric T> struct Counter {
  T value;

  T next(T step) {
    if (step < 0) {
      throw std::invalid_argument("negative step");
    }
    return value += step;
  }
};
} // namespace sample

int main() {
  std::vector<int> values{1, 2, 42};
  sample::Counter<int> counter{0};
  constexpr double ratio = 3.14;
  const char *message = "ready\n";
  try {
    for (int value : values) {
      if (value == 2)
        continue;
      counter.next(SCALE(value));
    }
  } catch (const std::exception &error) {
    return 1;
  }
  return counter.value > 0 ? 0 : 1;
}
