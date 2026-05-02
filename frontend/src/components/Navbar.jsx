export default function Navbar({ role, activeTab, onTabChange, onBack }) {
  const tabs = [
    { key: 'home', label: 'Главная' },
    { key: 'courses', label: 'Курсы' },
    { key: 'biographies', label: 'Биографии' },
    { key: 'profile', label: 'Профиль' },
  ]

  return (
    <nav style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0 2rem', height: 58, background: 'white',
      borderBottom: '0.5px solid var(--border)',
      position: 'sticky', top: 0, zIndex: 200
    }}>
      <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 21, display: 'flex', alignItems: 'center', gap: 7 }}>
        <div style={{ width: 8, height: 8, background: 'var(--rose)', borderRadius: '50%' }} />
        Istiqlol
      </div>

      {role === 'seeker' && (
        <div style={{ display: 'flex', gap: '2rem' }}>
          {tabs.map(({ key, label }) => (
            <span
              key={key}
              onClick={() => onTabChange(key)}
              style={{
                fontSize: 14,
                color: activeTab === key ? 'var(--dark)' : 'var(--warm-gray)',
                cursor: 'pointer',
                padding: '4px 0',
                borderBottom: `2px solid ${activeTab === key ? 'var(--rose)' : 'transparent'}`,
                transition: 'all 0.2s'
              }}
            >
              {label}
            </span>
          ))}
        </div>
      )}

      <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
        {role ? (
          <button className="btn btn-ghost" onClick={onBack}>← Выход</button>
        ) : (
          <>
            <button className="btn btn-outline">Войти</button>
            <button className="btn btn-primary">Войти через One ID</button>
          </>
        )}
      </div>
    </nav>
  )
}
