const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const h = () => ({
  'Content-Type': 'application/json',
  ...(localStorage.getItem('token') ? { Authorization: `Bearer ${localStorage.getItem('token')}` } : {})
})

export const api = {
  async demoLogin(role) {
    const r = await fetch(`${BASE}/auth/demo-login?role=${role}`, { method: 'POST', headers: h() })
    const d = await r.json()
    if (d.access_token) { localStorage.setItem('token', d.access_token); localStorage.setItem('userId', d.user_id) }
    return d
  },
  async getJobs(params = {}) {
    const q = new URLSearchParams(params).toString()
    return (await fetch(`${BASE}/jobs/?${q}`, { headers: h() })).json()
  },
  async getRecommendedJobs(userId) {
    return (await fetch(`${BASE}/recommendations/jobs?user_id=${userId}`, { headers: h() })).json()
  },
  async getRecommendedCourses(userId) {
    return (await fetch(`${BASE}/recommendations/courses?user_id=${userId}`, { headers: h() })).json()
  },
  async getProfile(userId) {
    return (await fetch(`${BASE}/profile/${userId}`, { headers: h() })).json()
  },
  async updateProfile(userId, data) {
    return (await fetch(`${BASE}/profile/${userId}`, { method: 'PUT', headers: h(), body: JSON.stringify(data) })).json()
  },
  async getCourses() {
    return (await fetch(`${BASE}/courses/`, { headers: h() })).json()
  },
  async getBiographies() {
    return (await fetch(`${BASE}/courses/biographies`, { headers: h() })).json()
  },
  async createJob(data) {
    return (await fetch(`${BASE}/jobs/`, { method: 'POST', headers: h(), body: JSON.stringify(data) })).json()
  },
  loginUrl: (role) => `${BASE}/auth/login?role=${role}`
}
