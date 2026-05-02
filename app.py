from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'istiqlol_secret_key_2026')
app.config['REMEMBER_COOKIE_DURATION'] = 60 * 60 * 24 * 30
app.config['PERMANENT_SESSION_LIFETIME'] = 60 * 60 * 24 * 30
app.config['SESSION_PERMANENT'] = True

database_url = os.environ.get('DATABASE_URL')
if database_url:
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+pg8000://', 1)
    elif database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+pg8000://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(os.path.join(basedir, 'database'), exist_ok=True)
    db_path = os.path.join(basedir, 'database', 'database.db').replace('\\', '/')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True, 'pool_recycle': 300}

if os.environ.get('RAILWAY_ENVIRONMENT'):
    upload_folder = '/app/uploads'
    backup_folder = '/app/backups'
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    upload_folder = os.path.join(basedir, 'uploads')
    backup_folder = os.path.join(basedir, 'backups')

os.makedirs(upload_folder, exist_ok=True)
os.makedirs(backup_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['BACKUP_FOLDER'] = backup_folder
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'

# ===== МОДЕЛИ =====

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(150))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), default='seeker')  # seeker, employer, admin
    city = db.Column(db.String(100))
    profession = db.Column(db.String(200))
    profile_type = db.Column(db.String(20), default='open')  # open, anon
    skills = db.Column(db.Text)  # JSON list
    bio = db.Column(db.Text)
    photo = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_employer(self):
        return self.role == 'employer'

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_skills(self):
        if self.skills:
            try:
                return json.loads(self.skills)
            except:
                return []
        return []

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    city = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='company')

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    salary_from = db.Column(db.String(100))
    salary_to = db.Column(db.String(100))
    format = db.Column(db.String(50))  # Офис, Удалённо, Гибрид
    city = db.Column(db.String(100))
    skills_required = db.Column(db.Text)  # JSON list
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    company = db.relationship('Company', backref='jobs')

    def get_skills(self):
        if self.skills_required:
            try:
                return json.loads(self.skills_required)
            except:
                return []
        return []

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cover_letter = db.Column(db.Text)
    status = db.Column(db.String(30), default='pending')  # pending, viewed, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    job = db.relationship('Job', backref='applications')
    user = db.relationship('User', backref='applications')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    hours = db.Column(db.Integer)
    level = db.Column(db.String(50))  # Начальный, Средний, Продвинутый
    has_certificate = db.Column(db.Boolean, default=True)
    emoji = db.Column(db.String(10), default='📚')
    bg_color = db.Column(db.String(20), default='#FDF0EC')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CourseEnrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    progress = db.Column(db.Integer, default=0)  # 0-100
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    course = db.relationship('Course', backref='enrollments')
    user = db.relationship('User', backref='enrollments')

class Biography(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200))
    company = db.Column(db.String(200))
    quote = db.Column(db.Text)
    emoji = db.Column(db.String(10), default='👩‍💼')
    bg_color = db.Column(db.String(20), default='#FDF0EC')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    issuer = db.Column(db.String(200))
    filename = db.Column(db.String(300))
    issued_date = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='certificates')

class VerificationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    company = db.relationship('Company', backref='verification_requests')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ===== HELPERS =====

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Доступ запрещён. Требуются права администратора.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def backup_to_json():
    try:
        bf = app.config['BACKUP_FOLDER']

        # Пользователи
        users_data = [{'id': u.id, 'username': u.username, 'full_name': u.full_name,
                        'email': u.email, 'password_hash': u.password_hash, 'role': u.role,
                        'city': u.city, 'profession': u.profession, 'profile_type': u.profile_type,
                        'skills': u.skills, 'bio': u.bio, 'photo': u.photo,
                        'created_at': u.created_at.isoformat() if u.created_at else None}
                       for u in User.query.all()]
        with open(os.path.join(bf, 'users.json'), 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)

        # Компании
        companies_data = [{'id': c.id, 'user_id': c.user_id, 'name': c.name,
                            'description': c.description, 'city': c.city,
                            'industry': c.industry, 'verified': c.verified,
                            'created_at': c.created_at.isoformat() if c.created_at else None}
                           for c in Company.query.all()]
        with open(os.path.join(bf, 'companies.json'), 'w', encoding='utf-8') as f:
            json.dump(companies_data, f, ensure_ascii=False, indent=2)

        # Вакансии
        jobs_data = [{'id': j.id, 'company_id': j.company_id, 'title': j.title,
                       'category': j.category, 'description': j.description,
                       'salary_from': j.salary_from, 'format': j.format, 'city': j.city,
                       'skills_required': j.skills_required, 'is_active': j.is_active,
                       'created_at': j.created_at.isoformat() if j.created_at else None}
                      for j in Job.query.all()]
        with open(os.path.join(bf, 'jobs.json'), 'w', encoding='utf-8') as f:
            json.dump(jobs_data, f, ensure_ascii=False, indent=2)

        # Отклики
        apps_data = [{'id': a.id, 'job_id': a.job_id, 'user_id': a.user_id,
                       'cover_letter': a.cover_letter, 'status': a.status,
                       'created_at': a.created_at.isoformat() if a.created_at else None}
                      for a in Application.query.all()]
        with open(os.path.join(bf, 'applications.json'), 'w', encoding='utf-8') as f:
            json.dump(apps_data, f, ensure_ascii=False, indent=2)

        # Курсы
        courses_data = [{'id': c.id, 'title': c.title, 'category': c.category,
                          'description': c.description, 'hours': c.hours, 'level': c.level,
                          'has_certificate': c.has_certificate, 'emoji': c.emoji,
                          'bg_color': c.bg_color}
                         for c in Course.query.all()]
        with open(os.path.join(bf, 'courses.json'), 'w', encoding='utf-8') as f:
            json.dump(courses_data, f, ensure_ascii=False, indent=2)

        # Записи на курсы
        enrollments_data = [{'id': e.id, 'course_id': e.course_id, 'user_id': e.user_id,
                               'progress': e.progress,
                               'enrolled_at': e.enrolled_at.isoformat() if e.enrolled_at else None}
                              for e in CourseEnrollment.query.all()]
        with open(os.path.join(bf, 'enrollments.json'), 'w', encoding='utf-8') as f:
            json.dump(enrollments_data, f, ensure_ascii=False, indent=2)

        # Биографии
        bios_data = [{'id': b.id, 'name': b.name, 'role': b.role, 'company': b.company,
                       'quote': b.quote, 'emoji': b.emoji, 'bg_color': b.bg_color}
                      for b in Biography.query.all()]
        with open(os.path.join(bf, 'biographies.json'), 'w', encoding='utf-8') as f:
            json.dump(bios_data, f, ensure_ascii=False, indent=2)

        print("✅ Полный бэкап создан!")
    except Exception as e:
        print(f"❌ Ошибка бэкапа: {e}")


