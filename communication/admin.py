from django.contrib import admin
from communication.models import Announcement, Message

admin.site.register(Message)
admin.site.register(Announcement)