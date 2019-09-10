from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
from django.utils import timezone
from django.utils.datetime_safe import datetime

from todo_app.models import Post


@shared_task
def warning_email(email, link):
    subject, from_email, to = 'Notification', settings.EMAIL_HOST_USER, email
    text_content = 'Time is running out'
    html_content = """
                    <tr>
                        <td bgcolor="#ffffff" style="padding: 40px 40px; font-family: sans-serif; font-size: 15px; line-height: 20px; color: #555555; text-align: center;">
                            <p style="margin: 0;">Listə baxmaq üçün düyməyə klikləyərək səhfəyə keçid edin</p>
                        </td>
                    </tr>
                    <tr>
                        <td bgcolor="#ffffff" style="padding: 0 40px 40px; font-family: sans-serif; font-size: 15px; line-height: 20px; color: #555555;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin: auto">
                                <tr>
                                    <td style="border-radius: 3px; background: #20bdb7; text-align: center;" class="button-td">
                                        <a href="{}" style="background: #20bdb7; border: 15px solid #20bdb7; font-family: sans-serif; font-size: 13px; line-height: 1.1; text-align: center; text-decoration: none; display: block; border-radius: 3px; font-weight: bold;" class="button-a">
                                            &nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ffffff;">View</span>&nbsp;&nbsp;&nbsp;&nbsp;
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            <!-- Button : END -->
                        </td>
                    </tr>
                    """.format("http://localhost:8000/" + link)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return "Success"