def restore_from_json():
    try:
        bf = app.config['BACKUP_FOLDER']

        # Пользователи
        uf = os.path.join(bf, 'users.json')
        if os.path.exists(uf):
            with open(uf, 'r', encoding='utf-8') as f:
                for ud in json.load(f):
                    if not User.query.filter_by(username=ud['username']).first():
                        u = User(username=ud['username'], full_name=ud.get('full_name'),
                                 email=ud.get('email'), password_hash=ud['password_hash'],
                                 role=ud['role'], city=ud.get('city'),
                                 profession=ud.get('profession'),
                                 profile_type=ud.get('profile_type', 'open'),
                                 skills=ud.get('skills'), bio=ud.get('bio'))
                        if ud.get('created_at'):
                            u.created_at = datetime.fromisoformat(ud['created_at'])
                        db.session.add(u)
            db.session.commit()
            print("✅ Пользователи восстановлены")

        # Компании
        cf = os.path.join(bf, 'companies.json')
        if os.path.exists(cf):
            with open(cf, 'r', encoding='utf-8') as f:
                for cd in json.load(f):
                    if not Company.query.filter_by(name=cd['name']).first():
                        user = User.query.filter_by(id=cd['user_id']).first()
                        if user:
                            c = Company(user_id=user.id, name=cd['name'],
                                        description=cd.get('description'),
                                        city=cd.get('city'), industry=cd.get('industry'),
                                        verified=cd.get('verified', False))
                            if cd.get('created_at'):
                                c.created_at = datetime.fromisoformat(cd['created_at'])
                            db.session.add(c)
            db.session.commit()
            print("✅ Компании восстановлены")

        # Вакансии
        jf = os.path.join(bf, 'jobs.json')
        if os.path.exists(jf):
            with open(jf, 'r', encoding='utf-8') as f:
                for jd in json.load(f):
                    company = Company.query.filter_by(id=jd['company_id']).first()
                    if company and not Job.query.filter_by(title=jd['title'], company_id=company.id).first():
                        j = Job(company_id=company.id, title=jd['title'],
                                category=jd.get('category'), description=jd.get('description'),
                                salary_from=jd.get('salary_from'), format=jd.get('format'),
                                city=jd.get('city'), skills_required=jd.get('skills_required'),
                                is_active=jd.get('is_active', True))
                        if jd.get('created_at'):
                            j.created_at = datetime.fromisoformat(jd['created_at'])
                        db.session.add(j)
            db.session.commit()
            print("✅ Вакансии восстановлены")

        # Курсы
        coursesf = os.path.join(bf, 'courses.json')
        if os.path.exists(coursesf):
            with open(coursesf, 'r', encoding='utf-8') as f:
                for cd in json.load(f):
                    if not Course.query.filter_by(title=cd['title']).first():
                        c = Course(title=cd['title'], category=cd.get('category'),
                                   description=cd.get('description'), hours=cd.get('hours'),
                                   level=cd.get('level'), has_certificate=cd.get('has_certificate', True),
                                   emoji=cd.get('emoji', '📚'), bg_color=cd.get('bg_color', '#FDF0EC'))
                        db.session.add(c)
            db.session.commit()
            print("✅ Курсы восстановлены")

        # Биографии
        biof = os.path.join(bf, 'biographies.json')
        if os.path.exists(biof):
            with open(biof, 'r', encoding='utf-8') as f:
                for bd in json.load(f):
                    if not Biography.query.filter_by(name=bd['name']).first():
                        b = Biography(name=bd['name'], role=bd.get('role'),
                                      company=bd.get('company'), quote=bd.get('quote'),
                                      emoji=bd.get('emoji', '👩‍💼'),
                                      bg_color=bd.get('bg_color', '#FDF0EC'))
                        db.session.add(b)
            db.session.commit()
            print("✅ Биографии восстановлены")

        # Отклики
        appf = os.path.join(bf, 'applications.json')
        if os.path.exists(appf):
            with open(appf, 'r', encoding='utf-8') as f:
                for ad in json.load(f):
                    if not Application.query.filter_by(job_id=ad['job_id'], user_id=ad['user_id']).first():
                        job = Job.query.filter_by(id=ad['job_id']).first()
                        user = User.query.filter_by(id=ad['user_id']).first()
                        if job and user:
                            a = Application(job_id=job.id, user_id=user.id,
                                            cover_letter=ad.get('cover_letter'),
                                            status=ad.get('status', 'pending'))
                            if ad.get('created_at'):
                                a.created_at = datetime.fromisoformat(ad['created_at'])
                            db.session.add(a)
            db.session.commit()
            print("✅ Отклики восстановлены")

        # Записи на курсы
        enrf = os.path.join(bf, 'enrollments.json')
        if os.path.exists(enrf):
            with open(enrf, 'r', encoding='utf-8') as f:
                for ed in json.load(f):
                    if not CourseEnrollment.query.filter_by(course_id=ed['course_id'], user_id=ed['user_id']).first():
                        course = Course.query.filter_by(id=ed['course_id']).first()
                        user = User.query.filter_by(id=ed['user_id']).first()
                        if course and user:
                            e = CourseEnrollment(course_id=course.id, user_id=user.id,
                                                 progress=ed.get('progress', 0))
                            db.session.add(e)
            db.session.commit()
            print("✅ Записи на курсы восстановлены")

    except Exception as e:
        print(f"❌ Ошибка восстановления: {e}")

# ===== МАРШРУТЫ =====

@app.route('/')
def index():
    jobs_count = Job.query.filter_by(is_active=True).count()
    seekers_count = User.query.filter_by(role='seeker').count()
    companies_count = Company.query.filter_by(verified=True).count()
    courses_count = Course.query.count()
    return render_template('index.html',
                           jobs_count=jobs_count,
                           seekers_count=seekers_count,
                           companies_count=companies_count,
                           courses_count=courses_count)

# --- Авторизация ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Добро пожаловать, {user.full_name or user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard'))
        flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'seeker')

        if not username or not password:
            flash('Заполните все поля', 'danger')
            return render_template('register.html')
        if password != confirm_password:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('Такое имя пользователя уже существует', 'danger')
            return render_template('register.html')

        user = User(username=username, full_name=full_name, email=email,
                    password_hash=generate_password_hash(password), role=role)
        db.session.add(user)
        db.session.flush()

        if role == 'employer':
            company_name = request.form.get('company_name', '').strip() or full_name
            company = Company(user_id=user.id, name=company_name,
                              city=request.form.get('city', ''))
            db.session.add(company)

        db.session.commit()
        backup_to_json()
        login_user(user, remember=True)
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# --- Дашборд ---
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'employer':
        return redirect(url_for('employer_dashboard'))
    if current_user.role == 'admin':
        return redirect(url_for('admin_panel'))

    # Соискатель
    all_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    courses = Course.query.all()
    biographies = Biography.query.all()

    user_skills = current_user.get_skills()
    my_applications = Application.query.filter_by(user_id=current_user.id).all()
    applied_job_ids = {a.job_id for a in my_applications}

    enrollments = {e.course_id: e.progress for e in
                   CourseEnrollment.query.filter_by(user_id=current_user.id).all()}

    return render_template('seeker_dashboard.html',
                           jobs=all_jobs,
                           courses=courses,
                           biographies=biographies,
                           user_skills=user_skills,
                           applied_job_ids=applied_job_ids,
                           enrollments=enrollments,
                           now=datetime.utcnow())

