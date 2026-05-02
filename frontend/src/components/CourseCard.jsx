export default function CourseCard({ course, onEnroll }) {
  const { title, category, hours, emoji, bg, progress = 0, enrolled = false } = course
  return (
    <div className="course-card">
      <div style={{ height: 88, background: bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 34 }}>
        {emoji}
      </div>
      <div style={{ padding: '0.9rem 1rem' }}>
        <div style={{ fontSize: 10.5, fontWeight: 600, textTransform: 'uppercase', color: 'var(--rose)', letterSpacing: '0.5px', marginBottom: 5 }}>
          {category}
        </div>
        <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 7, lineHeight: 1.35 }}>{title}</div>
        <div style={{ fontSize: 12, color: 'var(--warm-gray)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>{hours} часов</span>
          <span className="cert-badge">✦ Сертификат</span>
        </div>
        {enrolled && (
          <div style={{ height: 3, background: '#f0ede8', borderRadius: 3, marginTop: 8, overflow: 'hidden' }}>
            <div style={{ height: '100%', background: 'var(--rose)', width: `${progress}%`, borderRadius: 3 }} />
          </div>
        )}
        <button
          onClick={() => onEnroll?.(course)}
          style={{
            display: 'block', width: '100%', marginTop: 10, padding: '8px',
            borderRadius: 8, border: '0.5px solid var(--rose)', color: 'var(--rose)',
            background: 'none', fontFamily: "'Outfit', sans-serif", fontSize: 12.5,
            fontWeight: 500, cursor: 'pointer', transition: 'all 0.15s'
          }}
          onMouseEnter={e => { e.target.style.background = 'var(--rose)'; e.target.style.color = 'white' }}
          onMouseLeave={e => { e.target.style.background = 'none'; e.target.style.color = 'var(--rose)' }}
        >
          {enrolled && progress > 0 ? 'Продолжить →' : 'Записаться →'}
        </button>
      </div>
    </div>
  )
}
