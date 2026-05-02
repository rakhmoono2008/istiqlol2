"""Run once to populate DB with demo data: python -m app.api.seed"""
from app.core.database import SessionLocal, engine, Base
import app.models.base  # register models
from app.models.base import User, Profile, Company, Job, Course, Biography

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Company
if not db.query(Company).first():
    u = User(one_id_sub="employer_demo", role="employer"); db.add(u); db.flush()
    c = Company(user_id=u.id, name="Click Technologies", description="Ведущая IT-компания Узбекистана",
                phone="+998 71 200-00-00", address="Ташкент, ул. Навои 38", verified=True)
    db.add(c); db.flush()
    for j in [
        Job(company_id=c.id, title="UX/UI Дизайнер", category="IT", work_format="office",
            salary_min=5000000, salary_max=8000000, city="Ташкент",
            required_skills=["Figma","UX Research","Prototyping","Wireframing"],
            description="Ищем опытного UX/UI дизайнера для работы над мобильными приложениями."),
        Job(company_id=c.id, title="Frontend Developer", category="IT", work_format="remote",
            salary_min=1200, salary_max=2000, salary_currency="USD", city="Ташкент",
            required_skills=["React","TypeScript","CSS","Figma"],
            description="Разработка интерфейсов на React."),
        Job(company_id=c.id, title="Marketing Manager", category="Маркетинг", work_format="hybrid",
            salary_min=4000000, salary_max=6000000, city="Ташкент",
            required_skills=["Digital Marketing","SMM","Analytics","Copywriting"],
            description="Управление digital-маркетингом компании."),
        Job(company_id=c.id, title="Brand Designer", category="IT", work_format="office",
            salary_min=6000000, salary_max=9000000, city="Самарканд",
            required_skills=["Branding","Illustrator","Photoshop","InDesign"],
            description="Создание и развитие бренда компании."),
    ]:
        db.add(j)

# Courses
if not db.query(Course).first():
    for course in [
        Course(title="UX Research & Design",        category="Дизайн",          duration_hours=42, emoji="🎨", bg_color="#FDF0EC", is_featured=True,  related_skills=["Figma","UX Research","Prototyping"]),
        Course(title="Python для аналитиков",        category="Программирование", duration_hours=60, emoji="💻", bg_color="#EAF3EE", is_featured=True,  related_skills=["Python","Data Analysis","SQL"]),
        Course(title="Digital Marketing Pro",         category="Маркетинг",       duration_hours=35, emoji="📊", bg_color="#FBF4E8", is_featured=True,  related_skills=["Digital Marketing","SMM","Analytics"]),
        Course(title="Лидерство для женщин",          category="Мягкие навыки",   duration_hours=18, emoji="🗣️", bg_color="#F0EBF8", is_featured=False, related_skills=["Leadership","Management","Communication"]),
        Course(title="Финансовая грамотность",        category="Финансы",         duration_hours=24, emoji="📈", bg_color="#EAF3EE", is_featured=False, related_skills=["Finance","Accounting","Excel"]),
        Course(title="Управление персоналом",         category="HR",              duration_hours=48, emoji="🤝", bg_color="#FDF0EC", is_featured=False, related_skills=["HR","Recruitment","Management"]),
        Course(title="Figma Advanced",                category="Дизайн",          duration_hours=20, emoji="✏️", bg_color="#FDF0EC", is_featured=False, related_skills=["Figma","UI Design","Prototyping"]),
        Course(title="Excel & Google Sheets",         category="Офис",            duration_hours=16, emoji="📋", bg_color="#EAF3EE", is_featured=False, related_skills=["Excel","Data Analysis"]),
    ]:
        db.add(course)

# Biographies
if not db.query(Biography).first():
    for b in [
        Biography(name="Нилуфар Рашидова", role="CEO", company="TechUz Solutions",
            quote="Главное — не бояться начинать. Каждая ошибка — это урок",
            story="Нилуфар основала TechUz в 2018 году имея только ноутбук и идею.", emoji="👩‍💼", bg_color="#FDF0EC"),
        Biography(name="Дилрабо Юсупова", role="Data Scientist", company="AI Lab UZ",
            quote="Технологии не имеют пола. Только знания имеют значение",
            story="После курса Python стала ведущим data scientist.", emoji="👩‍🔬", bg_color="#EAF3EE"),
        Biography(name="Камола Азимова", role="Creative Director", company="Adept Agency",
            quote="Творчество открыло мне двери, которые я не могла найти",
            story="Начинала с бесплатных курсов дизайна, сейчас руководит командой 30 человек.", emoji="👩‍🎨", bg_color="#FBF4E8"),
    ]:
        db.add(b)

db.commit()
db.close()
print("✅ Seed data inserted!")
