interface RoutineCardProps {
  title: string;
  timeSlot: string;
  recommendation?: string;
}

export function RoutineCard({ title, timeSlot, recommendation }: RoutineCardProps) {
  return (
    <article style={{ border: "1px solid #d1d5db", borderRadius: "0.5rem", padding: "1rem", marginBottom: "0.75rem" }}>
      <h3>{title}</h3>
      <p>{timeSlot}</p>
      {recommendation ? <small>AI tip: {recommendation}</small> : null}
    </article>
  );
}
