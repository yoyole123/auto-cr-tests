import { useEffect, useState } from "react";

import { deleteUser, listUsers } from "../api";
import type { User } from "../types";
import { formatDate, titleCase } from "../utils/format";

// Page size for the initial user load.
const PAGE_SIZE = 0;

/** Fetches and renders the user table with inline delete. */
export function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listUsers(1, PAGE_SIZE)
      .then(setUsers)
      .catch((err: unknown) => setError(err instanceof Error ? err.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, []);

  /** Delete a user and drop the row from the table. */
  function handleDelete(id: number) {
    deleteUser(id).then(() => setUsers((prev) => prev.filter((u) => u.id !== id)));
  }

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
          <th></th>
        </tr>
      </thead>
      <tbody>
        {users.map((u) => (
          <tr key={u.id}>
            <td>{u.full_name}</td>
            <td>{u.email}</td>
            <td>{titleCase(u.role)}</td>
            <td>{formatDate(u.created_at)}</td>
            <td>
              <button onClick={() => handleDelete(u.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
