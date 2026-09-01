from apps.notifications.models import Notification
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def send_notification(user, title, message, notification_type):
        # 1. In-App Notification
        Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type
        )
        
        # 2. Email Notification
        email_host = getattr(settings, 'EMAIL_HOST', None)
        email_host_user = getattr(settings, 'EMAIL_HOST_USER', None)
        
        if email_host and email_host_user:
            try:
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', email_host_user)
                send_mail(
                    subject=title,
                    message=message,
                    from_email=from_email,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Failed to send email to {user.email}: {e}")

        # 3. SMS/Push placeholder logs
        logger.info(f"Notification [{notification_type}] sent to {user.email}: {title}")
