from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

User = get_user_model()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email")

        if not email:
            return  # No email found, let AllAuth handle it

        try:
            user = EmailAddress.objects.get(email=email).user
            sociallogin.connect(request, user)
        except EmailAddress.DoesNotExist:
            pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        base_username = slugify(user.email.split("@")[0])
        unique_username = base_username
        counter = 1

        while User.objects.filter(username=unique_username).exists():
            unique_username = f"{base_username}-{counter}"
            counter += 1

        user.username = unique_username
        user.save()

        if user.groups.count() == 0:
            default_group, _ = Group.objects.get_or_create(name="Student")
            user.groups.add(default_group)

        return user
