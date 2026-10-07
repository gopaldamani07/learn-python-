
const API_BASE = '/api'
function errorMessage(data, status) {
  const detail = data?.detail
  if (typeof detail === 'string') return detail
  // pydantic prefixes messages raised from validators with "Value error, "
  if (Array.isArray(detail)) return detail.map((d) => d.msg.replace(/^Value error, /, '')).join('. ')
  if (status >= 500) return "The server isn't responding. Is the API running?"
  return 'Something went wrong. Please try again.'
}

async function request(method, path, { body, token } = {}) {
  const headers = {}
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  if (token) headers.Authorization = `Bearer ${token}`

  let response
  try {
    response = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    })
  } catch {
    throw new Error("Can't reach the server. Check your connection and try again.")
  }

  // DELETE answers 204 with no body, so there may be nothing to parse
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    const error = new Error(errorMessage(data, response.status))
    error.status = response.status
    throw error
  }
  return data
}

export async function login(username, password) {
  const data = await request('POST', '/login', { body: { username, password } })
  return data.bearer_token
}

export function signup(username, password, confirmPassword) {
  return request('POST', '/signup', {
    body: { username, password, confirm_password: confirmPassword },
  })
}

export function listTeams(token) {
  return request('GET', '/teams', { token })
}

export function searchTeams(token, name) {
  return request('GET', `/teams/search?name=${encodeURIComponent(name)}`, { token })
}

export function createTeam(token, team) {
  return request('POST', '/teams', { token, body: team })
}

export function updateTeam(token, id, team) {
  return request('PUT', `/teams/${id}`, { token, body: team })
}

export function deleteTeam(token, id) {
  return request('DELETE', `/teams/${id}`, { token })
}
