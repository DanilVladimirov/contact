web: gunicorn vk.wsgi
web: daphne therapist_portal.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py runworker channel_layer