import { useState } from 'react'
import { clearSession, loadSession, saveSession } from './auth.js'
import LoginPage from './pages/LoginPage.jsx'
import RegisterPage from './pages/RegisterPage.jsx'
import TeamsPage from './pages/TeamsPage.jsx'

function App() {
  const [session, setSession] = useState(loadSession)
  const [page, setPage] = useState('login')
  // a one-off message for the login page, e.g. right after signing up
  const [loginNotice, setLoginNotice] = useState(null)

  function handleLogin(newSession) {
    saveSession(newSession)
    setSession(newSession)
    setLoginNotice(null)
  }

  function handleLogout() {
    clearSession()
    setSession(null)
  }

  function handleSessionExpired() {
    setLoginNotice({
      username: session.username,
      tone: 'info',
      text: 'Your session expired. Sign in again to continue.',
    })
    handleLogout()
  }

  function handleRegistered(username) {
    setLoginNotice({ username, tone: 'success', text: 'Account created. Sign in to continue.' })
    setPage('login')
  }

  function showRegister() {
    setLoginNotice(null)
    setPage('register')
  }

  if (!session) {
    if (page === 'register') {
      return <RegisterPage onRegistered={handleRegistered} onShowLogin={() => setPage('login')} />
    }
    return <LoginPage notice={loginNotice} onLogin={handleLogin} onShowRegister={showRegister} />
  }

  return (
    <TeamsPage session={session} onLogout={handleLogout} onSessionExpired={handleSessionExpired} />
  )
}

export default App
