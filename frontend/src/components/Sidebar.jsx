const NAV = [
  { key: 'home',        icon: '✦', label: 'Главная' },
  { key: 'courses',     icon: '◈', label: 'Курсы' },
  { key: 'biographies', icon: '◎', label: 'Биографии' },
  { key: 'profile',     icon: '○', label: 'Профиль' },
]

export default function Sidebar({ activeTab, onTabChange, userName = 'М', displayName = 'Малика А.' }) {
  return (
    <aside style={{
      background: 'white', borderRight: '0.5px solid var(--border)',
      padding: '1.25rem 0.875rem', display: 'flex', flexDirection: 'column', gap: '1.5rem',
      width: 220, flexShrink: 0
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '0.6rem 0.5rem' }}>
        <div className="avatar">{userName}</div>
        <div>
          <div style={{ fontSize: 14, fontWeight: 500 }}>{displayName}</div>
          <div style={{ fontSize: 12, color: 'var(--warm-gray)' }}>Соискатель</div>
        </div>
      </div>

      <nav style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        {NAV.map(({ key, icon, label }) => (
          <div
            key={key}
            onClick={() => onTabChange(key)}
            style={{
              display: 'flex', alignItems: 'center', gap: 9,
              padding: '9px 11px', borderRadius: 10, fontSize: 14,
              color: activeTab === key ? 'var(--rose)' : 'var(--warm-gray)',
              background: activeTab === key ? 'var(--rose-light)' : 'transparent',
              fontWeight: activeTab === key ? 500 : 400,
              cursor: 'pointer', transition: 'all 0.15s'
            }}
          >
            <span style={{ fontSize: 15, width: 18, textAlign: 'center' }}>{icon}</span>
            {label}
          </div>
        ))}
      </nav>
    </aside>
  )
}
