export type Role = "admin" | "user";

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: Role;
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}
