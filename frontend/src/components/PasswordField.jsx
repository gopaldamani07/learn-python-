import { useState } from 'react'

function PasswordField({ id, label, autoComplete, autoFocus = false, value, onChange }) {
  const [showPassword, setShowPassword] = useState(false)

  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <div className="password-row">
        <input
          id={id}
          type={showPassword ? 'text' : 'password'}
          autoComplete={autoComplete}
          autoFocus={autoFocus}
          value={value}
          onChange={(event) => onChange(event.target.value)}
        />
        <button
          type="button"
          className="toggle-password"
          aria-pressed={showPassword}
          onClick={() => setShowPassword((show) => !show)}
        >
          {showPassword ? 'Hide' : 'Show'}
        </button>
      </div>
    </div>
  )
}

export default PasswordField
