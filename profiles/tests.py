from django.test import TestCase
# from django.test.client import Client
import random
import datetime
from django.utils import timezone
from django.urls import reverse
from profiles.models import Profile, Notification
from django.contrib.auth.models import User
# Create your tests here.

# class UserAndProfileTest(TestCase):
#
#     def set_up(self):
#         i = 0
#         firstnamebox = ['John', 'Lee', 'Martin', 'Mark', 'Stephen', 'Emily', 'Ruby', 'Jen', 'Claire', 'Courtney']
#         lastnamebox = ['McLaren', 'Brown', 'Anderson', 'Write', 'Collins', 'Morris', 'Young', 'Wolf']
#         while i<20:
#             user = User.objects.create(username = str(i) + 'username', password = str(i) + 'username', email = str(i) + 'email@mail.com', first_name = random.choice(firstnamebox), last_name = random.choice(lastnamebox))
#             Profile.objects.create(user = user, registrated = datetime.datetime.now())
#             i = i+1
#             # print(user.first_name + " "+ user.last_name)
#             # print(user.profile.registrated)
#         profiles = Profile.objects.all()
#         i = 0
#         while i<11:
#             profile = random.choice(profiles)
#             profile.is_closed = True
#             profile.save()
#             i = i +1
#         closed = Profile.objects.filter(is_closed = True)
#         opened = Profile.objects.filter(is_closed = False)
#         print("CLOSED PROFILES:")
#         for c in closed:
#             print(c.user.first_name + " "+ c.user.last_name)
#             print(c.user.username)
#         print('----------------')
#         print('OPENED PROFILES:')
#         for o in opened:
#             print(o.user.first_name + " "+ o.user.last_name)
#             print(o.user.username)

class ReadingNotifTest(TestCase):

    def read_and_delete(self):
        user = User.objects.create(username = 'username', password = 'password', email = 'email@mail.com', first_name = 'John', last_name = 'Smith')
        user2 = User.objects.create(username = 'username2', password = 'password2', email = 'email2@mail.com', first_name = 'Bill', last_name = 'Low')
        i = 0
        pasttime = timezone.now() - datetime.timedelta(days = 3)
        # print('BEFORE READING')
        while i<6:
            notif = Notification.objects.create(recipient = user, text = 'text', time = timezone.now(), notificator = user2)
            # print(notif.time)
            i = i+1
        while i<11:
            notif = Notification.objects.create(recipient = user, text = 'text', time = pasttime, notificator = user2)
            i = i+1
            # print(notif.time)
        self.client.login(username='username', password='password')
        # self.client.post(reverse('ajax_notif_update'))
        # print(self.client.post(reverse('ajax_notif_update')).status_code)
        notif = Notification.objects.all()
        for n in notif:
            n.status = 'Read'
            n.save()
        resp = self.client.get(reverse('notifications'))
        print(resp.status_code)
        # print(self.client.get(reverse('notifications')).status_code)
        N = Notification.objects.filter(recipient = user)
        # print('AFTER READING')
        # for n in N:
            # print(n.time, n.status, n.is_older_than_day())
        # self.assertEqual(N.count(),5)
