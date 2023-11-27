# Local Setup

Run docker db container

```bash
# Start db container
docker compose up

# Migrate databases
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```


# Authentication
Project uses JWT authentication

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret"}' \
  http://localhost:8000/api/token/
```

That will return access and refresh tokens. To refresh access token use endpoint

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":""eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5OTU2NTg4MywiaWF0IjoxNjk5NDc5NDgzLCJqdGkiOiIwZWI0MGQzODQ2YTE0Zjc4OWIyMDQzYWQ1MzUyYjJjNyIsInVzZXJfaWQiOjF9.W56Qlhdwz6NNAM0YL8zSRa6u1JA_-7jtMsUenm5T44E""}' \
  http://localhost:8000/api/token/refresh/
```
