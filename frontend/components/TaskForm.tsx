"use client";

import { FormEvent, useState } from "react";
import { api, Task } from "@/lib/api";

interface TaskFormProps {
  onCreated?: (task: Task) => void;
}

export function TaskForm({ onCreated }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [duration, setDuration] = useState(30);
  const [priority, setPriority] = useState(3);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);

    try {
      const task = await api.createTask({ title, duration, priority });
      onCreated?.(task);
      setTitle("");
    } catch (error) {
      console.error("Failed to create task", error);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: "0.75rem", maxWidth: "24rem" }}>
      <label>
        Task title
        <input value={title} onChange={(event) => setTitle(event.target.value)} required />
      </label>
      <label>
        Duration (minutes)
        <input
          type="number"
          min={5}
          value={duration}
          onChange={(event) => setDuration(Number(event.target.value))}
          required
        />
      </label>
      <label>
        Priority (1-5)
        <input
          type="number"
          min={1}
          max={5}
          value={priority}
          onChange={(event) => setPriority(Number(event.target.value))}
          required
        />
      </label>
      <button type="submit" disabled={submitting}>
        {submitting ? "Saving..." : "Create Task"}
      </button>
    </form>
  );
}
