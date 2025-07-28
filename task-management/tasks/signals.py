from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task


@receiver(m2m_changed, sender=Task.assigned_to.through)
def task_assigned_to_changed(sender, instance, action, **kwargs):
    if action == "post_add":
        assigned_emails = [employee.email for employee in instance.assigned_to.all()]

        print(f"Task '{instance.title}' assigned to: {', '.join(assigned_emails)}")
        send_mail(
            subject="Task Assigned",
            message=f"You have been assigned to a new task: {instance.title}",
            from_email="from@example.com",
            recipient_list=assigned_emails,
            fail_silently=False,
        )


@receiver(post_delete, sender=Task)
def task_deleted(sender, instance, **kwargs):
    if instance.details:
        print(f"Task '{instance.title}' deleted with details: {instance.details}")
        instance.details.delete()

        print(f"Details for task '{instance.title}' have been deleted.")