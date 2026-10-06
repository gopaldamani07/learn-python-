
const API_BASE = '/api'
function errorMessage(data, status) {
  const detail = data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) return detail.map((d) => d.msg).join('. ')
  if (status >= 500) return "The server isn't responding. Is the API running?"
  return 'Something went wrong. Please try again.'
}

export async function login(username, password) {
  let response
  try {
    response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
  } catch {
    throw new Error("Can't reach the server. Check your connection and try again.")
  }

  const data = await response.json().catch(() => null)
  if (!response.ok) {
    throw new Error(errorMessage(data, response.status))
  }
  return data.bearer_token
}
