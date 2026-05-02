export default function JobCard({ job }) {
  const { title, company, match, skills = [], salary, location, emoji = '💼' } = job
  return (
    <div className="job-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
        <div style={{
          width: 44, height: 44, borderRadius: 10,
          background: 'var(--sage-light)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 18
        }}>{emoji}</div>
        {match && <span className="match-badge">{match}% совпадение</span>}
      </div>
      <div style={{ fontSize: 15, fontWeight: 500, marginBottom: 3 }}>{title}</div>
      <div style={{ fontSize: 13, color: 'var(--warm-gray)', marginBottom: '0.65rem' }}>{company}</div>
      <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap', marginBottom: '0.65rem' }}>
        {skills.map(s => <span key={s} className="tag">{s}</span>)}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '0.5px solid #f0ede8', paddingTop: '0.65rem' }}>
        <span style={{ fontSize: 14, fontWeight: 500 }}>{salary}</span>
        <span style={{ fontSize: 12, color: 'var(--warm-gray)' }}>{location}</span>
      </div>
    </div>
  )
}
