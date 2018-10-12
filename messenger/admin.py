from django.contrib import admin
from .models import Chat, Message, ImageMessage, SessionMessages

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(ImageMessage)
admin.site.register(SessionMessages)
