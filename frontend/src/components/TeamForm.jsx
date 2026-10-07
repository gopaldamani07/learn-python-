import { useState } from 'react'

// Used for both creating a team and editing one (pass `team` to edit).
function TeamForm({ idPrefix, team, submitLabel, savingLabel, onSubmit, onCancel }) {
  const [name, setName] = useState(team?.name ?? '')
  const [description, setDescription] = useState(team?.description ?? '')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()

    if (!name.trim()) {
      setError('Enter a team name.')
      return
    }

    setError('')
    setSaving(true)
    try {
      await onSubmit({ name: name.trim(), description: description.trim() || null })
      if (!team) {
        setName('')
        setDescription('')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <form className="team-form" onSubmit={handleSubmit} noValidate>
      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}

      <div className="field">
        <label htmlFor={`${idPrefix}-name`}>Name</label>
        <input
          id={`${idPrefix}-name`}
          type="text"
          autoComplete="off"
          autoFocus={Boolean(team)}
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
      </div>

      <div className="field">
        <label htmlFor={`${idPrefix}-description`}>Description (optional)</label>
        <textarea
          id={`${idPrefix}-description`}
          rows={2}
          value={description}
          onChange={(event) => setDescription(event.target.value)}
        />
      </div>

      <div className="form-actions">
        <button type="submit" className="button" disabled={saving}>
          {saving ? savingLabel : submitLabel}
        </button>
        {onCancel && (
          <button type="button" className="button button-secondary" onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>
    </form>
  )
}

export default TeamForm
