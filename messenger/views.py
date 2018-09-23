from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.generic import ListView
from .models import Chat, Message, ImageMessage
from django.contrib.auth.decorators import login_required
from .forms import MessageForm, ImageMessageForm
import datetime
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from profiles.models import Profile, Subscrib


@login_required
def start_chat(request, user_id):
    user = get_object_or_404(User, id = user_id)
    me = get_object_or_404(User, id = request.user.id)
    chat = Chat.objects.filter(member = user).filter(member = me).distinct()
    this_chat = None
    i = 0
    while i<len(chat):
        if chat[i].member.count()==2:
            this_chat =chat[i]
        i = i+1
    if this_chat==None:
        this_chat = Chat.objects.create()
        this_chat.member.add(me, user)
        this_chat.save()
        user_p = get_object_or_404(Profile, user = user)
        user_p.dialogues.add(this_chat)
        user_p.save()
        my_p = get_object_or_404(Profile, user = me)
        my_p.dialogues.add(this_chat)
        my_p.save()

    return redirect ('messenger:chat', this_chat.id)



@login_required
def chat_list(request):
    chat = Chat.objects.filter(member = request.user)
    profile = request.user.profile
    if profile.has_unread_notif():
        notif = True
    else:
        notif = False
    i = 0
    for ch in chat:
        if ch.is_not_group_chat:
            ch.companion = ch.companion(request.user)
        if ch.user_didnt_read(request.user):
            i = i+1
    if i >0:
        unread = True
    else:
        unread = False
    return render(request, 'messenger/chat_list.html', {'chat' : chat, 'unread' : unread, 'profile': profile, 'notif':notif})

@login_required
def ajax_scroll_messages(request, chat_id):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        old_page = int((list(dict_k))[0])
        first_border = old_page*10
        second_border = first_border+10
        chat = get_object_or_404(Chat, id = chat_id)
        messages = Message.objects.filter(chat = chat)[first_border:second_border]
        context = {}
        i = 0
        for message in messages:
            message_context = {}
            message_context.update({'f_n':message.writer.first_name, 'l_n':message.writer.last_name, 'date':message.pub_date, 'wr_id':message.writer.id})
            if message.text:
                message_context.update({'text':message.text})
            if message.is_grey(request.user):
                message_context.update({'grey':True})
            if message.image_box():
                imagelist = ''
                for im in message.image_box():
                    imagelist = imagelist + "<a href=" + im.image.url + "><img src = '" + im.image_ultra.url +  "' style='width: 50px; height: 50px'></a>" + " "
                message_context.update({'images':imagelist})
            context.update({i:message_context})
            i = i + 1
        return JsonResponse(context)


@login_required
def chat(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, id = chat_id)
        profile = request.user.profile
        if profile.has_unread_notif():
            notif = True
        else:
            notif = False
        form = MessageForm()
        form_im = ImageMessageForm()
        messages = Message.objects.filter(chat = chat)[:10][::-1]
        unread = {}
        i=0
        while i <len(messages):
            if request.user in messages[i].who_read.all():
                unread[messages[i]]=True
            else:
                unread[messages[i]]=False
            i = i+1
        return render (request, 'messenger/chat.html', {'messages' : messages, 'form' : form, 'unread':unread, 'form_im':form_im, 'notif': notif, 'profile':profile})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required
def create_chat(request):
    subscribs = Subscrib.objects.filter(who = request.user)
    return render (request, 'messenger/create_chat.html', {'subscribs': subscribs})

