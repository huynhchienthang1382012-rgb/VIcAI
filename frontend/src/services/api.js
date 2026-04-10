import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const http = axios.create({ baseURL: API_URL })

export const setToken = (token) => {
  http.defaults.headers.common.Authorization = `Bearer ${token}`
}

export async function register(email, password) {
  const { data } = await http.post('/auth/register', { email, password })
  return data
}

export async function login(email, password) {
  const { data } = await http.post('/auth/login', { email, password })
  return data
}

export async function listConversations() {
  const { data } = await http.get('/conversations')
  return data
}

export async function createConversation(payload) {
  const { data } = await http.post('/conversations', payload)
  return data
}

export async function listMessages(conversationId) {
  const { data } = await http.get(`/conversations/${conversationId}/messages`)
  return data
}

export async function streamChat(conversationId, payload, onToken, onMeta) {
  const res = await fetch(`${API_URL}/chat/${conversationId}/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: http.defaults.headers.common.Authorization
    },
    body: JSON.stringify(payload)
  })

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buf = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buf += decoder.decode(value, { stream: true })

    const events = buf.split('\n\n')
    buf = events.pop() || ''

    for (const event of events) {
      const lines = event.split('\n')
      const eventType = lines.find((l) => l.startsWith('event:'))?.replace('event:', '').trim()
      const dataLine = lines.find((l) => l.startsWith('data:'))?.replace('data:', '').trim() || ''
      if (eventType === 'token') onToken(dataLine)
      if (eventType === 'meta') onMeta(JSON.parse(dataLine))
    }
  }
}
