import { useEffect, useState } from 'react'
import { createTeam, deleteTeam, listTeams, searchTeams, updateTeam } from '../api.js'
import TeamForm from '../components/TeamForm.jsx'
import './TeamsPage.css'

function formatDate(value) {
  return new Date(value).toLocaleDateString(undefined, { dateStyle: 'medium' })
}

function TeamItem({ team, isOwner, onUpdate, onDelete }) {
  const [mode, setMode] = useState('view') // 'view' | 'edit' | 'confirm-delete'
  const [deleting, setDeleting] = useState(false)
  const [error, setError] = useState('')

  async function handleUpdate(changes) {
    await onUpdate(team.id, changes)
    setMode('view')
  }

  async function handleDelete() {
    setError('')
    setDeleting(true)
    try {
      await onDelete(team.id)
    } catch (err) {
      setError(err.message)
      setDeleting(false)
    }
  }

  if (mode === 'edit') {
    return (
      <li className="team">
        <TeamForm
          idPrefix={`team-${team.id}`}
          team={team}
          submitLabel="Save changes"
          savingLabel="Saving…"
          onSubmit={handleUpdate}
          onCancel={() => setMode('view')}
        />
      </li>
    )
  }

  if (mode === 'confirm-delete') {
    return (
      <li className="team">
        <div className="team-info">
          <p>
            Delete <strong>{team.name}</strong>? This can't be undone.
          </p>
          {error && (
            <p className="form-error" role="alert">
              {error}
            </p>
          )}
        </div>
        <div className="team-actions">
          <button
            type="button"
            className="button button-small button-danger"
            disabled={deleting}
            onClick={handleDelete}
          >
            {deleting ? 'Deleting…' : 'Delete team'}
          </button>
          <button
            type="button"
            className="button button-small button-secondary"
            onClick={() => setMode('view')}
          >
            Cancel
          </button>
        </div>
      </li>
    )
  }

  return (
    <li className="team">
      <div className="team-info">
        <h3>{team.name}</h3>
        {team.description && <p>{team.description}</p>}
        <p className="team-meta">
          Owner: {isOwner ? 'you' : team.owner} · Created {formatDate(team.created_at)}
        </p>
      </div>
      {/* the API only lets the owner change or delete a team */}
      {isOwner && (
        <div className="team-actions">
          <button
            type="button"
            className="button button-small button-secondary"
            onClick={() => setMode('edit')}
          >
            Edit
          </button>
          <button
            type="button"
            className="button button-small button-secondary"
            onClick={() => setMode('confirm-delete')}
          >
            Delete
          </button>
        </div>
      )}
    </li>
  )
}

function TeamsPage({ session, onLogout, onSessionExpired }) {
  const [teams, setTeams] = useState(null) // null until the first load finishes
  const [query, setQuery] = useState('')
  const [loadError, setLoadError] = useState('')
  const [reloadCount, setReloadCount] = useState(0)

  const search = query.trim()

  useEffect(() => {
    let ignore = false
    // wait for a pause in typing before searching
    const timer = setTimeout(
      async () => {
        try {
          const data = search
            ? await searchTeams(session.token, search)
            : await listTeams(session.token)
          if (ignore) return
          setTeams(data)
          setLoadError('')
        } catch (err) {
          if (ignore) return
          if (err.status === 401) onSessionExpired()
          else setLoadError(err.message)
        }
      },
      search ? 250 : 0,
    )
    return () => {
      ignore = true
      clearTimeout(timer)
    }
  }, [search, session.token, reloadCount, onSessionExpired])

  function reload() {
    setReloadCount((count) => count + 1)
  }

  // a 401 means the token ran out, so send the user back to sign in
  async function callApi(apiFunction, ...args) {
    try {
      return await apiFunction(session.token, ...args)
    } catch (err) {
      if (err.status === 401) onSessionExpired()
      throw err
    }
  }

  async function handleCreate(team) {
    await callApi(createTeam, team)
    // clear the search so the new team is visible in the list
    setQuery('')
    reload()
  }

  async function handleUpdate(id, changes) {
    const updated = await callApi(updateTeam, id, changes)
    setTeams((current) => current.map((team) => (team.id === id ? updated : team)))
  }

  async function handleDelete(id) {
    await callApi(deleteTeam, id)
    setTeams((current) => current.filter((team) => team.id !== id))
  }

  return (
    <main className="teams-page">
      <header className="teams-header">
        <div>
          <h1>Teams</h1>
          <p className="muted">
            Signed in as <strong>{session.username}</strong>
          </p>
        </div>
        <button type="button" className="button button-secondary" onClick={onLogout}>
          Sign out
        </button>
      </header>

      <section className="panel">
        <h2>New team</h2>
        <TeamForm
          idPrefix="new-team"
          submitLabel="Create team"
          savingLabel="Creating…"
          onSubmit={handleCreate}
        />
      </section>

      <section className="panel">
        <div className="list-header">
          <h2>All teams</h2>
          <div className="field">
            <input
              type="search"
              placeholder="Search by name"
              aria-label="Search teams by name"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </div>
        </div>

        {loadError && (
          <p className="form-error list-message" role="alert">
            {loadError}{' '}
            <button type="button" className="link-button" onClick={reload}>
              Try again
            </button>
          </p>
        )}

        {teams === null && !loadError && <p className="muted list-message">Loading teams…</p>}

        {teams?.length === 0 && (
          <p className="muted list-message">
            {search ? `No teams match "${search}".` : 'No teams yet. Create the first one above.'}
          </p>
        )}

        {teams?.length > 0 && (
          <ul className="team-list">
            {teams.map((team) => (
              <TeamItem
                key={team.id}
                team={team}
                isOwner={team.owner === session.username}
                onUpdate={handleUpdate}
                onDelete={handleDelete}
              />
            ))}
          </ul>
        )}
      </section>
    </main>
  )
}

export default TeamsPage
