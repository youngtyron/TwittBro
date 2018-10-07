from django.db import models
from django.contrib.auth.models import User
import PIL
# from PIL import Image
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
import datetime
from datetime import timezone
from datetime import timedelta
from posts.models import Post
from messenger.models import Message, Chat, SessionMessages
from django.shortcuts import get_object_or_404

# pip install django-imagekit -------- ТАК СКАИЧВАТЬ ИМАДЖКИТ!!!

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    status = models.CharField(max_length = 255, blank =True, null = True)
    registrated = models.DateField()
    birth_date = models.DateField(blank =True, null = True)
    avatar = models.ImageField(upload_to="images/", null = True, blank = True)
    avatar_small = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(100, 100)], format = 'JPEG', options = {'quality' : 75})
    avatar_ultra = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(50, 50)], format = 'JPEG', options = {'quality' : 50})
    avatar_micro = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(25, 25)], format = 'JPEG', options = {'quality' : 25})
    dialogues = models.ManyToManyField(Chat)
    is_closed = models.BooleanField(default = False)
    rating = models.PositiveIntegerField(default = 0)

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def reassign(self):
        sessionmessage = SessionMessages.objects.filter(user = self.user)
        if sessionmessage.exists():
            sessionmessage.update(time=datetime.datetime.now())
            return
        else:
            SessionMessages.objects.create(user = self.user, time = datetime.datetime.now())
            return

    def disassign(self):
        sessionmessage = SessionMessages.objects.filter(user = self.user)
        if sessionmessage.exists():
            sessionmessage.delete()
            return
        else:
            return

    def updated_chats(self):
        chats = Chat.objects.filter(member = self.user)
        sessionmessages = get_object_or_404(SessionMessages, user = self.user)
        updated_chats = []
        for chat in chats:
            new_messages = chat.messages.filter(is_read = False).exclude(who_read = self.user).filter(pub_date__gt = sessionmessages.time)
            if new_messages.exists():
                updated_chats.append(chat)
        return updated_chats

    def my_following(self):
        following = []
        queryset = Subscrib.objects.filter(who = self.user)
        for q in queryset:
            following.append(q.to)
        return following

    def my_followers(self):
        followers = []
        queryset = Subscrib.objects.filter(to = self.user)
        for q in queryset:
            followers.append(q.who)
        return followers

    def plus_popularity(self):
        self.rating = self.rating + 1
        self.save()
        return

    def minus_popularity(self):
        self.rating = self.rating - 1
        self.save()
        return

    def has_unread_notif(self):
        unread_notif = Notification.objects.filter(recipient = self.user, status = 'Not read')
        if unread_notif.exists():
            return True
        else:
            return False

    def has_access(self, user):
        if self.user == user:
            return True
        elif user.profile.is_closed:
            admit = Admittance.objects.filter(for_user = self.user, on_page = user)
            if admit.exists():
                return True
            else:
                return False
        else:
            return True

    def red_envelope(self): #ПРОВЕРКА, ИМЕЕТ ЛИ ПРОФИЛЬ НЕПРОЧИТАННЫЕ СООБЩЕНИЯ
        chats = Chat.objects.filter(member = self.user)
        i = 0
        for chat in chats:
            if chat.has_unread_messages(self.user):
                i =i+ 1
        if i <1:
            return False
        else:
            return True

    def is_follower(self, user):
        fol = Subscrib.objects.filter(who = self.user, to = user)
        fol2 = Subscrib.objects.filter(to = self.user, who = user)
        admit = Admittance.objects.filter(for_user = self.user, on_page = user)
        if fol.exists() and not fol2.exists() and not admit.exists():
            return True

    def small_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar_small.url
        else:
            return '/static/images/default_ava.jpg'

    def ultra_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar_ultra.url
        else:
            return '/static/images/default_ava.jpg'

    def micro_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar_micro.url
        else:
            return '/static/images/default_ava.jpg'

    def avatar_opening_link(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return '/static/images/default_ava.jpg'

class Subscrib(models.Model):
    who = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'subcribed')
    to = models.ForeignKey(User, on_delete = models.CASCADE)
    subs_date = models.DateTimeField()

    def __str__(self):
        return '%s to -> %s' % (self.who, self.to)

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.CharField(max_length = 255)
    time = models.DateTimeField()
    notificator = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True, related_name = 'notices')
    N = 'Not read'
    R = 'Read'
    status_choices = ((N, 'Not read'),(R, 'Read'))
    status = models.CharField(max_length=30, choices = status_choices, default = 'Not read')
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE, null = True, blank = True)
    object_id = models.PositiveIntegerField(null = True, blank = True)
    content_object = GenericForeignKey('content_type', 'object_id')
    L = 'Like'
    Rp = 'Repost'
    Sub = 'Subscribe'
    An = 'Another'
    PCom = 'PostComment'
    CCom = 'CommentComment'
    about_choices = ((L, 'Like'), (Rp, 'Repost'), (Sub, 'Subscribe'), (An, 'Another'), (PCom, 'PostComment'), (CCom, 'CommentComment'))
    about =  models.CharField(max_length=30, choices = about_choices, default = 'Another')


    class Meta:
        ordering = ['-time']

    def __str__(self):
        return '%s %s, %s, %s, %s' % (self.recipient.first_name, self.recipient.last_name, self.status, self.about, self.content_object)

    def is_older_than_day(self):
        now = datetime.datetime.now(timezone.utc)
        day = timedelta(hours = 24)
        if (now - self.time) > day:
            return True
        else:
            return False

class Admittance(models.Model):
    for_user = models.ForeignKey(User, on_delete = models.CASCADE)
    on_page = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'profile_admittance')

    def __str__(self):
        return 'for %s on page %s' % (self.for_user.username, self.on_page.username)

class Alert(models.Model):   #МОДЕЛЬ, ГЕНЕРИРУЕМАЯ ПРИ НЕПРАВИЛЬНОМ ВВОДЕ ПАРОЛЯ
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
