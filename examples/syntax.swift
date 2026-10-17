import Foundation

// Protocols, generic constraints, optionals, and enum cases.
protocol Measurable {
    var size: Int { get }
}

struct Bucket<T>: Measurable {
    let values: [T]
    var size: Int { values.count }

    func first() -> T? {
        guard let value = values.first else { return nil }
        return value
    }
}

enum Status {
    case ready(Int)
    case waiting
}

let bucket = Bucket(values: [1, 2, 42])
let status = bucket.first().map(Status.ready) ?? .waiting
switch status {
case .ready(let value):
    print("ready: \(value)\n")
case .waiting:
    print("waiting")
}
