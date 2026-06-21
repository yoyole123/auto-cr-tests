import { useState } from "react";

import { clearToken, isLoggedIn } from "./auth";
import { LoginForm } from "./components/LoginForm";
import { UserList } from "./components/UserList";

/** Top-level app: shows the login form or the user list depending on auth state. */
export function App() {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());

  function handleLogout() {
    clearToken();
    setLoggedIn(false);
  }

  if (!loggedIn) {
    return <LoginForm onLoggedIn={() => setLoggedIn(true)} />;
  }

  return (
    <main>
      <header>
        <h1>Users</h1>
        <button onClick={handleLogout}>Log out</button>
      </header>
      <UserList />
    </main>
  );
}
