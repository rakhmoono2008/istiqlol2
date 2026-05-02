import { useState } from 'react'
import LandingPage from './pages/LandingPage'
import SeekerDashboard from './pages/SeekerDashboard'
import EmployerDashboard from './pages/EmployerDashboard'

export default function App() {
  const [role, setRole] = useState(null)
  if (!role) return <LandingPage onSelect={setRole} />
  if (role === 'seeker') return <SeekerDashboard onBack={() => setRole(null)} />
  return <EmployerDashboard onBack={() => setRole(null)} />
}
