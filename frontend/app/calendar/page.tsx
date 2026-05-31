import { Calendar } from "@/components/Calendar";

const sampleEvents = [
  { title: "Deep work", start: "09:00", end: "11:00" },
  { title: "Exercise", start: "18:00", end: "18:45" },
];

export default function CalendarPage() {
  return (
    <section>
      <h1>Calendar</h1>
      <p>Visual representation of scheduled tasks and routines.</p>
      <Calendar events={sampleEvents} />
    </section>
  );
}
