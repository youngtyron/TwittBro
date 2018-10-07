from django.contrib import admin
from .models import Chat, Message, ImageMessage, SessionMessages
# Register your models here.
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(ImageMessage)
admin.site.register(SessionMessages)
