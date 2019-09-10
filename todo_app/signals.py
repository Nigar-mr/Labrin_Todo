from datetime import timedelta

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.datetime_safe import datetime
from todo_app.models import Verification, Post
from todo_app.tasks import warning_email
from threading import Thread

User = get_user_model()



#
# @receiver(post_save, sender=Verification, dispatch_uid='send_mail_to_user')
# def send_mail_to_user(*args, **kwargs):
#     obj = kwargs.get("instance")
#     created = kwargs.get("created")
#     if created:
#         link = f"http://localhost:8008/verify/{obj.token}/{obj.user_id}/"
#         background_job = Thread(target=warning_email, args=(obj.user.email, link))
#         background_job.start()
#
#



@receiver(post_save, sender=Verification, dispatch_uid='send_mail_to_user')
def send_mail_to_user(*args, **kwargs):
    obj = kwargs.get("instance")
    now = datetime.now(timezone.utc)
    post = Post.objects.all()
    date = post.datetime - now - timedelta(seconds=600)
    link = f"http://localhost:8000/"
    warning_email.apply_async(args=(obj.user.email, link), eta=now + date)