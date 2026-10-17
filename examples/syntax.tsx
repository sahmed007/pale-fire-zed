import { useState, type ReactNode } from "react";

type Status = "ready" | "waiting";
interface CardProps {
  title: string;
  children?: ReactNode;
}

// JSX tags, attributes, embedded expressions, and event handlers.
export function CounterCard({ title, children }: CardProps) {
  const [count, setCount] = useState<number>(0);
  const status: Status = count > 0 ? "ready" : "waiting";

  function increment() {
    if (count >= 42) return;
    setCount(previous => previous + 2);
  }

  return (
    <section className="card" data-status={status}>
      <h2>{title}</h2>
      <button type="button" onClick={increment}>
        Count: {count}
      </button>
      {children ?? <p>No additional details.</p>}
    </section>
  );
}