# --- Вакансии ---
@app.route('/jobs')
def jobs():
    category = request.args.get('category')
    format_ = request.args.get('format')
    city = request.args.get('city')
    query = Job.query.filter_by(is_active=True)
    if category:
        query = query.filter_by(category=category)
    if format_:
        query = query.filter_by(format=format_)
    if city:
        query = query.filter_by(city=city)
    jobs = query.order_by(Job.created_at.desc()).all()
    categories = [c[0] for c in db.session.query(Job.category).distinct().all() if c[0]]
    return render_template('jobs.html', jobs=jobs, categories=categories,
                           current_category=category, now=datetime.utcnow())

@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    applied = False
    if current_user.is_authenticated:
        applied = Application.query.filter_by(job_id=job_id, user_id=current_user.id).first() is not None
    return render_template('job_detail.html', job=job, applied=applied)

@app.route('/jobs/<int:job_id>/apply', methods=['POST'])
@login_required
def apply_job(job_id):
    if current_user.role != 'seeker':
        flash('Только соискатели могут откликаться на вакансии', 'danger')
        return redirect(url_for('job_detail', job_id=job_id))
    if Application.query.filter_by(job_id=job_id, user_id=current_user.id).first():
        flash('Вы уже откликались на эту вакансию', 'warning')
        return redirect(url_for('job_detail', job_id=job_id))
    app_obj = Application(job_id=job_id, user_id=current_user.id,
                          cover_letter=request.form.get('cover_letter', ''))
    db.session.add(app_obj)
    db.session.commit()
    flash('✅ Отклик отправлен!', 'success')
    return redirect(url_for('job_detail', job_id=job_id))

# --- Курсы ---
@app.route('/courses')
def courses():
    category = request.args.get('category')
    query = Course.query
    if category:
        query = query.filter_by(category=category)
    courses = query.all()
    categories = [c[0] for c in db.session.query(Course.category).distinct().all() if c[0]]
    enrollments = {}
    if current_user.is_authenticated:
        enrollments = {e.course_id: e.progress for e in
                       CourseEnrollment.query.filter_by(user_id=current_user.id).all()}
    return render_template('courses.html', courses=courses, categories=categories,
                           current_category=category, enrollments=enrollments)

