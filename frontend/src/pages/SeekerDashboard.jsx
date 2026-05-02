import { useState, useEffect } from 'react'
import s from './Seeker.module.css'
import { api } from '../services/api'

/* ─── Static fallback data ─── */
const JOBS = [
  { id:1, title:'UX/UI Дизайнер',    company:'Click Technologies', company_verified:true,  match:94, required_skills:['Figma','Mobile','Research'],     salary:'5–8 млн сум',   location:'2.4 км',  work_format:'office' },
  { id:2, title:'Product Designer',  company:'Uzcard',             company_verified:true,  match:88, required_skills:['Prototyping','User Testing'],     salary:'$800–1200',     location:'Удалённо', work_format:'remote' },
  { id:3, title:'Marketing Manager', company:'Hamkorbank',         company_verified:false, match:82, required_skills:['Digital','SMM','Analytics'],      salary:'4–6 млн сум',   location:'5.1 км',  work_format:'hybrid' },
  { id:4, title:'Brand Designer',    company:'Beeline UZ',         company_verified:true,  match:79, required_skills:['Branding','Illustrator'],         salary:'6–9 млн сум',   location:'3.7 км',  work_format:'office' },
  { id:5, title:'Data Analyst',      company:'Payme',              company_verified:true,  match:73, required_skills:['SQL','Python','Tableau'],         salary:'$600–900',      location:'Удалённо', work_format:'remote' },
  { id:6, title:'HR Generalist',     company:'Ucell',              company_verified:false, match:68, required_skills:['Recruitment','HR','Excel'],       salary:'3–5 млн сум',   location:'1.2 км',  work_format:'office' },
]
const COURSES = [
  { id:1, emoji:'🎨', title:'UX Research & Design',   category:'Дизайн',          duration_hours:42, bg_color:'#FDF0EC', is_featured:true  },
  { id:2, emoji:'💻', title:'Python для аналитиков',   category:'Программирование', duration_hours:60, bg_color:'#EAF3EE', is_featured:true  },
  { id:3, emoji:'📊', title:'Digital Marketing Pro',   category:'Маркетинг',       duration_hours:35, bg_color:'#FBF4E8', is_featured:true  },
  { id:4, emoji:'🗣️', title:'Лидерство для женщин',    category:'Мягкие навыки',   duration_hours:18, bg_color:'#F0EBF8', is_featured:false },
  { id:5, emoji:'📈', title:'Финансовая грамотность',  category:'Финансы',         duration_hours:24, bg_color:'#EAF3EE', is_featured:false },
  { id:6, emoji:'🤝', title:'Управление персоналом',   category:'HR',              duration_hours:48, bg_color:'#FDF0EC', is_featured:false },
]
const BIOS = [
  { id:1, emoji:'👩‍💼', name:'Нилуфар Рашидова', role:'CEO · TechUz Solutions',     quote:'"Главное — не бояться начинать. Каждая ошибка — это урок"',       bg_color:'#FDF0EC' },
  { id:2, emoji:'👩‍🔬', name:'Дилрабо Юсупова',  role:'Data Scientist · AI Lab UZ', quote:'"Технологии не имеют пола. Только знания имеют значение"',          bg_color:'#EAF3EE' },
  { id:3, emoji:'👩‍🎨', name:'Камола Азимова',   role:'Creative Director',           quote:'"Творчество открыло мне двери, которые я не могла найти"',          bg_color:'#FBF4E8' },
  { id:4, emoji:'👩‍⚕️', name:'Зулайхо Мирзаева', role:'Chief Medical Officer',       quote:'"Образование — единственное, что нельзя отнять"',                  bg_color:'#F0EBF8' },
  { id:5, emoji:'👩‍💻', name:'Муаззам Хасанова', role:'CTO · Startup Hub',           quote:'"Код не делает различий между мужчинами и женщинами"',              bg_color:'#FDF0EC' },
  { id:6, emoji:'👩‍🏫', name:'Барно Турсунова',  role:'Professor · TUIT',            quote:'"Я учу следующее поколение вдохновлённых женщин"',                  bg_color:'#EAF3EE' },
]
const FILTERS = ['Все','Ташкент','Удалённо','IT','Маркетинг','Дизайн','Финансы']
const NAV = [['home','✦','Главная'],['courses','◈','Курсы'],['biographies','◎','Биографии'],['profile','○','Профиль']]

