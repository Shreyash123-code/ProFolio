import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_django_project.settings")
django.setup()

from django.contrib.auth.models import User

# Check if superuser exists
if not User.objects.filter(username='admin').exists():
    print("Creating superuser 'admin' with password 'adminpass'...")
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
    print("Superuser created successfully.")
else:
    print("Superuser 'admin' already exists.")
