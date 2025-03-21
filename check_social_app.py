import os
import django
from allauth.socialaccount.models import SocialApp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Maestro.settings')
django.setup()

# Query for existing SocialApps
apps = SocialApp.objects.filter(provider='google')
if apps.exists():
    for app in apps:
        print(f'✅ ID: {app.id}, Name: {app.name}, Sites: {list(app.sites.values_list("domain", flat=True))}')
else:
    print("No Google SocialApp found.")