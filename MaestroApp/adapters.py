from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from allauth.account.models import EmailAddress


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # If user already exists, prevent duplicate sign-up
        if sociallogin.user.id:
            return

        email = sociallogin.account.extra_data.get("email")
        if email:
            try:
                user = EmailAddress.objects.get(email=email).user
                sociallogin.connect(request, user)
            except EmailAddress.DoesNotExist:
                pass