@app.route('/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll_course(course_id):
    course = Course.query.get_or_404(course_id)
    existing = CourseEnrollment.query.filter_by(course_id=course_id, user_id=current_user.id).first()
    if existing:
        flash('Вы уже записаны на этот курс', 'info')
    else:
        enrollment = CourseEnrollment(course_id=course_id, user_id=current_user.id)
        db.session.add(enrollment)
        db.session.commit()
        flash(f'✅ Вы записались на курс «{course.title}»!', 'success')
    return redirect(url_for('courses'))

# --- Биографии ---
@app.route('/biographies')
def biographies():
    bios = Biography.query.all()
    return render_template('biographies.html', biographies=bios)

# --- Профиль ---
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    current_user.full_name = request.form.get('full_name', '').strip()
    current_user.city = request.form.get('city', '').strip()
    current_user.profession = request.form.get('profession', '').strip()
    current_user.bio = request.form.get('bio', '').strip()
    current_user.profile_type = request.form.get('profile_type', 'open')
    skills_raw = request.form.get('skills', '')
    skills_list = [s.strip() for s in skills_raw.split(',') if s.strip()]
    current_user.skills = json.dumps(skills_list, ensure_ascii=False)
    db.session.commit()
    flash('Профиль обновлён', 'success')
    return redirect(url_for('profile'))

# --- Работодатель ---
@app.route('/employer')
@login_required
def employer_dashboard():
    if current_user.role not in ('employer', 'admin'):
        flash('Доступ только для работодателей', 'danger')
        return redirect(url_for('index'))
    company = Company.query.filter_by(user_id=current_user.id).first()
    if not company:
        company = Company(user_id=current_user.id,
                          name=current_user.full_name or current_user.username)
        db.session.add(company)
        db.session.commit()
    jobs = Job.query.filter_by(company_id=company.id).order_by(Job.created_at.desc()).all()
    total_apps = sum(len(j.applications) for j in jobs)
    active_jobs = sum(1 for j in jobs if j.is_active)
    return render_template('employer_dashboard.html', company=company,
                           jobs=jobs, total_apps=total_apps, active_jobs=active_jobs)

@app.route('/employer/post', methods=['POST'])
@login_required
def post_job():
    if current_user.role not in ('employer', 'admin'):
        flash('Доступ только для работодателей', 'danger')
        return redirect(url_for('index'))
    company = Company.query.filter_by(user_id=current_user.id).first()
    if not company:
        flash('Сначала создайте профиль компании', 'danger')
        return redirect(url_for('employer_dashboard'))
    skills_raw = request.form.get('skills', '')
    skills_list = [s.strip() for s in skills_raw.split(',') if s.strip()]
    job = Job(
        company_id=company.id,
        title=request.form.get('title', '').strip(),
        category=request.form.get('category', ''),
        description=request.form.get('description', ''),
        salary_from=request.form.get('salary_from', ''),
        format=request.form.get('format', 'Офис'),
        city=company.city or '',
        skills_required=json.dumps(skills_list, ensure_ascii=False)
    )
    db.session.add(job)
    db.session.commit()
    flash('✅ Вакансия опубликована!', 'success')
    return redirect(url_for('employer_dashboard'))

@app.route('/employer/job/<int:job_id>/toggle', methods=['POST'])
@login_required
def toggle_job(job_id):
    job = Job.query.get_or_404(job_id)
    company = Company.query.filter_by(user_id=current_user.id).first()
    if not company or job.company_id != company.id:
        flash('Нет прав', 'danger')
        return redirect(url_for('employer_dashboard'))
    job.is_active = not job.is_active
    db.session.commit()
    flash('Статус вакансии изменён', 'success')
    return redirect(url_for('employer_dashboard'))

@app.route('/employer/job/<int:job_id>/applications')
@login_required
def job_applications(job_id):
    job = Job.query.get_or_404(job_id)
    company = Company.query.filter_by(user_id=current_user.id).first()
    if not company or job.company_id != company.id:
        flash('Нет прав', 'danger')
        return redirect(url_for('employer_dashboard'))
    return render_template('job_applications.html', job=job)

# --- Чат ---
@app.route('/chat')
@login_required
def chat_list():
    users = User.query.filter(User.id != current_user.id).order_by(User.username).all()
    conversations = []
    for user in users:
        last_msg = Message.query.filter(
            ((Message.sender_id == current_user.id) & (Message.receiver_id == user.id)) |
            ((Message.sender_id == user.id) & (Message.receiver_id == current_user.id))
        ).order_by(Message.created_at.desc()).first()
        unread = Message.query.filter_by(
            sender_id=user.id, receiver_id=current_user.id, is_read=False).count()
        if last_msg:
            conversations.append({'user': user, 'last_msg': last_msg, 'unread': unread})
    conversations.sort(key=lambda x: x['last_msg'].created_at, reverse=True)
    return render_template('chat_list.html', conversations=conversations)

@app.route('/chat/<int:user_id>')
@login_required
def chat_room(user_id):
    other_user = User.query.get_or_404(user_id)
    Message.query.filter_by(
        sender_id=user_id, receiver_id=current_user.id, is_read=False
    ).update({'is_read': True})
    db.session.commit()
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()
    return render_template('chat_room.html', other_user=other_user, messages=messages)

@app.route('/chat/send', methods=['POST'])
@login_required
def chat_send():
    data = request.get_json()
    receiver_id = data.get('receiver_id')
    content = data.get('content', '').strip()
    if not content or not receiver_id:
        return jsonify({'error': 'invalid'}), 400
    msg = Message(sender_id=current_user.id, receiver_id=receiver_id, content=content)
    db.session.add(msg)
    db.session.commit()
    return jsonify({'id': msg.id, 'content': msg.content,
                    'sender_id': current_user.id,
                    'sender_name': current_user.full_name or current_user.username,
                    'created_at': msg.created_at.strftime('%H:%M')})

@app.route('/chat/poll/<int:user_id>')
@login_required
def chat_poll(user_id):
    after_id = request.args.get('after', 0, type=int)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id)),
        Message.id > after_id
    ).order_by(Message.created_at.asc()).all()
    Message.query.filter_by(sender_id=user_id, receiver_id=current_user.id,
                             is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify([{'id': m.id, 'content': m.content,
                     'sender_id': m.sender_id,
                     'created_at': m.created_at.strftime('%H:%M')} for m in messages])

@app.route('/chat/unread_count')
@login_required
def unread_count():
    count = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    return jsonify({'count': count})


# --- Фото профиля ---
@app.route('/profile/upload_photo', methods=['POST'])
@login_required
def upload_photo():
    if 'photo' not in request.files:
        flash('Файл не выбран', 'danger')
        return redirect(url_for('profile'))
    file = request.files['photo']
    if file.filename == '':
        flash('Файл не выбран', 'danger')
        return redirect(url_for('profile'))
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in {'png', 'jpg', 'jpeg', 'gif', 'webp'}:
        flash('Только изображения (jpg, png, gif)', 'danger')
        return redirect(url_for('profile'))
    filename = f"photo_{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if current_user.photo:
        old_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.photo)
        if os.path.exists(old_path):
            os.remove(old_path)
    current_user.photo = filename
    db.session.commit()
    backup_to_json()
    flash('✅ Фото профиля обновлено!', 'success')
    return redirect(url_for('profile'))

