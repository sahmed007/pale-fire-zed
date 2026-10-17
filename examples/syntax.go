package main

import "fmt"

// Generic types, interfaces, receivers, and error handling.
type Bucket[T any] struct {
    Values []T
}

type Measurable interface {
    Size() int
}

func (b Bucket[T]) Size() int { return len(b.Values) }

func first[T any](values []T) (T, error) {
    for _, value := range values {
        return value, nil
    }
    var zero T
    return zero, fmt.Errorf("empty bucket")
}

func main() {
    bucket := Bucket[int]{Values: []int{1, 2, 42}}
    if value, err := first(bucket.Values); err != nil {
        fmt.Println(err)
    } else {
        fmt.Printf("first: %d\n", value)
    }
}
