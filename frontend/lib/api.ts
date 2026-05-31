const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export interface Task {
  id?: string;
  title: string;
  description?: string;
  duration: number;
  priority: number;
  deadline?: string;
}

export interface RoutineResponse {
  routine_id: string;
  recommendations: string[];
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}

export const api = {
  listTasks: () => request<Task[]>("/api/tasks"),
  createTask: (payload: Task) =>
    request<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  generateRoutine: () =>
    request<RoutineResponse>("/api/routines/generate", {
      method: "POST",
    }),
};
