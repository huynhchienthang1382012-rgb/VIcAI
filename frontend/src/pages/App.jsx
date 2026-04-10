import { useEffect, useState } from 'react'
import { Sidebar } from '../components/Sidebar'
import { MessageBubble } from '../components/MessageBubble'
import { Composer } from '../components/Composer'
import {
  createConversation,
  listConversations,
  listMessages,
  login,
  register,
  setToken,
  streamChat
} from '../services/api'

export function App() {
  const [token, setAuthToken] = useState(localStorage.getItem('token') || '')
  const [email, setEmail] = useState('demo@viciai.dev')
  const [password, setPassword] = useState('12345678')
  const [conversations, setConversations] = useState([])
  const [currentId, setCurrentId] = useState(null)
  const [messages, setMessages] = useState([])
  const [busy, setBusy] = useState(false)
  const [theme, setTheme] = useState('dark')

  useEffect(() => document.body.dataset.theme = theme, [theme])

  useEffect(() => {
    if (!token) return
    setToken(token)
    bootstrap()
  }, [token])

  async function bootstrap() {
    const list = await listConversations()
    setConversations(list)
    if (list[0]) selectConversation(list[0].id)
  }

  async function auth(isRegister) {
    const action = isRegister ? register : login
    const data = await action(email, password)
    localStorage.setItem('token', data.access_token)
    setAuthToken(data.access_token)
  }

  async function createNewConversation() {
    const c = await createConversation({ title: `Chat ${new Date().toLocaleString()}`, mode: 'normal' })
    setConversations((prev) => [c, ...prev])
    setCurrentId(c.id)
    setMessages([])
  }

  async function selectConversation(id) {
    setCurrentId(id)
    const data = await listMessages(id)
    setMessages(data)
  }

  async function sendMessage(content, mode) {
    if (!currentId) return
    setBusy(true)
    const tempUser = { role: 'user', content }
    const tempAssistant = { role: 'assistant', content: '' }
    setMessages((prev) => [...prev, tempUser, tempAssistant])

    await streamChat(
      currentId,
      { content, mode },
      (token) => setMessages((prev) => {
        const copy = [...prev]
        copy[copy.length - 1] = { ...copy[copy.length - 1], content: copy[copy.length - 1].content + token }
        return copy
      }),
      () => null
    )
    setBusy(false)
  }

  if (!token) {
    return (
      <div className="auth-screen">
        <div className="auth-box">
          <h1>VicAI Assistant</h1>
          <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
          <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" />
          <button onClick={() => auth(false)}>Đăng nhập</button>
          <button className="secondary" onClick={() => auth(true)}>Tạo tài khoản</button>
        </div>
      </div>
    )
  }

  return (
    <div className="app-layout">
      <Sidebar conversations={conversations} currentId={currentId} onSelect={selectConversation} onCreate={createNewConversation} />
      <main className="chat-pane">
        <header>
          <h2>Trợ lý AI đa lĩnh vực</h2>
          <button onClick={() => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))}>{theme}</button>
        </header>
        <section className="messages">
          {messages.map((m, idx) => <MessageBubble key={idx} message={m} />)}
        </section>
        <Composer onSend={sendMessage} busy={busy} />
      </main>
    </div>
  )
}
