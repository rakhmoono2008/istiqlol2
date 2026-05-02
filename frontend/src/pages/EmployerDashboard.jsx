import { useState } from 'react'
import { api } from '../services/api'
import s from './Employer.module.css'

const VACANCIES = [
  { id:1, title:'UX/UI Дизайнер',    responses:47, days:3,  status:'active' },
  { id:2, title:'Frontend Developer', responses:89, days:7,  status:'active' },
  { id:3, title:'Marketing Manager',  responses:23, days:14, status:'paused' },
]

export default function EmployerDashboard({ onBack }) {
  const [view, setView]   = useState('list')
  const [saved, setSaved] = useState(false)
  const [form, setForm]   = useState({
    title:'', category:'IT', work_format:'office',
    salary_min:'', salary_currency:'UZS', description:'', skills:''
  })
  const set = k => e => setForm(f=>({...f,[k]:e.target.value}))

  const submit = () => {
    if (!form.title.trim()) return alert('Введите название вакансии')
    setSaved(true)
    setTimeout(() => { setSaved(false); setView('list') }, 1500)
  }

  return (
    <div className={s.page}>
      <nav className={s.nav}>
        <div className={s.logo}><span className={s.dot}/>Istiqlol</div>
        <div className={s.coInfo}>
          <span className={s.coName}>Click Technologies</span>
          <span className={s.verBadge}>✓ Верифицировано</span>
        </div>
        <button className={s.backBtn} onClick={onBack}>Выйти</button>
      </nav>

      <div className={s.body}>
        <div className={s.topRow}>
          <div>
            <h2 className={s.h2}>Панель работодателя</h2>
            <p className={s.sub}>Управляйте вакансиями и откликами</p>
          </div>
          {view==='list' && (
            <button className={s.postBtn} onClick={()=>setView('post')}>+ Разместить вакансию</button>
          )}
        </div>

        {/* Stats */}
        <div className={s.statsGrid}>
          {[['12','Активных вакансий','var(--rose)'],['284','Всего откликов','var(--sage)'],['43','Просмотры сегодня','var(--dark)'],['8','На рассмотрении','var(--gold)']].map(([n,l,c])=>(
            <div key={l} className={s.statCard}>
              <div className={s.statNum} style={{color:c}}>{n}</div>
              <div className={s.statLabel}>{l}</div>
            </div>
          ))}
        </div>

        {/* List */}
        {view==='list' && (
          <div className={s.card}>
            <div className={s.cardHead}>Ваши вакансии</div>
            {VACANCIES.map(v=>(
              <div key={v.id} className={s.vacRow}>
                <div>
                  <div className={s.vacTitle}>{v.title}</div>
                  <div className={s.vacMeta}>Опубликовано {v.days} дн. назад · {v.responses} откликов</div>
                </div>
                <div className={s.vacRight}>
                  <span className={`${s.badge} ${v.status==='active'?s.badgeGreen:s.badgeGray}`}>
                    {v.status==='active'?'Активна':'Приостановлена'}
                  </span>
                  <button className={s.editVacBtn}>Редактировать</button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Post form */}
        {view==='post' && (
          <div className={s.formCard}>
            <div className={s.formTitle}>Новая вакансия</div>
            <div className={s.formGrid}>
              <div className={s.field}>
                <label className={s.label}>Название должности *</label>
                <input className={s.input} placeholder="UX/UI Дизайнер" value={form.title} onChange={set('title')}/>
              </div>
              <div className={s.field}>
                <label className={s.label}>Категория</label>
                <select className={s.input} value={form.category} onChange={set('category')}>
                  {['IT','Маркетинг','Финансы','HR','Образование','Медицина'].map(c=><option key={c}>{c}</option>)}
                </select>
              </div>
              <div className={s.field}>
                <label className={s.label}>Формат работы</label>
                <select className={s.input} value={form.work_format} onChange={set('work_format')}>
                  <option value="office">Офис</option>
                  <option value="remote">Удалённо</option>
                  <option value="hybrid">Гибрид</option>
                </select>
              </div>
              <div className={s.field}>
                <label className={s.label}>Зарплата от</label>
                <div className={s.salaryRow}>
                  <input className={s.input} placeholder="5 000 000" value={form.salary_min} onChange={set('salary_min')} style={{flex:1}}/>
                  <select className={s.input} value={form.salary_currency} onChange={set('salary_currency')} style={{width:'90px'}}>
                    <option>UZS</option><option>USD</option><option>EUR</option>
                  </select>
                </div>
              </div>
            </div>
            <div className={s.field}>
              <label className={s.label}>Описание вакансии</label>
              <textarea className={s.textarea} rows={4} placeholder="Опишите обязанности, требования и условия работы..." value={form.description} onChange={set('description')}/>
            </div>
            <div className={s.field}>
              <label className={s.label}>Ключевые навыки (через запятую)</label>
              <input className={s.input} placeholder="Figma, Prototyping, User Research" value={form.skills} onChange={set('skills')}/>
            </div>
            <div className={s.formActions}>
              <button className={s.submitBtn} onClick={submit}>
                {saved ? '✓ Опубликовано!' : 'Опубликовать вакансию'}
              </button>
              <button className={s.cancelBtn} onClick={()=>setView('list')}>Отмена</button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
