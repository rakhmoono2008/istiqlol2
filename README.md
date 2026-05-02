# Istiqlol — Карьерная платформа для женщин

Платформа поиска работы для женщин Узбекистана с AI-рекомендациями и интеграцией One ID.

## Стек
- Backend: FastAPI + Python
- Frontend: React + Vite
- База данных: PostgreSQL
- Аутентификация: One ID (egov.uz OAuth2)
- AI: Cosine similarity + геолокация
- Деплой: Railway

---

## Запуск локально

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
# Отредактируй .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
Docs: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```
App: http://localhost:5173

---

## Деплой на Railway

1. railway.app → New Project → Deploy from GitHub
2. + New → Database → PostgreSQL
3. Переменные окружения:
```
DATABASE_URL=<из Railway>
SECRET_KEY=your-secret-key
ONE_ID_CLIENT_ID=xxx
ONE_ID_CLIENT_SECRET=xxx
ONE_ID_REDIRECT_URI=https://your-app.railway.app/auth/callback
```

## API эндпоинты

| Метод | URL | Описание |
|---|---|---|
| GET | /auth/login | Редирект на One ID |
| GET | /jobs/ | Список вакансий |
| POST | /jobs/ | Создать вакансию |
| GET | /profile/{id} | Профиль |
| PUT | /profile/{id} | Обновить профиль |
| GET | /recommendations/ | AI-рекомендации |
| GET | /courses/ | Курсы |
