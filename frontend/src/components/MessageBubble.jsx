import ReactMarkdown from 'react-markdown'

export function MessageBubble({ message }) {
  return (
    <div className={`bubble ${message.role}`}>
      <div className="role">{message.role === 'assistant' ? 'VicAI' : 'Bạn'}</div>
      <ReactMarkdown>{message.content}</ReactMarkdown>
    </div>
  )
}
