web: python manage.py collectstatic --noinput && gunicorn vthomefix.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
