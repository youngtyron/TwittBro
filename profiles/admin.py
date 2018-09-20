from django.contrib import admin
from profiles.models import Profile, Subscrib, Notification, Admittance, Alert
# Register your models here.
admin.site.register(Profile)
admin.site.register(Subscrib)
admin.site.register(Notification)
admin.site.register(Admittance)
admin.site.register(Alert)
