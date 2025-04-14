# Awards API Platform

Это Django backend-приложение для управления пользователями и наградами. Реализована JWT-аутентификация, отложенные задачи с Celery/Redis, а также REST API для профиля и наград.

## Функциональность

- **Аутентификация:**
  - JWT: `/api/token/`, `/api/token/refresh/`, `/api/token/verify/`
- **Пользовательская модель:**
  - Расширенный пользователь с полем `coins`
- **API:**
  - GET `/api/profile/` — информация о пользователе
  - GET `/api/rewards/` — список выданных наград
  - POST `/api/rewards/request/` — запрос награды (ограничение: 1 раз в сутки)
- **Отложенные задачи:**
  - Модель `ScheduledReward` планирует выдачу награды.
  - В заданное время с помощью Celery начисляются монеты и создаётся запись в `RewardLog`.
- **Документация:**
  - Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

## Технологии

- Django, Django REST Framework
- PostgreSQL
- Celery + Redis
- JWT, CORS, CSRF
- Docker & docker-compose

## Запуск проекта

1. **Клонирование репозитория:**

   ```bash
   git clone <ссылка-на-репозиторий>
   cd awards_api


stasiastasias@jopa Desktop % curl -X POST http://localhost:8080/api/token/ \ 
     -H "Content-Type: application/json" \
     -d '{"username": "adminTest", "password": "adminTest"}'

{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDcyMjIzNCwiaWF0IjoxNzQ0NjM1ODM0LCJqdGkiOiIyZjFmMzBlZjIxYzk0ODliOWYzNTUzY2ExNTE2Zjk2NSIsInVzZXJfaWQiOjF9.3B6lT0w2xLDPqMXe9PKCxBNzRDPNm2WuFD23dFc--Wk","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjM2MTM0LCJpYXQiOjE3NDQ2MzU4MzQsImp0aSI6ImNmMDIyYWRjZjJjMDQ2NWI4Njk5ZTBlODVmYjkzOGE5IiwidXNlcl9pZCI6MX0.coU49fGLo9eaVeNyZPGxbKSC4h05SXO9Ly4Ms-tyJmM"}%                                         stasiastasias@jopa Desktop % curl -X GET http://localhost:8080/api/profile/ \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjM2MTM0LCJpYXQiOjE3NDQ2MzU4MzQsImp0aSI6ImNmMDIyYWRjZjJjMDQ2NWI4Njk5ZTBlODVmYjkzOGE5IiwidXNlcl9pZCI6MX0.coU49fGLo9eaVeNyZPGxbKSC4h05SXO9Ly4Ms-tyJmM"
{"username":"adminTest","email":"stasiastasias@yahoo.com","coins":0}%                                