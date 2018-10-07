from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from PIL import Image
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust,ResizeToFill
from django.shortcuts import get_object_or_404

class Chat(models.Model):
    name = models.CharField(max_length=100, default = 'dialogue')
    pict = models.ImageField(upload_to ='profile_img', blank = True, null =True)
    pict_small = ImageSpecField([Adjust(contrast=1, sharpness=1),
                  ResizeToFill(90, 90)],
                  format='JPEG', options={'quality': 50})
    member = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/messages/chat/%i/" % self.id
 
    def chat_small_pict_url(self):
        if self.pict and hasattr(self.pict, 'url'):
            return self.pict_small.url
        else:
            return '/static/images/people.jpg'

    def facial_message(self):
        last_message = Message.objects.filter(chat=self).latest()
        return last_message

    def members(self):
        return self.member.all()

    def user_didnt_read(self, user):
        messages = self.messages.all()
        i = 0
        for mess in messages:
            if user not in mess.who_read.all():
                i = i +1
        if i>0:
            return True
        else:
            return False

    def has_unread_messages(self, user):
        messages = self.messages.filter(is_read = False).exclude(who_read = user)
        if messages.exists():
            return True
        else:
            return False

    def is_not_group_chat(self):
        if self.member.count()>2:
            return False
        else:
            return True

    def is_group_chat(self):
        if self.member.count()>2:
            return True
        else:
            return False

    def companion(self, user):
        companion = self.member.exclude(id = user.id)[0]
        return companion

    def updated_messages(self, user):
        sessionmessages = get_object_or_404(SessionMessages, user = user)
        messages = self.messages.filter(is_read = False).exclude(who_read = user).filter(pub_date__gt = sessionmessages.time)
        return messages


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE, related_name = 'messages' )
    text = models.CharField(max_length=1000, null = True, blank = True)
    writer = models.ForeignKey(User, on_delete = models.CASCADE)
    pub_date = models.DateTimeField(default=datetime.datetime.now())
    is_read = models.BooleanField(default=False)
    who_read = models.ManyToManyField(User, related_name = 'read_messages')

    class Meta:
        ordering=['-pub_date']
        get_latest_by = 'pub_date'

    def __str__(self):
        return '%s %s - %s - %s' %(self.writer.first_name, self.writer.last_name, self.chat.name, self.pub_date)

    def recieved(self):
        return self.who_read.all()

    def image_box(self):
        image_box = ImageMessage.objects.filter(letter = self)
        return image_box

    def has_two_readers(self):
        if self.who_read.all().count() >1:
            return True
        else:
            return False

    def is_grey(self, user):
        if self.is_read:
            return False
        else:
            if self.chat.is_group_chat():
                if user is self.writer and self.has_two_readers():
                    return False
                elif user in self.recieved() and user != self.writer:
                    return False
                else:
                    return True
            else:
                return True

class ImageMessage(models.Model):
    letter = models.ForeignKey(Message, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="images/", null = True, blank = True)
    image_small = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(100, 100)], format = 'JPEG', options = {'quality' : 75})
    image_ultra = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(50, 50)], format = 'JPEG', options = {'quality' : 50})

    def __str__(self):
        return self.letter.writer.username

class SessionMessages(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    time = models.DateTimeField()

    def __str__(self):
        return self.user.username
