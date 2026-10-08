import { useState } from 'react'
import { login } from '../api.js'
import PasswordField from '../components/PasswordField.jsx'
import './AuthForm.css'


function LoginPage({ notice, onLogin, onShowRegister }) {
  const knownUsername = notice?.username ?? ''
  const [username, setUsername] = useState(knownUsername)
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()

    if (!username || !password) {
      setError('Enter your username and password.')
      return
    }

    setError('')
    setLoading(true)
    try {
      const token = await login(username, password)
      onLogin({ username, token })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page">
      <section className="card">
        <h1>Sign in</h1>
        <p className="muted">Use your account to manage your teams.</p>

        <form className="auth-form" onSubmit={handleSubmit} noValidate>
          {notice && !error && (
            <p className={`form-${notice.tone}`} role="status">
              {notice.text}
            </p>
          )}

          {error && (
            <p className="form-error" role="alert">
              {error}
            </p>
          )}

          <div className="field">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              autoComplete="username"
              autoCapitalize="none"
              spellCheck={false}
              autoFocus={!knownUsername}
              value={username}
              onChange={(event) => setUsername(event.target.value)}
            />
          </div>

          <PasswordField
            id="password"
            label="Password"
            autoComplete="current-password"
            autoFocus={Boolean(knownUsername)}
            value={password}
            onChange={setPassword}
          />

          <button type="submit" className="button" disabled={loading}>
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <p className="switch-page">
          New here?{' '}
          <button type="button" className="link-button" onClick={onShowRegister}>
            Create an account
          </button>
        </p>
      </section>
    </main>
  )
}

export default LoginPage
