Hotel Booking Django Project (Full)

Steps to run locally (using Docker):
1. docker compose up --build
2. Wait for migrations to run and the server to start on http://localhost:8000
3. Create superuser: docker compose run web python manage.py createsuperuser
4. Seed data: docker compose run web python manage.py seed_db

Steps to run locally (without Docker):
1. python -m venv venv
2. source venv/bin/activate  (or venv\Scripts\activate on Windows)
3. pip install -r requirements.txt
4. Set env vars for DATABASE_*, DJANGO_SECRET_KEY
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py seed_db
