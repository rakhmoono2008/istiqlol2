"""
Запуск: python seed.py
Заполняет базу начальными данными (курсы, биографии, тестовые вакансии)
"""
import sys
sys.path.append('.')

from app.core.database import SessionLocal
from app.models.base import Course, Biography, Company, Job, User

db = SessionLocal()

# ── Курсы ──
courses = [
    Course(title="UX Research & Design", category="Дизайн", duration_hours=42,
           has_certificate=True, related_skills=["Figma","UX","Wireframing","Prototyping"],
           description="Полный курс по UX-исследованиям и проектированию интерфейсов"),
    Course(title="Python для аналитиков данных", category="Программирование", duration_hours=60,
           has_certificate=True, related_skills=["Python","Pandas","NumPy","SQL"],
           description="От нуля до уверенного анализа данных на Python"),
    Course(title="Digital Marketing Pro", category="Маркетинг", duration_hours=35,
           has_certificate=True, related_skills=["SMM","SEO","Google Ads","Analytics"],
           description="Современный digital-маркетинг: от стратегии до результата"),
    Course(title="Лидерство для женщин", category="Мягкие навыки", duration_hours=18,
           has_certificate=True, related_skills=["Leadership","Communication","Management"],
           description="Развитие лидерских качеств и уверенности в себе"),
    Course(title="Финансовая грамотность", category="Финансы", duration_hours=24,
           has_certificate=True, related_skills=["Finance","Budgeting","Excel"],
           description="Личные финансы, бюджетирование и инвестиции"),
    Course(title="Управление персоналом", category="HR", duration_hours=48,
           has_certificate=True, related_skills=["HR","Recruitment","Management"],
           description="Найм, адаптация и мотивация команды"),
    Course(title="Основы облачных технологий", category="IT", duration_hours=30,
           has_certificate=True, related_skills=["Cloud","AWS","DevOps"],
           description="AWS, Google Cloud и Azure для начинающих"),
    Course(title="Свой бизнес с нуля", category="Предпринимательство", duration_hours=52,
           has_certificate=True, related_skills=["Business","Marketing","Finance"],
           description="От идеи до работающего бизнеса"),
    Course(title="Деловой английский", category="Языки", duration_hours=40,
           has_certificate=True, related_skills=["English","Communication"],
           description="Английский для деловой переписки и переговоров"),
]

# ── Биографии ──
biographies = [
    Biography(name="Нилуфар Рашидова", role="CEO", company="TechUz Solutions",
              quote="Главное — не бояться начинать. Каждая ошибка — это урок",
              story="Нилуфар основала TechUz в 2018 году имея только ноутбук и идею. Сегодня компания насчитывает 200+ сотрудников.",
              is_published=True),
    Biography(name="Дилрабо Юсупова", role="Data Scientist", company="AI Lab UZ",
              quote="Технологии не имеют пола. Только знания имеют значение",
              story="Дилрабо получила степень PhD в области машинного обучения и вернулась в Узбекистан строить AI-будущее.",
              is_published=True),
    Biography(name="Камола Азимова", role="Creative Director", company="Adept Agency",
              quote="Творчество открыло мне двери, которые я не могла найти",
              story="Камола начинала как фрилансер на Fiverr, а сегодня её агентство работает с топ-50 брендами Узбекистана.",
              is_published=True),
    Biography(name="Зулайхо Мирзаева", role="Chief Medical Officer", company="UzMedGroup",
              quote="Образование — единственное, что нельзя отнять",
              story="Зулайхо стала первой женщиной-главврачом в своём регионе после 15 лет упорного труда.",
              is_published=True),
    Biography(name="Муаззам Хасанова", role="CTO", company="Startup Hub Tashkent",
              quote="Код не делает различий между мужчинами и женщинами",
              story="Муаззам изучила программирование самостоятельно по YouTube и стала CTO в 28 лет.",
              is_published=True),
    Biography(name="Барно Турсунова", role="Professor", company="TUIT University",
              quote="Я учу следующее поколение вдохновлённых женщин",
              story="Барно преподаёт Computer Science 12 лет и запустила бесплатные курсы для женщин из регионов.",
              is_published=True),
]

try:
    db.add_all(courses)
    db.add_all(biographies)
    db.commit()
    print(f"✅ Добавлено {len(courses)} курсов и {len(biographies)} биографий")
except Exception as e:
    db.rollback()
    print(f"❌ Ошибка: {e}")
finally:
    db.close()