@login_required
def ajax_message(request, chat_id):
    chat = get_object_or_404(Chat, id = chat_id)
    if request.method == 'POST' and request.is_ajax:
        text = request.POST['text']
        images = request.FILES.getlist('image')
        if text:
            if images:
                if len(images)>10:
                    context = {'too_much': True}
                    return JsonResponse(context)
            message = Message.objects.create(
                     chat = chat,
                     text = text,
                     writer = request.user,
                     pub_date =datetime.datetime.now()
                     )
            message.who_read.add(request.user)
            if images:
                imagelist = ''
                for image in images:
                    image = ImageMessage.objects.create(
                        letter = message,
                        image = image
                        )
                    imagelist = imagelist + "<a href='" + image.image.url + "'><img src = '" + image.image_ultra.url +  "' style='width: 50px; height: 50px'></a>" + " "
                context = {'text':message.text, 'f_name' : message.writer.first_name, 'l_name': message.writer.last_name, 'images': imagelist}
            else:
                context = {'text':message.text, 'f_name' : message.writer.first_name, 'l_name': message.writer.last_name}
            return JsonResponse(context)
        else:
            if images:
                if len(images)>10:
                    context = {'too_much': True}
                    return JsonResponse(context)
                imagelist = ''
                message = Message.objects.create(
                        chat = chat,
                        writer = request.user,
                        pub_date =datetime.datetime.now()
                        )
                message.who_read.add(request.user)
                for image in images:
                    image = ImageMessage.objects.create(
                        letter = message,
                        image = image
                        )
                    imagelist = imagelist + "<a href='" + image.image.url + "'><img src = '" + image.image_ultra.url +  "' style='width: 50px; height: 50px'></a>" + " "
                context = {'f_name' : message.writer.first_name, 'l_name': message.writer.last_name, 'images': imagelist}
                return JsonResponse(context)


@login_required
def ajax_read_message(request, chat_id):
    if request.method == 'POST' and request.is_ajax:
         chat = get_object_or_404(Chat, id = chat_id)
         messages = Message.objects.filter(chat = chat).exclude(writer = request.user)
         for m in messages:
             if m.is_read == False:
                 m.who_read.add(request.user)
                 if m.who_read.count() == chat.member.count():
                     m.is_read = True
                 m.save()
         context = {'me' : request.user.id}
         return JsonResponse(context)


@login_required
def ajax_make_chat(request):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        list_k = (list(dict_k)[0])
        users = []
        i = 0
        ids = list_k.split(',')
        if len(ids)>1:
            chat = Chat.objects.create()
            chat.member.add(request.user)
            profile = get_object_or_404(Profile, user = request.user)
            profile.dialogues.add(chat)
            for i in ids:
                user = get_object_or_404(User, id = i)
                chat.member.add(user)
                profile = get_object_or_404(Profile, user = user)
                profile.dialogues.add(chat)
                context = {'chat_id' : chat.id}
                return JsonResponse(context)
        elif len(ids) == 1:
            user = get_object_or_404(User, id = ids[0])
            chat = Chat.objects.filter(member = request.user).filter(member = user)
            if len(chat) == 1:
                if chat[0].is_not_group_chat():
                    context = {'chat_id' : chat[0].id}
                    return JsonResponse(context)
                else:
                    chat = Chat.objects.create()
                    chat.member.add(request.user)
                    profile1 = get_object_or_404(Profile, user = request.user)
                    profile1.dialogues.add(chat)
                    chat.member.add(user)
                    profile2 = get_object_or_404(Profile, user = user)
                    profile2.dialogues.add(chat)
                    context = {'chat_id' : chat.id}
                    return JsonResponse(context)
            elif not chat.exists():
                chat = Chat.objects.create()
                chat.member.add(request.user)
                profile1 = get_object_or_404(Profile, user = request.user)
                profile1.dialogues.add(chat)
                chat.member.add(user)
                profile2 = get_object_or_404(Profile, user = user)
                profile2.dialogues.add(chat)
                context = {'chat_id' : chat.id}
                return JsonResponse(context)
            else:
                for ch in chat:
                    i = 0
                    if ch.member.count() == 2:
                        i = i+1
                        if i ==0:
                            chat = Chat.objects.create()
                            chat.member.add(request.user)
                            chat.member.add(user)
                            profile1 = get_object_or_404(Profile, user = request.user)
                            profile1.dialogues.add(chat)
                            profile2 = get_object_or_404(Profile, user = user)
                            profile2.dialogues.add(chat)
                            context = {'chat_id' : chat.id}
                            return JsonResponse(context)
                        else:
                            context = {'chat_id' : ch.id}
                            return JsonResponse(context)