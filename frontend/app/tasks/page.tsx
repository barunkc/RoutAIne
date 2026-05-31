"use client";

import { useState } from "react";
import { TaskForm } from "@/components/TaskForm";
import type { Task } from "@/lib/api";
import { formatDuration } from "@/lib/utils";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);

  return (
    <section>
      <h1>Task Manager</h1>
      <p>Create tasks with time allocation and priority.</p>
      <TaskForm onCreated={(task) => setTasks((current) => [...current, task])} />
      <ul style={{ marginTop: "1rem" }}>
        {tasks.map((task) => (
          <li key={`${task.title}-${task.duration}`}>
            {task.title} · {formatDuration(task.duration)} · Priority {task.priority}
          </li>
        ))}
      </ul>
    </section>
  );
}
