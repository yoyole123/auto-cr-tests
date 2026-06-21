/** Thin fetch client for the backend API. */
import { getToken } from "./auth";
import type { LoginResponse, User } from "./types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string>),
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const resp = await fetch(`${BASE_URL}${path}`, { ...init, headers });
  if (!resp.ok) {
    const detail = await resp.text();
    throw new Error(`Request failed (${resp.status}): ${detail}`);
  }
  return resp.status === 204 ? (undefined as T) : ((await resp.json()) as T);
}

export function login(email: string, password: string): Promise<LoginResponse> {
  return request<LoginResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function registerUser(email: string, password: string, fullName: string): Promise<User> {
  return request<User>("/users", {
    method: "POST",
    body: JSON.stringify({ email, password, full_name: fullName }),
  });
}

export function listUsers(page = 1, pageSize = 20): Promise<User[]> {
  return request<User[]>(`/users?page=${page}&page_size=${pageSize}`);
}

export function deleteUser(id: number): Promise<void> {
  return request<void>(`/users/${id}`, { method: "DELETE" });
}
