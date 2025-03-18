import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Maestro.settings")
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


site_id = 1


site = Site.objects.get(id=site_id)
site.domain = "maestro-production-423a.up.railway.app"
site.name = "maestro-production-423a.up.railway.app"
site.save()

print(f"Updated site ID {site_id} to domain: {site.domain} and name: {site.name}")


social_app, created = SocialApp.objects.get_or_create(
    name="MaestroApp",
    defaults={
        "client_id": os.getenv("CLIENT_ID"),
        "secret": os.getenv("SECRET_KEY"),
    }
)

if site not in social_app.sites.all():
    social_app.sites.add(site)
    social_app.save()

print(f"Social Application '{social_app.name}' configured successfully!")
