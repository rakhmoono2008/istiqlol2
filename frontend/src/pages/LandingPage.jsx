import { useEffect, useState } from 'react'
import s from './Landing.module.css'

export default function LandingPage({ onSelect }) {
  const [visible, setVisible] = useState(false)
  useEffect(() => { setTimeout(() => setVisible(true), 60) }, [])

  return (
    <div className={s.page}>
      <nav className={s.nav}>
        <div className={s.logo}><span className={s.dot} />Istiqlol</div>
        <button className={s.loginBtn} onClick={() => onSelect('seeker')}>One ID →</button>
      </nav>

      <section className={`${s.hero} ${visible ? s.visible : ''}`}>
        <div className={s.badge}>✦ Только для женщин Узбекистана</div>
        <h1 className={s.h1}>Карьера, которую<br />заслуживаете <em>вы</em></h1>
        <p className={s.sub}>Умные AI-рекомендации, государственная верификация<br />и сообщество поддержки для каждой женщины</p>

        <div className={s.cards}>
          <div className={`${s.card} ${s.seeker}`} onClick={() => onSelect('seeker')}>
            <div className={s.cardIcon}>👩</div>
            <h3>Я ищу работу</h3>
            <p>AI подберёт вакансии по навыкам и опыту</p>
            <span className={s.arrow}>→</span>
          </div>
          <div className={`${s.card} ${s.employer}`} onClick={() => onSelect('employer')}>
            <div className={`${s.cardIcon} ${s.iconGreen}`}>🏢</div>
            <h3>Я работодатель</h3>
            <p>Разместите вакансию и найдите специалистов</p>
            <span className={`${s.arrow} ${s.arrowGreen}`}>→</span>
          </div>
        </div>
      </section>

      <div className={s.stats}>
        {[['12 400+','активных вакансий'],['8 200','соискателей'],['940','компаний'],['95%','успешных откликов']].map(([n,l])=>(
          <div key={l} className={s.stat}>
            <div className={s.statNum}>{n}</div>
            <div className={s.statLabel}>{l}</div>
          </div>
        ))}
      </div>

      <section className={s.features}>
        {[
          ['🤖','AI-рекомендации','Cosine Similarity подбирает вакансии точно под ваши навыки и геолокацию'],
          ['🔒','Анонимный профиль','Скройте имя и фото — работодатель видит только опыт и навыки'],
          ['✓','Верификация компаний','Синяя галочка подтверждает надёжность работодателя через One ID'],
          ['📜','Сертификаты','Пройдите курсы и получите сертификаты, которые видны в профиле'],
        ].map(([ic,title,desc])=>(
          <div key={title} className={s.feature}>
            <div className={s.featureIcon}>{ic}</div>
            <h4>{title}</h4>
            <p>{desc}</p>
          </div>
        ))}
      </section>
    </div>
  )
}
