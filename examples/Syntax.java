import java.util.List;

// Records, annotations, generic parameters, and exception handling.
public class Syntax {
    record Bucket<T>(List<T> values) {
        T first() {
            if (values.isEmpty()) {
                throw new IllegalStateException("empty bucket");
            }
            return values.get(0);
        }
    }

    @Deprecated
    static int doubled(int value) {
        return value * 2;
    }

    public static void main(String[] args) {
        var bucket = new Bucket<Integer>(List.of(1, 2, 42));
        try {
            for (int value : bucket.values()) {
                if (value == 2) continue;
                System.out.printf("value: %d%n", doubled(value));
            }
        } catch (IllegalStateException error) {
            System.err.println(error.getMessage());
        }
    }
}
