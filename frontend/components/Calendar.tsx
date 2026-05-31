interface CalendarEvent {
  title: string;
  start: string;
  end: string;
}

interface CalendarProps {
  events: CalendarEvent[];
}

export function Calendar({ events }: CalendarProps) {
  return (
    <section>
      <h2>Today&apos;s Time Blocks</h2>
      <ul>
        {events.map((event) => (
          <li key={`${event.title}-${event.start}`}>
            <strong>{event.title}</strong>: {event.start} - {event.end}
          </li>
        ))}
      </ul>
    </section>
  );
}
