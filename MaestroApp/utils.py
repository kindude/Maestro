from django.contrib.contenttypes.models import ContentType

from MaestroApp.models import UserNotificationStatus, MaestroNotification, MaestroUser


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
        notification.save()

    # Create UserNotificationStatus entries instead of direct ManyToMany relation
    for user in users:
        UserNotificationStatus.objects.create(user=user, notification=notification, is_read=False)