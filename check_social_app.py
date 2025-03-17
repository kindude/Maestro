from allauth.socialaccount.models import SocialApp

apps = SocialApp.objects.filter(provider='google')
for app in apps:
    print(f'ID: {app.id}, Name: {app.name}, Sites: {app.sites.all()}')
