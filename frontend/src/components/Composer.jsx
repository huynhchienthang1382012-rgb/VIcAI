import { useState } from 'react'

const MODES = ['normal', 'deep', 'fast', 'teach', 'code', 'summary']

export function Composer({ onSend, busy }) {
  const [text, setText] = useState('')
  const [mode, setMode] = useState('normal')

  return (
    <div className="composer-wrap">
      <select value={mode} onChange={(e) => setMode(e.target.value)}>
        {MODES.map((m) => <option key={m}>{m}</option>)}
      </select>
      <textarea
        rows={3}
        placeholder="Nhập câu hỏi..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button
        disabled={busy || !text.trim()}
        onClick={() => {
          onSend(text, mode)
          setText('')
        }}
      >
        {busy ? 'Đang xử lý...' : 'Gửi'}
      </button>
    </div>
  )
}
