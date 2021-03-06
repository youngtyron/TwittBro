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
def ajax_update_chat(request, chat_id):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        last_message_id = int((list(dict_k))[0])
        chat = get_object_or_404(Chat, id = chat_id)
        last_message = get_object_or_404(Message, id = last_message_id)
        new_messages = Message.objects.filter(chat = chat).filter(pub_date__gt = last_message.pub_date)
        if new_messages.exists():
            context = {}
            i = 0
            for message in new_messages:
                message_context = {'f_n':message.writer.first_name, 'l_n':message.writer.last_name, 'date':message.pub_date.strftime("%b. %d, %Y, %I:%M %p"), 'wr_id':message.writer.id, 'id':message.id}
                if message.text:
                    message_context.update({'text':message.text})
                if message.is_grey(request.user):
                    message_context.update({'grey':True})
                if message.image_box():
                    imagelist = ''
                    for im in message.image_box():
                        imagelist = imagelist + "<img src = '" + im.image_ultra.url +  "' style='width: 50px; height: 50px' class ='mini-images' name = '"+im.image.url+"'>" + " "
                    message_context.update({'images':imagelist})
                context.update({i:message_context})
                i = i+1
            return JsonResponse(context)
        else:
            context= {'none':True}
            return JsonResponse(context)

@login_required
def ajax_drop_chat(request, chat_id):
    if request.method == 'POST' and request.is_ajax:
        chat = get_object_or_404(Chat, id = chat_id)
        profile = get_object_or_404(Profile, user = request.user)
        chat.member.remove(request.user)
        chat.save()
        profile.dialogues.remove(chat)
        return HttpResponse()

@login_required
def chat_list(request):
    chat = Chat.objects.filter(member = request.user)
    profile = request.user.profile
    if profile.has_unread_notif():
        notif = True
    else:
        notif = False
    subscrib_onme = Subscrib.objects.filter(to = request.user)
    my_subscribs = Subscrib.objects.filter(who = request.user)
    return render(request, 'messenger/chat_list.html', {'chat' : chat, 'profile': profile, 'notif':notif, 'subscrib_onme':subscrib_onme, 'my_subscribs':my_subscribs})

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
            message_context.update({'f_n':message.writer.first_name, 'l_n':message.writer.last_name, 'date':message.pub_date.strftime("%b. %d, %Y, %I:%M %p"), 'wr_id':message.writer.id, 'id':message.id})
            if message.text:
                message_context.update({'text':message.text})
            if message.is_grey(request.user):
                message_context.update({'grey':True})
            if message.image_box():
                imagelist = ''
                for im in message.image_box():
                    imagelist = imagelist + "<img src = '" + im.image_ultra.url +  "' style='width: 50px; height: 50px' class ='mini-images' name = '"+im.image.url+"'>" + " "
                message_context.update({'images':imagelist})
            context.update({i:message_context})
            i = i + 1
        return JsonResponse(context)


@login_required
def chat(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, id = chat_id)
        if chat.is_group_chat():
            this_is_chat = True
        else:
            this_is_chat = False
        profile = request.user.profile
        if profile.has_unread_notif():
            notif = True
        else:
            notif = False
        subscrib_onme = Subscrib.objects.filter(to = request.user)
        my_subscribs = Subscrib.objects.filter(who = request.user)
        form = MessageForm()
        form_im = ImageMessageForm()
        messages = Message.objects.filter(chat = chat)[:10][::-1]
        return render (request, 'messenger/chat.html', {'chat':chat, 'messages' : messages,'form' : form, 'form_im':form_im, 'notif': notif, 'profile':profile, 'subscrib_onme':subscrib_onme, 'my_subscribs':my_subscribs})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


@login_required
def create_chat(request):
    subscribs = Subscrib.objects.filter(who = request.user)
    profile = Profile.objects.get(user = request.user)
    if profile.has_unread_notif():
        notif = True
    else:
        notif = False
    subscrib_onme = Subscrib.objects.filter(to = request.user)
    my_subscribs = Subscrib.objects.filter(who = request.user)
    return render (request, 'messenger/create_chat.html', {'subscribs': subscribs, 'profile':profile, 'notif':notif, 'subscrib_onme':subscrib_onme, 'my_subscribs':my_subscribs})


@login_required
def add_member(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, id = chat_id)
        subscribs = Subscrib.objects.filter(who = request.user)
        potential_members = []
        for subscrib in subscribs:
            if not subscrib.to in chat.members():
                potential_members.append(subscrib)
        subscrib_onme = Subscrib.objects.filter(to = request.user)
        my_subscribs = Subscrib.objects.filter(who = request.user)
        profile = Profile.objects.get(user = request.user)
        if profile.has_unread_notif():
            notif = True
        else:
            notif = False
            return render (request, 'messenger/create_chat.html', {'subscribs': potential_members, 'profile':profile, 'notif':notif, 'subscrib_onme':subscrib_onme, 'my_subscribs':my_subscribs})


@login_required
def ajax_message(request, chat_id):
    chat = get_object_or_404(Chat, id = chat_id)
    if request.method == 'POST' and request.is_ajax:
        text = request.POST['text']
        images = request.FILES.getlist('image')
        if not bool(text and text.strip()) and not images:
            context = {'empty':True}
            return JsonResponse(context)
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
                context = {'text':message.text, 'f_name' : message.writer.first_name, 'l_name': message.writer.last_name, 'images': imagelist, 'id':message.id, 'wr_id':message.writer.id}
            else:
                context = {'text':message.text, 'f_name' : message.writer.first_name, 'l_name': message.writer.last_name, 'id':message.id, 'wr_id':message.writer.id}
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
                context = {'f_name' : message.writer.first_name, 'l_name': message.writer.last_name, 'images': imagelist, 'id':message.id, 'wr_id':message.writer.id}
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

@login_required
def ajax_add_member(request, chat_id):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        list_k = (list(dict_k)[0])
        users = []
        i = 0
        ids = list_k.split(',')
        chat = get_object_or_404(Chat, id = chat_id)
        for id in ids:
            user = get_object_or_404(User, id = int(id))
            profile = get_object_or_404(Profile, user = user)
            chat.member.add(user)
            profile.dialogues.add(chat)
        context = {'chat_id':chat.id}
        return JsonResponse(context)

@login_required
def ajax_change_chat_name(request, chat_id):
    if request.method == 'POST' and request.is_ajax:
        name = request.POST['name']
        if not bool(name and name.strip()):
            context = {'empty':True}
            return JsonResponse(context)
        else:
            chat = get_object_or_404(Chat, id = chat_id)
            chat.name = name
            chat.save()
            return JsonResponse({'name':chat.name})

@login_required
def ajax_change_chat_avatar(request, chat_id):
    if request.method == 'POST' and request.is_ajax:
        avatar = request.FILES.get('avatar')
        chat = get_object_or_404(Chat, id = chat_id)
        chat.pict = avatar
        chat.save()
        avatar_link = chat.chat_small_pict_url()
        return JsonResponse({'avatar':avatar_link})
