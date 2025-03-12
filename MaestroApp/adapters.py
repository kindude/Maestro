from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import login
from django.contrib.auth import get_user_model

User = get_user_model()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """Automatically links the Google account if email exists; otherwise, creates a new user."""

        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get("email")
        if email:
            try:
                user = EmailAddress.objects.get(email=email).user
                sociallogin.connect(request, user)
                user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
                login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

            except EmailAddress.DoesNotExist:
                user = User.objects.create(
                    email=email,
                    username=email.split('@')[0],
                )
                user.set_unusable_password()
                user.save()

                sociallogin.connect(request, user)
                user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
                login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
