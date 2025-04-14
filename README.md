# Awards API Platform

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

**Клонирование репозитория:**

   ```bash
   git clone <ссылка-на-репозиторий>
   cd awards_api
   ```
устанавливаем все requirements.txt


**Запуск Docker Compose:**

```bash
docker-compose up --build
```

**Применение миграций, сбор статики и создание суперпользователя:**

Откройте отдельный терминал и выполните следующие команды:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py createsuperuser
```

**Получение токенов/информации:**

## В Swagger проходим authorize (замочек) вставляем обязательно
```bash
 Bearer <полученный_access_токен>
```
http://localhost:8080/swagger/
То есть обязательно введите префикс Bearer перед токеном. 


```bash
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testSuperTest", "password": "testSuperTest"}'

Пример ответа:

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Запрос информации о профиле:

Используйте полученный access‑токен (обязательно с префиксом Bearer ):

curl -v -X GET http://localhost:8000/api/profile/ \
     -b '' \
     -H "Authorization: Bearer <access_token>"
```
**Тестирование отложенных задач (Celery):**

Для запроса награды отправьте:
```bash
curl -X POST http://localhost:8000/api/rewards/request/ \
     -H "Authorization: Bearer <access_token>"
После заданной задержки (обычно 5 минут) проверьте, что у пользователя поле coins увеличилось и появилась запись в RewardLog.
```



## Демонстрация тестов/ запросов через терминал
```bash
stasiastasias@jopa Desktop % curl -X POST http://localhost:8080/api/token/ \    
     -H "Content-Type: application/json" \
     -d '{"username": "testSuperTest", "password": "testSuperTest"}'

{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDcyNjk5NywiaWF0IjoxNzQ0NjQwNTk3LCJqdGkiOiI5YzdmZmM4NzA5NTk0NGYyYWVjMTgxOWU5ZTA4YTRlNSIsInVzZXJfaWQiOjJ9.oVeSKYLndCUZCUgNfZSYnxtp9rfMQlTaP7VVVd45hJs","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjQwODk3LCJpYXQiOjE3NDQ2NDA1OTcsImp0aSI6IjFiNTU2MThkYmY2MjRlNzY4ZjJmNjU0NzU1NGJmYWNkIiwidXNlcl9pZCI6Mn0.1hbMHo9Xb22QJeMrGFRLRWogBXKm87djmvQ7dPL3BDY"}%                                         
stasiastasias@jopa Desktop % curl -v -X GET http://localhost:8080/api/profile/ \
    -b '' \                               
    -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjQwODk3LCJpYXQiOjE3NDQ2NDA1OTcsImp0aSI6IjFiNTU2MThkYmY2MjRlNzY4ZjJmNjU0NzU1NGJmYWNkIiwidXNlcl9pZCI6Mn0.1hbMHo9Xb22QJeMrGFRLRWogBXKm87djmvQ7dPL3BDY"

Note: Unnecessary use of -X or --request, GET is already inferred.
* WARNING: failed to open cookie file ""
*   Trying [::1]:8080...
* Connected to localhost (::1) port 8080
> GET /api/profile/ HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/8.4.0
> Accept: */*
> Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjQwODk3LCJpYXQiOjE3NDQ2NDA1OTcsImp0aSI6IjFiNTU2MThkYmY2MjRlNzY4ZjJmNjU0NzU1NGJmYWNkIiwidXNlcl9pZCI6Mn0.1hbMHo9Xb22QJeMrGFRLRWogBXKm87djmvQ7dPL3BDY
> 
< HTTP/1.1 200 OK
< Server: gunicorn
< Date: Mon, 14 Apr 2025 14:23:56 GMT
< Connection: close
< Content-Type: application/json
< Vary: Accept, origin
< Allow: GET, HEAD, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 311
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< 
* Closing connection
{"username":"testSuperTest","id":2,"is_authenticated":true,"auth_header":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjQwODk3LCJpYXQiOjE3NDQ2NDA1OTcsImp0aSI6IjFiNTU2MThkYmY2MjRlNzY4ZjJmNjU0NzU1NGJmYWNkIiwidXNlcl9pZCI6Mn0.1hbMHo9Xb22QJeMrGFRLRWogBXKm87djmvQ7dPL3BDY"}%   stasiastasias@jopa Desktop % curl -X POST http://localhost:8080/api/token/ \    
     -H "Content-Type: application/json" \
     -d '{"username": "adminTest", "password": "adminTest"}'    

{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDcyNzA2NiwiaWF0IjoxNzQ0NjQwNjY2LCJqdGkiOiJkM2EzZWZmNzNmOGU0YjU2YjljZTAzNzUxNGVmZGExOCIsInVzZXJfaWQiOjF9.sk_a3WD4-qcBwbTNVmyj-0jKssqcjaGLvWUfQX0Gov4","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjQwOTY2LCJpYXQiOjE3NDQ2NDA2NjYsImp0aSI6ImMzYzQ0YjgyZDdiZjQ3MTU5ODQyMTA2NDBjZjA1ZWU4IiwidXNlcl9pZCI6MX0.LZQ2a29RMANOqoe7Srw-SXvfidsqGYW9BmnxedWqaMk"}%                                         
stasiastasias@jopa Desktop % curl -v -X GET http://localhost:8080/api/profile/ \
    -b '' \                               
    -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjQwOTY2LCJpYXQiOjE3NDQ2NDA2NjYsImp0aSI6ImMzYzQ0YjgyZDdiZjQ3MTU5ODQyMTA2NDBjZjA1ZWU4IiwidXNlcl9pZCI6MX0.LZQ2a29RMANOqoe7Srw-SXvfidsqGYW9BmnxedWqaMk"

Note: Unnecessary use of -X or --request, GET is already inferred.
* WARNING: failed to open cookie file ""
*   Trying [::1]:8080...
* Connected to localhost (::1) port 8080
> GET /api/profile/ HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/8.4.0
> Accept: */*
> Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjQwOTY2LCJpYXQiOjE3NDQ2NDA2NjYsImp0aSI6ImMzYzQ0YjgyZDdiZjQ3MTU5ODQyMTA2NDBjZjA1ZWU4IiwidXNlcl9pZCI6MX0.LZQ2a29RMANOqoe7Srw-SXvfidsqGYW9BmnxedWqaMk
> 
< HTTP/1.1 200 OK
< Server: gunicorn
< Date: Mon, 14 Apr 2025 14:24:59 GMT
< Connection: close
< Content-Type: application/json
< Vary: Accept, origin
< Allow: GET, HEAD, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 307
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< 
* Closing connection
{"username":"adminTest","id":1,"is_authenticated":true,"auth_header":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjQwOTY2LCJpYXQiOjE3NDQ2NDA2NjYsImp0aSI6ImMzYzQ0YjgyZDdiZjQ3MTU5ODQyMTA2NDBjZjA1ZWU4IiwidXNlcl9pZCI6MX0.LZQ2a29RMANOqoe7Srw-SXvfidsqGYW9BmnxedWqaMk"}%       stasiastasias@jopa Desktop % 
```
