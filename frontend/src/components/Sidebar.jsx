export function Sidebar({ conversations, currentId, onSelect, onCreate }) {
  return (
    <aside className="sidebar">
      <div className="brand">VicAI</div>
      <button className="new-btn" onClick={onCreate}>+ Cuộc hội thoại mới</button>
      <div className="history">
        {conversations.map((c) => (
          <button
            key={c.id}
            className={`history-item ${currentId === c.id ? 'active' : ''}`}
            onClick={() => onSelect(c.id)}
          >
            {c.title}
          </button>
        ))}
      </div>
    </aside>
  )
}