export default function SeekerDashboard({ onBack }) {
  const [tab,    setTab]    = useState('home')
  const [filter, setFilter] = useState('Все')
  const [profType, setProfType] = useState('open')
  const [jobs,    setJobs]    = useState(JOBS)
  const [courses, setCourses] = useState(COURSES)
  const [bios,    setBios]    = useState(BIOS)

  useEffect(() => {
    api.getCourses().then(d => { if (Array.isArray(d) && d.length) setCourses(d) }).catch(()=>{})
    api.getBiographies().then(d => { if (Array.isArray(d) && d.length) setBios(d) }).catch(()=>{})
  }, [])

  const filteredJobs = filter === 'Все' ? jobs
    : jobs.filter(j =>
        j.work_format === 'remote' && filter === 'Удалённо' ||
        j.city?.includes(filter) ||
        j.category?.includes(filter) ||
        j.required_skills?.some(sk => sk.includes(filter))
      )

  const featuredCourses = courses.filter(c => c.is_featured).slice(0, 3)

  return (
    <div className={s.page}>
      <nav className={s.nav}>
        <div className={s.logo}><span className={s.dot}/>Istiqlol</div>
        <div className={s.navLinks}>
          {NAV.map(([k,,l])=>(
            <span key={k} className={`${s.navLink} ${tab===k?s.active:''}`} onClick={()=>setTab(k)}>{l}</span>
          ))}
        </div>
        <button className={s.backBtn} onClick={onBack}>Выйти</button>
      </nav>

      <div className={s.layout}>
        {/* SIDEBAR */}
        <aside className={s.sidebar}>
          <div className={s.sideUser}>
            <div className={s.ava}>М</div>
            <div><p className={s.uName}>Малика А.</p><span className={s.uRole}>Соискатель</span></div>
          </div>
          <nav className={s.sideNav}>
            {NAV.map(([k,ic,l])=>(
              <div key={k} className={`${s.sItem} ${tab===k?s.sActive:''}`} onClick={()=>setTab(k)}>
                <span>{ic}</span>{l}
              </div>
            ))}
          </nav>
          <div className={s.sideCard}>
            <div className={s.scLabel}>Заполненность профиля</div>
            <div className={s.scBar}><div className={s.scFill} style={{width:'72%'}}/></div>
            <div className={s.scPct}>72%</div>
          </div>
        </aside>

        {/* MAIN CONTENT */}
        <main className={s.main}>

          {/* ══════════ HOME ══════════ */}
          {tab==='home' && <>
            <div className={s.header}>
              <h2 className={s.h2}>Добро пожаловать, Малика 👋</h2>
              <p>AI нашёл для вас {filteredJobs.length} подходящих вакансий сегодня</p>
            </div>

            {/* AI Banner */}
            <div className={s.aiBanner}>
              <div className={s.aiIcon}>🤖</div>
              <div className={s.aiText}>
                <h3>AI-рекомендации обновлены</h3>
                <p>На основе навыков: UX Design, Figma, Prototyping · Ташкент</p>
              </div>
              <div className={s.aiScore}>
                <div className={s.scoreNum}>94%</div>
                <div className={s.scoreLabel}>совпадение</div>
              </div>
            </div>

            {/* ── FEATURED COURSES ON HOME ── */}
            <section className={s.homeSection}>
              <div className={s.sectionHead}>
                <h3 className={s.sectionTitle}>Рекомендуемые курсы</h3>
                <span className={s.seeAll} onClick={()=>setTab('courses')}>Все курсы →</span>
              </div>
              <div className={s.featuredCourses}>
                {featuredCourses.map(c=>(
                  <div key={c.id} className={s.featCard}>
                    <div className={s.featThumb} style={{background:c.bg_color||'#FDF0EC'}}>{c.emoji||'📖'}</div>
                    <div className={s.featBody}>
                      <div className={s.featCat}>{c.category}</div>
                      <div className={s.featTitle}>{c.title}</div>
                      <div className={s.featMeta}>
                        <span>{c.duration_hours} ч.</span>
                        {c.has_certificate!==false && <span className={s.certBadge}>✦ Сертификат</span>}
                      </div>
                      <button className={s.startBtn}>Начать</button>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Filters */}
            <section className={s.homeSection}>
              <div className={s.sectionHead}>
                <h3 className={s.sectionTitle}>Вакансии для вас</h3>
              </div>
              <div className={s.filterRow}>
                {FILTERS.map(f=>(
                  <span key={f} className={`${s.chip} ${filter===f?s.chipOn:''}`} onClick={()=>setFilter(f)}>{f}</span>
                ))}
              </div>
              <div className={s.jobsGrid}>
                {filteredJobs.map(job=>(
                  <div key={job.id} className={s.jobCard}>
                    <div className={s.jobTop}>
                      <div className={s.coLogo}>💼</div>
                      <span className={s.matchBadge}>{job.match}%</span>
                    </div>
                    <div className={s.jobTitle}>{job.title}</div>
                    <div className={s.jobCo}>
                      {job.company}
                      {(job.company_verified||job.verified) && <span className={s.verMark}>✓</span>}
                    </div>
                    <div className={s.tags}>
                      {(job.required_skills||[]).slice(0,3).map(sk=>(
                        <span key={sk} className={s.tag}>{sk}</span>
                      ))}
                    </div>
                    <div className={s.jobFooter}>
                      <span className={s.salary}>{job.salary || `${job.salary_min?.toLocaleString()} ${job.salary_currency}`}</span>
                      <span className={s.loc}>📍 {job.location||job.city}</span>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </>}

          {/* ══════════ COURSES ══════════ */}
          {tab==='courses' && <>
            <div className={s.header}>
              <h2 className={s.h2}>Курсы и обучение</h2>
              <p>Получите сертификаты и улучшите свой профиль</p>
            </div>
            <div className={s.coursesGrid}>
              {courses.map(c=>(
                <div key={c.id} className={s.courseCard}>
                  <div className={s.courseThumb} style={{background:c.bg_color||'#FDF0EC'}}>{c.emoji||'📖'}</div>
                  <div className={s.courseBody}>
                    <div className={s.courseCat}>{c.category}</div>
                    <div className={s.courseTitle}>{c.title}</div>
                    <div className={s.courseMeta}>
                      <span>{c.duration_hours} ч.</span>
                      {c.has_certificate!==false && <span className={s.certBadge}>✦ Сертификат</span>}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>}

          {/* ══════════ BIOGRAPHIES ══════════ */}
          {tab==='biographies' && <>
            <div className={s.header}>
              <h2 className={s.h2}>Истории успеха</h2>
              <p>Вдохновляйтесь историями женщин Узбекистана</p>
            </div>
            <div className={s.bioGrid}>
              {bios.map(b=>(
                <div key={b.id} className={s.bioCard}>
                  <div className={s.bioAva} style={{background:b.bg_color||'#FDF0EC'}}>{b.emoji||'👩'}</div>
                  <div className={s.bioName}>{b.name}</div>
                  <div className={s.bioRole}>{b.role}</div>
                  <div className={s.bioQuote}>{b.quote}</div>
                </div>
              ))}
            </div>
          </>}

          {/* ══════════ PROFILE ══════════ */}
          {tab==='profile' && <>
            <div className={s.header}>
              <h2 className={s.h2}>Мой профиль</h2>
              <p>Управляйте видимостью и информацией</p>
            </div>
            <div className={s.profLayout}>
              <div className={s.profCard}>
                <div className={s.profAva}>М</div>
                <div className={s.profName}>Малика Азимова</div>
                <div className={s.profSub}>UX Designer · Ташкент</div>
                <div className={s.typeToggle}>
                  <button className={`${s.typeBtn} ${profType==='anon'?s.typeBtnOn:''}`} onClick={()=>setProfType('anon')}>Анонимный</button>
                  <button className={`${s.typeBtn} ${profType==='open'?s.typeBtnOn:''}`} onClick={()=>setProfType('open')}>Открытый</button>
                </div>
                <div className={s.typeDesc}>{profType==='open'?'Имя и фото видны работодателям':'Имя и фото скрыты от работодателей'}</div>
                <div className={s.skillsLabel}>Навыки</div>
                <div className={s.skillsWrap}>
                  {['Figma','UX Research','Prototyping','Wireframing','User Testing'].map(sk=>(
                    <span key={sk} className={s.skillPill}>{sk}</span>
                  ))}
                </div>
              </div>
              <div>
                <div className={s.profSection}>
                  <div className={s.secHead}>Опыт <span className={s.editLink}>+ Добавить</span></div>
                  {[['🏢','Lead UX Designer','Click Technologies · 2022–н.в.'],['💡','UI Designer','Freelance · 2020–2022']].map(([ic,t,sub])=>(
                    <div key={t} className={s.expItem}>
                      <div className={s.expIcon}>{ic}</div>
                      <div><div className={s.expTitle}>{t}</div><div className={s.expSub}>{sub}</div></div>
                    </div>
                  ))}
                </div>
                <div className={s.profSection}>
                  <div className={s.secHead}>Образование <span className={s.editLink}>+ Добавить</span></div>
                  <div className={s.expItem}>
                    <div className={s.expIcon}>🎓</div>
                    <div><div className={s.expTitle}>Бакалавр · Информационные технологии</div><div className={s.expSub}>ТАТУ · 2016–2020</div></div>
                  </div>
                </div>
                <div className={s.profSection}>
                  <div className={s.secHead}>Сертификаты <span className={s.editLink}>+ Добавить</span></div>
                  <div className={s.certsRow}>
                    {['Google UX Design','Figma Advanced','Design Thinking'].map(c=>(
                      <span key={c} className={s.certBadge}>✦ {c}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </>}

        </main>
      </div>
    </div>
  )
}
