"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { RoutineCard } from "@/components/RoutineCard";

export default function DashboardPage() {
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleGenerateRoutine() {
    setLoading(true);
    try {
      const routine = await api.generateRoutine();
      setRecommendations(routine.recommendations);
    } catch (error) {
      console.error("Failed to generate routine", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h1>Dashboard</h1>
      <p>Overview of today&apos;s routine and upcoming tasks.</p>
      <button type="button" onClick={handleGenerateRoutine} disabled={loading}>
        {loading ? "Generating..." : "Generate AI Routine"}
      </button>
      <div style={{ marginTop: "1rem" }}>
        {recommendations.map((recommendation, index) => (
          <RoutineCard
            key={`${recommendation}-${index}`}
            title={`Recommendation ${index + 1}`}
            timeSlot="Flexible"
            recommendation={recommendation}
          />
        ))}
      </div>
    </section>
  );
}
