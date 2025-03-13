from .models import MaestroNotification, MaestroUser
from django.contrib.contenttypes.models import ContentType


def create_notification(users, title, message, notification_type, related_object=None):
    if isinstance(users, MaestroUser):
        users = [users]

    notification = MaestroNotification.objects.create(
        title=title,
        message=message,
        notification_type=notification_type,
    )

    if related_object:
        notification.content_type = ContentType.objects.get_for_model(related_object)
        notification.object_id = related_object.id

    notification.users.set(users)

    for user in users:
        user.notifications.add(notification)
        user.save()
