from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    """
    Send activation email when a new user is created
    """
    if created and not instance.is_active:
        try:
            # Generate activation token
            token = default_token_generator.make_token(instance)
            uid = urlsafe_base64_encode(force_bytes(instance.pk))

            # Create activation URL
            activation_url = f"{settings.FRONTEND_URL}/users/activate/{uid}/{token}/"

            subject = "Activate Your Account - Task Management"
            message = f"""
Hi {instance.username},

Thank you for signing up for Task Management!

Please click the link below to activate your account:
{activation_url}

If you didn't create this account, please ignore this email.

Best regards,
The Task Management Team
            """.strip()

            recipient_list = [instance.email]

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False,
            )

            print(f"Activation email sent successfully to {instance.email}")

        except Exception as e:
            print(f"Failed to send activation email to {instance.email}: {str(e)}")
            # You could also log this to a file or send to a monitoring service
