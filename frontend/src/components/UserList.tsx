import { useEffect, useState } from "react";

import { listUsers } from "../api";
import type { User } from "../types";
import { formatDate, titleCase } from "../utils/format";

/** Fetches and renders the user table. */
export function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listUsers()
      .then(setUsers)
      .catch((err: unknown) => setError(err instanceof Error ? err.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading users...</p>;
  if (error) return <p role="alert">{error}</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
          <th>Joined</th>
        </tr>
      </thead>
      <tbody>
        {users.map((u) => (
          <tr key={u.id}>
            <td>{u.full_name}</td>
            <td>{u.email}</td>
            <td>{titleCase(u.role)}</td>
            <td>{formatDate(u.created_at)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
