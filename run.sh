cd app
gunicorn -b 0.0.0.0:8080 flask_health_charges:app