# --- Сертификаты ---
@app.route('/profile/add_certificate', methods=['POST'])
@login_required
def add_certificate():
    title = request.form.get('cert_title', '').strip()
    issuer = request.form.get('cert_issuer', '').strip()
    issued_date = request.form.get('cert_date', '').strip()
    if not title:
        flash('Укажите название сертификата', 'danger')
        return redirect(url_for('profile'))
    filename = None
    if 'cert_file' in request.files:
        file = request.files['cert_file']
        if file and file.filename:
            ext = file.filename.rsplit('.', 1)[-1].lower()
            if ext in {'pdf', 'png', 'jpg', 'jpeg'}:
                filename = f"cert_{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    cert = Certificate(user_id=current_user.id, title=title,
                       issuer=issuer, filename=filename, issued_date=issued_date)
    db.session.add(cert)
    db.session.commit()
    backup_to_json()
    flash('✅ Сертификат добавлен!', 'success')
    return redirect(url_for('profile'))

@app.route('/profile/delete_certificate/<int:cert_id>', methods=['POST'])
@login_required
def delete_certificate(cert_id):
    cert = Certificate.query.get_or_404(cert_id)
    if cert.user_id != current_user.id:
        flash('Нет прав', 'danger')
        return redirect(url_for('profile'))
    if cert.filename:
        path = os.path.join(app.config['UPLOAD_FOLDER'], cert.filename)
        if os.path.exists(path):
            os.remove(path)
    db.session.delete(cert)
    db.session.commit()
    flash('Сертификат удалён', 'success')
    return redirect(url_for('profile'))

# --- Верификация работодателя ---
@app.route('/employer/request_verification', methods=['POST'])
@login_required
def request_verification():
    if current_user.role != 'employer':
        flash('Только для работодателей', 'danger')
        return redirect(url_for('index'))
    company = Company.query.filter_by(user_id=current_user.id).first()
    if not company:
        flash('Компания не найдена', 'danger')
        return redirect(url_for('employer_dashboard'))
    existing = VerificationRequest.query.filter_by(company_id=company.id, status='pending').first()
    if existing:
        flash('Заявка уже отправлена, ожидайте', 'warning')
        return redirect(url_for('employer_dashboard'))
    vr = VerificationRequest(company_id=company.id)
    db.session.add(vr)
    db.session.commit()
    flash('✅ Заявка на верификацию отправлена!', 'success')
    return redirect(url_for('employer_dashboard'))

@app.route('/admin/verify_company/<int:company_id>', methods=['POST'])
@login_required
@admin_required
def verify_company(company_id):
    company = Company.query.get_or_404(company_id)
    action = request.form.get('action', 'approve')
    company.verified = (action == 'approve')
    vr = VerificationRequest.query.filter_by(company_id=company_id, status='pending').first()
    if vr:
        vr.status = 'approved' if action == 'approve' else 'rejected'
        vr.comment = request.form.get('comment', '')
    db.session.commit()
    msg = 'верифицирована' if action == 'approve' else 'отклонена'
    flash(f'Компания {company.name} {msg}', 'success')
    return redirect(url_for('admin_panel'))

