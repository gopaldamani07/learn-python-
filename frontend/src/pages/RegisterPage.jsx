import { useState } from 'react'
import { signup } from '../api.js'
import PasswordField from '../components/PasswordField.jsx'
import './AuthForm.css'

function RegisterPage({ onRegistered, onShowLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()

    if (!username || !password || !confirmPassword) {
      setError('Enter a username, a password, and confirm the password.')
      return
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    setError('')
    setLoading(true)
    try {
      await signup(username, password, confirmPassword)
      onRegistered(username)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page">
      <section className="card">
        <h1>Create an account</h1>
        <p className="muted">Choose a username and password to get started.</p>

        <form className="auth-form" onSubmit={handleSubmit} noValidate>
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
              autoFocus
              value={username}
              onChange={(event) => setUsername(event.target.value)}
            />
          </div>

          <PasswordField
            id="password"
            label="Password"
            autoComplete="new-password"
            value={password}
            onChange={setPassword}
          />

          <PasswordField
            id="confirm-password"
            label="Confirm password"
            autoComplete="new-password"
            value={confirmPassword}
            onChange={setConfirmPassword}
          />

          <button type="submit" className="button" disabled={loading}>
            {loading ? 'Creating account…' : 'Create account'}
          </button>
        </form>

        <p className="switch-page">
          Already have an account?{' '}
          <button type="button" className="link-button" onClick={onShowLogin}>
            Sign in
          </button>
        </p>
      </section>
    </main>
  )
}

export default RegisterPage
