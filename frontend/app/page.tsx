import Link from "next/link";

export default function Home() {
  return (
    <section>
      <h1>routAIne</h1>
      <p>Plan tasks, generate routines, and keep habits on track with AI support.</p>
      <p>
        Open your <Link href="/dashboard">dashboard</Link> to get started.
      </p>
    </section>
  );
}
