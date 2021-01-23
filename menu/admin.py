import os
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
import threading
from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.core.mail import (send_mail, BadHeaderError, EmailMessage)
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.auth.models import User
from .models import Menu, Lunch, Option, Submission, Answer, timezone, BroadCast_Email

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        message = Mail(from_email='pablo@team.cr',to_emails=self.recipient_list ,subject='CorneMenu Day 23/1/2021',html_content='<a href="http://35.222.64.43:8006/menus/1/start/">CornerMenu Day 21/01/2021</a>')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            print(message)
        except Exception as e:
            print(e.message)


class BroadCast_Email_Admin(admin.ModelAdmin):
    model = BroadCast_Email

    def submit_email(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in User.objects.all() ] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email.short_description = 'Submit BroadCast (1 Select Only)'
    submit_email.allow_tags = True

    actions = [ 'submit_email' ]

    list_display = ("subject", "created")
    search_fields = ['subject',]

admin.site.register(Menu)
admin.site.register(Lunch)
admin.site.register(Option)
admin.site.register(Submission)
admin.site.register(Answer)
admin.site.register(BroadCast_Email, BroadCast_Email_Admin)

