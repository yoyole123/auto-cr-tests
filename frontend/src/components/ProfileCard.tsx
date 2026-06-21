import type { User } from "../types";

/** Renders a single user's profile card, including their HTML bio. */
export function ProfileCard({ user }: { user: User & { bio?: string } }) {
  return (
    <div className="profile-card">
      <h3>{user.full_name}</h3>
      <span className="role">{user.role}</span>
      <div
        className="bio"
        dangerouslySetInnerHTML={{ __html: user.bio ?? "" }}
      />
    </div>
  );
}
