from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from members.models import Members

@receiver(post_save, sender=Members)
def create_member_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.cspcEmail, password=str(instance.studentNumber))
        if instance.role == Members.OFFICER:
            officer_group, _ = Group.objects.get_or_create(name='Officers')
            user.groups.add(officer_group)
        else:
            member_group, _ = Group.objects.get_or_create(name='Members')
            user.groups.add(member_group)

        user.save()

@receiver(post_delete, sender=Members)
def delete_member_user(sender, instance, **kwargs):
    try:
        user = User.objects.get(username=instance.cspcEmail)
        user.delete()
    except User.DoesNotExist:
        pass