# --- AI матчинг вакансий ---
@app.route('/api/ai_match')
@login_required
def ai_match():
    import urllib.request
    import urllib.error
    import json as _json

    if current_user.role != 'seeker':
        return jsonify({'error': 'only for seekers'}), 403

    jobs = Job.query.filter_by(is_active=True).all()
    user_skills = current_user.get_skills()
    user_skills_set = set(s.lower() for s in user_skills)

    api_key = os.environ.get('GEMINI_API_KEY', '')
    if api_key:
        jobs_text = '\n'.join([
            f"ID:{j.id}|{j.title}|skills:{','.join(j.get_skills())}|format:{j.format}|cat:{j.category or ''}"
            for j in jobs[:20]
        ])
        prompt = (
            f"Job matching assistant for women in Uzbekistan.\n"
            f"Candidate: profession={current_user.profession or ''}, "
            f"skills={','.join(user_skills)}, bio={current_user.bio or ''}\n"
            f"Jobs:\n{jobs_text}\n"
            f"Return ONLY a JSON array sorted by score desc: "
            f'[{{"job_id": N, "score": 0-100, "reason": "short reason in Russian"}}]\n'
            f"No explanation, only JSON."
        )
        try:
            url = (
                'https://generativelanguage.googleapis.com/v1beta/models/'
                f'gemini-1.5-flash-latest:generateContent?key={api_key}'
            )
            body = _json.dumps({'contents': [{'parts': [{'text': prompt}]}]}).encode()
            req = urllib.request.Request(
                url, data=body, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = _json.loads(resp.read())
            text = data['candidates'][0]['content']['parts'][0]['text']
            text = text.strip().lstrip('```json').lstrip('```').rstrip('```').strip()
            results = _json.loads(text)
            return jsonify(results)
        except Exception as e:
            print(f'Gemini error: {e}')

    # Fallback — keyword matching
    results = []
    for job in jobs:
        job_skills = set(s.lower() for s in job.get_skills())
        if user_skills_set and job_skills:
            common = len(user_skills_set & job_skills)
            score = min(95, int((common / max(len(job_skills), 1)) * 100) + 25)
        else:
            score = 40
        results.append({'job_id': job.id, 'score': score, 'reason': ''})
    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(results[:10])

# --- Админ-панель ---
@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    stats = {
        'users': User.query.count(),
        'jobs': Job.query.count(),
        'courses': Course.query.count(),
        'companies': Company.query.count(),
        'user_list': User.query.order_by(User.created_at.desc()).all()
    }
    return render_template('admin.html', stats=stats)

@app.route('/admin/biographies/add', methods=['POST'])
@login_required
@admin_required
def add_biography():
    bio = Biography(
        name=request.form.get('name', ''),
        role=request.form.get('role', ''),
        company=request.form.get('company', ''),
        quote=request.form.get('quote', ''),
        emoji=request.form.get('emoji', '👩‍💼'),
        bg_color=request.form.get('bg_color', '#FDF0EC')
    )
    db.session.add(bio)
    db.session.commit()
    flash('Биография добавлена', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/courses/add', methods=['POST'])
@login_required
@admin_required
def add_course():
    course = Course(
        title=request.form.get('title', ''),
        category=request.form.get('category', ''),
        description=request.form.get('description', ''),
        hours=request.form.get('hours', 0, type=int),
        level=request.form.get('level', 'Начальный'),
        emoji=request.form.get('emoji', '📚'),
        bg_color=request.form.get('bg_color', '#FDF0EC')
    )
    db.session.add(course)
    db.session.commit()
    flash('Курс добавлен', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/users/<int:user_id>/toggle_role', methods=['POST'])
@login_required
@admin_required
def toggle_user_role(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Нельзя изменить свою роль', 'danger')
    else:
        user.role = 'user' if user.role == 'admin' else 'admin'
        db.session.commit()
        flash(f'Роль пользователя {user.username} изменена', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ===== ИНИЦИАЛИЗАЦИЯ =====
def seed_data():
    """Начальные данные"""
    # Биографии
    if Biography.query.count() == 0:
        bios = [
            Biography(name='Нилуфар Рашидова', role='CEO', company='TechUz Solutions',
                      quote='Главное — не бояться начинать. Каждая ошибка — это урок',
                      emoji='👩‍💼', bg_color='#FDF0EC'),
            Biography(name='Дилрабо Юсупова', role='Data Scientist', company='AI Lab UZ',
                      quote='Технологии не имеют пола. Только знания имеют значение',
                      emoji='👩‍🔬', bg_color='#EAF3EE'),
            Biography(name='Камола Азимова', role='Creative Director', company='Adept Agency',
                      quote='Творчество открыло мне двери, которые я не могла найти',
                      emoji='👩‍🎨', bg_color='#FBF4E8'),
            Biography(name='Зулайхо Мирзаева', role='Chief Medical Officer', company='UZ Health',
                      quote='Образование — единственное, что нельзя отнять',
                      emoji='👩‍⚕️', bg_color='#F0EBF8'),
            Biography(name='Муаззам Хасанова', role='CTO', company='Startup Hub Tashkent',
                      quote='Код не делает различий между мужчинами и женщинами',
                      emoji='👩‍💻', bg_color='#FDF0EC'),
            Biography(name='Барно Турсунова', role='Professor', company='TUIT University',
                      quote='Я учу следующее поколение вдохновлённых женщин',
                      emoji='👩‍🏫', bg_color='#EAF3EE'),
        ]
        db.session.add_all(bios)

    # Курсы
    if Course.query.count() == 0:
        courses = [
            Course(title='UX Research & Design', category='Дизайн', hours=42,
                   level='Средний', emoji='🎨', bg_color='#FDF0EC'),
            Course(title='Python для аналитиков данных', category='Программирование',
                   hours=60, level='С нуля', emoji='💻', bg_color='#EAF3EE'),
            Course(title='Digital Marketing Pro', category='Маркетинг',
                   hours=35, level='Средний', emoji='📊', bg_color='#FBF4E8'),
            Course(title='Лидерство для женщин', category='Лидерство',
                   hours=18, level='Начальный', emoji='🗣️', bg_color='#F0EBF8'),
            Course(title='Финансовая грамотность', category='Финансы',
                   hours=24, level='Начальный', emoji='📈', bg_color='#EAF3EE'),
            Course(title='Управление персоналом', category='HR',
                   hours=48, level='Средний', emoji='🤝', bg_color='#FDF0EC'),
            Course(title='Основы облачных технологий', category='IT',
                   hours=30, level='Начальный', emoji='☁️', bg_color='#EFF6FF'),
            Course(title='Свой бизнес с нуля', category='Предпринимательство',
                   hours=52, level='Средний', emoji='🧠', bg_color='#FBF4E8'),
            Course(title='Деловой английский', category='Языки',
                   hours=40, level='Средний', emoji='🌐', bg_color='#EAF3EE'),
        ]
        db.session.add_all(courses)

    db.session.commit()

with app.app_context():
    try:
        db.create_all()
        # Сначала восстанавливаем из бэкапа (если есть)
        restore_from_json()
        # Создать администратора если не существует
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', full_name='Администратор',
                         password_hash=generate_password_hash('admin123'), role='admin')
            db.session.add(admin)
            db.session.commit()
            print("=" * 50)
            print("✅ Администратор создан: admin / admin123")
            print("=" * 50)
        # Демо работодатель
        if not User.query.filter_by(username='click').first():
            emp = User(username='click', full_name='Click Technologies',
                       password_hash=generate_password_hash('click123'), role='employer')
            db.session.add(emp)
            db.session.flush()
            company = Company(user_id=emp.id, name='Click Technologies',
                              city='Ташкент', industry='IT', verified=True)
            db.session.add(company)
            db.session.flush()
            skills1 = json.dumps(['Figma', 'Mobile', 'Research'])
            skills2 = json.dumps(['Prototyping', 'User Testing'])
            skills3 = json.dumps(['Digital', 'SMM', 'Analytics'])
            jobs = [
                Job(company_id=company.id, title='UX/UI Дизайнер',
                    category='IT / Дизайн', salary_from='5 000 000',
                    format='Офис', city='Ташкент', skills_required=skills1,
                    description='Ищем опытного UX/UI дизайнера для работы над мобильными приложениями.'),
                Job(company_id=company.id, title='Product Designer',
                    category='IT / Дизайн', salary_from='$800',
                    format='Удалённо', city='Ташкент', skills_required=skills2,
                    description='Создавайте продуктовый дизайн для миллионов пользователей.'),
                Job(company_id=company.id, title='Marketing Manager',
                    category='Маркетинг', salary_from='4 000 000',
                    format='Гибрид', city='Ташкент', skills_required=skills3,
                    description='Развивайте digital-направление нашей компании.'),
            ]
            db.session.add_all(jobs)
            db.session.commit()
        # Демо соискатель
        if not User.query.filter_by(username='malika').first():
            seeker = User(username='malika', full_name='Малика Азимова',
                          password_hash=generate_password_hash('malika123'), role='seeker',
                          city='Ташкент', profession='UX Designer',
                          skills=json.dumps(['Figma', 'UX Research', 'Prototyping', 'Wireframing']))
            db.session.add(seeker)
            db.session.commit()
        seed_data()
        backup_to_json()
    except Exception as e:
        print(f"⚠️ Ошибка инициализации: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Istiqlol запускается...")
    app.run(debug=True, host='0.0.0.0', port=port)
