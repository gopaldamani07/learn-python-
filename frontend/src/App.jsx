import { useState } from 'react'
import { clearSession, loadSession, saveSession } from './auth.js'
import LoginPage from './pages/LoginPage.jsx'

function App() {
  const [session, setSession] = useState(loadSession)

  function handleLogin(newSession) {
    saveSession(newSession)
    setSession(newSession)
  }

  function handleLogout() {
    clearSession()
    setSession(null)
  }

  if (!session) {
    return <LoginPage onLogin={handleLogin} />
  }

  // Placeholder until the next page is built
  return (
    <main className="page">
      <section className="card">
        <h1>You're signed in</h1>
        <p className="muted">
          Welcome, <strong>{session.username}</strong>.
        </p>
        <button type="button" className="button" onClick={handleLogout}>
          Sign out
        </button>
      </section>
    </main>
  )
}

export default App
