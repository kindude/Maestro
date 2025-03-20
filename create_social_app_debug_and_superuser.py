import os
import django
from dotenv import load_dotenv
load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Maestro.settings")
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')


site_id = 1


site = Site.objects.get(id=site_id)
site.domain = "127.0.0.1:8000"
site.name = "127.0.0.1:8000"
site.save()

print(f"Updated site ID {site_id} to domain: {site.domain} and name: {site.name}")


social_app, created = SocialApp.objects.get_or_create(
    name="MaestroApp",
    defaults={
        "client_id": os.getenv("CLIENT_ID"),
        "secret": os.getenv("CLIENT_SECRET"),
    }
)

if site not in social_app.sites.all():
    social_app.sites.add(site)
    social_app.save()

print(f"Social Application '{social_app.name}' configured successfully!")