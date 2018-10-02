from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from profiles.models import Profile, Subscrib, Notification, Admittance
from posts.models import Post, Comment, ImagePost
import datetime
from datetime import timezone
from datetime import timedelta
import json
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from likes.models import Like
from django.http import JsonResponse
from messenger.models import Message, Chat, ImageMessage
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


def ajax_scroll_people(request):
    if request.is_ajax:
        dict_k = request.GET.keys()
        old_page = int((list(dict_k))[0])
        first_border = old_page*10
        second_border = first_border+10
        i = 0
        people = Profile.objects.all()[first_border:second_border]
        context = {}
        for profile in people:
            profile_context = {'f_n': profile.user.first_name, 'l_n': profile.user.last_name, 'followers' : profile.rating, 'link': "http://localhost:8000/" + str(profile.user.id),
                                'ava': "<img src = '"+str(profile.ultra_avatar_url())+"' class ='round-im-50'>"}
            if profile.user in request.user.profile.my_followers():
                profile_context.update({'follow_you':True})
            if profile.user in request.user.profile.my_following():
                profile_context.update({'you_follow':True})
            if profile.user == request.user:
                profile_context.update({'you':True})
            context.update({i:profile_context})
            i += 1
        return JsonResponse(context)

@login_required
def ajax_scroll_postresults(request):
    if request.is_ajax:
        q = (str(request.META['HTTP_REFERER'])).split('/search/?question=')[1]
        Q  = q.split(' ')
        dict_k = request.GET.keys()
        old_page = int((list(dict_k))[0])
        first_border = old_page*10
        second_border = first_border+10
        i = 0
        results = Post.objects.none()
        while i <len(Q):
            results = results|Post.objects.filter(text__icontains = Q[i])[first_border:second_border]
            i+=1
        context = {}
        c = 0
        for post in results:
            author_link = "http://localhost:8000/" + str(post.author.id)
            post_link = "http://localhost:8000/post/" + str(post.id)
            if post.author.profile.avatar:
                image = "<img src = " + post.author.profile.avatar_ultra.url + " class ='round-im-50'>"
            else:
                image = "<img src = '/static/images/default_ava.jpg' class ='round-im-50'>"
            post_context = {'post_link':post_link, 'id':post.id, 'f_n':post.author.first_name, 'l_n':post.author.last_name, 'avatar':image, 'link' : author_link, 'pub_date':post.pub_date.strftime("%b. %d, %Y, %I:%M %p"), 'l_q':post.likes_quanity, 'r_q':post.reposts_quanity, 'c_q': post.comments_quanity, 'id':post.id, 'text':post.text}
            if request.user in post.who_liked():
                post_context.update({'red':True})
            if post.author != request.user:
                post_context.update({'can_repost':True})
            else:
                post_context.update({'delete_cross':True})
            if post.all_comments():
                commentlist = ''
                for com in post.all_comments():
                    if com.is_to_comment():
                        link = "http://localhost:8000/" + str(com.answer_to.commentator.id)
                        commentlist = commentlist + "<li class='list-group-item one-comment-results' name ='"+ str(com.id) +"'>"+"<a href='http://localhost:8000/"+str(com.commentator.id)+"'><p class ='commentator-name'>" + com.commentator.first_name + " " + com.commentator.last_name + "</p></a><p><a href="+link + ">" +com.answer_to.commentator.first_name+ "</a>, "+com.text+"</p><p>"+str(com.com_date)+"</p></li>"
                    else:
                        commentlist = commentlist + "<li class='list-group-item one-comment-results' name ='"+ str(com.id) +"'>"+"<a href='http://localhost:8000/"+str(com.commentator.id)+"'><p class ='commentator-name'>" + com.commentator.first_name + " " + com.commentator.last_name + "</p></a><p>"+com.text+"</p><p>"+str(com.com_date)+"</p></li>"
                post_context.update({'comments':commentlist})
            if post.image_box():
                    imagelist = ''
                    for im in post.image_box():
                        imagelist = imagelist + "<a href=" + im.image.url + "><img src = '" + im.image_ultra.url +  "' style='width: 50px; height: 50px'></a>" + " "
                    post_context.update({'images':imagelist})
            context.update({c:post_context})
            c+=1
        return JsonResponse(context)

@login_required
def ajax_scroll_news(request):
    if request.is_ajax:
        dict_k = request.GET.keys()
        old_page = int((list(dict_k))[0])
        subscribs = Subscrib.objects.filter(who = request.user)
        users = []
        for s in subscribs:
            user = s.to
            users.append(user)
        users.append(request.user)
        first_border = old_page*10
        second_border = first_border+10
        posts = Post.objects.filter(author__in = users)[first_border:second_border]
        context = {}
        i = 0
        for post in posts:
            author_link = "http://localhost:8000/" + str(post.author.id)
            if post.author.profile.avatar:
                image = "<img src = " + post.author.profile.avatar_ultra.url + " class ='round-im-50'>"
            else:
                image = "<img src = '/static/images/default_ava.jpg' class ='round-im-50'>"
            if request.user in post.who_liked():
                you_liked = True
            else:
                you_liked = False
            if post.is_repost:
                repost = True
                post_link = "http://localhost:8000/post/" + str(post.repost.id)
                if post.repost.image_box():
                    imagelist = ''
                    for im in post.repost.image_box():
                        imagelist = imagelist + "<a href=" + im.image.url + "><img src = '" + im.image_ultra.url +  "' style='width: 50px; height: 50px'></a>" + " "
                    post_context = {'f_n' : post.author.first_name, 'l_n':post.author.last_name, 'date' : post.pub_date.strftime("%b. %d, %Y, %I:%M %p"), 'id':post.id,
                                    'avatar' : image, 'link' : author_link, 'repost' : repost, 'images' : imagelist, 'you_liked' :you_liked, 'l_q' : post.likes_quanity,
                                    'c_q':post.comments_quanity
                                    }
                else:
                    post_context = {'f_n' : post.author.first_name, 'l_n':post.author.last_name, 'date' : post.pub_date.strftime("%b. %d, %Y, %I:%M %p"), 'id':post.id,
                                    'avatar' : image, 'link' : author_link, 'repost' : repost, 'you_liked' :you_liked, 'l_q' : post.likes_quanity, 'c_q':post.comments_quanity
                                    }
                if post.repost.text:
                    post_context.update({'text':post.repost.text})
            else:
                repost = False
                post_link = "http://localhost:8000/post/" + str(post.id)
                if post.image_box():
                    imagelist = ''
                    for im in post.image_box():
                        imagelist = imagelist + "<a href=" + im.image.url + "><img src = '" + im.image_ultra.url +  "' style='width: 50px; height: 50px'></a>" + " "
                    post_context = {'f_n' : post.author.first_name, 'l_n':post.author.last_name, 'date' : post.pub_date.strftime("%b. %d, %Y, %I:%M %p"), 'id':post.id,
                                    'avatar' : image, 'link' : author_link, 'repost' : repost, 'images' : imagelist, 'you_liked' :you_liked, 'l_q' : post.likes_quanity,
                                    'c_q':post.comments_quanity
                                    }
                else:
                    post_context = {'f_n' : post.author.first_name, 'l_n':post.author.last_name, 'date' : post.pub_date.strftime("%b. %d, %Y, %I:%M %p"), 'id':post.id,
                                    'avatar' : image, 'link' : author_link, 'repost' : repost, 'you_liked' :you_liked, 'l_q' : post.likes_quanity,
                                    'c_q':post.comments_quanity
                                    }
                if post.text:
                    post_context.update({'text':post.text})
            if post.author != request.user:
                post_context.update({'repost_button':True})
            else:
                post_context.update({'delete_cross':True})
            if post.all_comments():
                commentlist = ''
                for com in post.all_comments():
                    if com.is_to_comment():
                        link = "http://localhost:8000/" + str(com.answer_to.commentator.id)
                        commentlist = commentlist + "<li class='list-group-item one-comment-news' name ='"+ str(com.id) +"'>"+"<a href='http://localhost:8000/"+str(com.commentator.id)+"'><p class ='commentator-name'>" + com.commentator.first_name + " " + com.commentator.last_name + "</p></a><p><a href="+link + ">" +com.answer_to.commentator.first_name+ "</a>, "+com.text+"</p><p>"+str(com.com_date)+"</p></li>"
                    else:
                        commentlist = commentlist + "<li class='list-group-item one-comment-news' name ='"+ str(com.id) +"'>"+"<a href='http://localhost:8000/"+str(com.commentator.id)+"'><p class ='commentator-name'>" + com.commentator.first_name + " " + com.commentator.last_name + "</p></a><p>"+com.text+"</p><p>"+str(com.com_date)+"</p></li>"
                post_context.update({'comments':commentlist})
            post_context.update({'r_q': post.reposts_quanity, 'post_link':post_link})
            context.update({i:post_context})
            i = i + 1
        return JsonResponse(context)

def ajax_scroll_wall(request, user_id):
    if request.is_ajax:
        dict_k = request.GET.keys()
        old_page = int((list(dict_k))[0])
        first_border = old_page*10
        second_border = first_border+10
        posts = Post.objects.filter(author = user_id)[first_border:second_border]
        context = {}
        i = 0
        for post in posts:
            post_context = {'pub_date':post.pub_date.strftime("%b. %d, %Y, %I:%M %p"), 'l_q':post.likes_quanity, 'r_q':post.reposts_quanity, 'c_q': post.comments_quanity, 'id':post.id}
            if post.text:
                post_context.update({'text':post.text})
            if post.image_box():
                imagelist = ''
                for im in post.image_box():
                    imagelist = imagelist + "<a href=" + im.image.url + "><img src = '" + im.image_ultra.url +  "' style='width: 50px; height: 50px'></a>" + " "
                post_context.update({'images':imagelist})
            if post.is_repost:
                author_link = "http://localhost:8000/" + str(post.repost.author.id)
                post_link = "http://localhost:8000/post/" + str(post.repost.id)
                post_context.update({'repost': True, 'author_link' : author_link, 'f_n':post.repost.author.first_name, 'l_n':post.repost.author.last_name})
            else:
                post_link = "http://localhost:8000/post/" + str(post.id)
            post_context.update({'post_link':post_link})
            if request.user == post.author:
                post_context.update({'your_post':True})
            if request.user in post.who_liked():
                post_context.update({'red':True})
            if post.all_comments():
                commentlist = ''
                for com in post.all_comments():
                    if com.is_to_comment():
                        link = "http://localhost:8000/" + str(com.answer_to.commentator.id)
                        commentlist = commentlist + "<li class='list-group-item one-comment' name ='"+ str(com.id) +"'>"+"<a href='http://localhost:8000/"+str(com.commentator.id)+"'><p class ='commentator-name'>" + com.commentator.first_name + " " + com.commentator.last_name + "</p></a><p><a href="+link + ">" +com.answer_to.commentator.first_name+ "</a>, "+com.text+"</p><p>"+str(com.com_date)+"</p></li>"
                    else:
                        commentlist = commentlist + "<li class='list-group-item one-comment' name ='"+ str(com.id) +"'>"+"<a href='http://localhost:8000/"+str(com.commentator.id)+"'><p class ='commentator-name'>" + com.commentator.first_name + " " + com.commentator.last_name + "</p></a><p>"+com.text+"</p><p>"+str(com.com_date)+"</p></li>"
                post_context.update({'comments':commentlist})
            context.update({i:post_context})
            i = i + 1
        return JsonResponse(context)

@login_required
def ajax_give_access(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        user = get_object_or_404(User, id= user_id)
        Admittance.objects.create(for_user = user, on_page = request.user)
        context = {'f': user.first_name, 'l': user.last_name}
        return JsonResponse(context)

@login_required
def ajax_black_book(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        user = get_object_or_404(User, id= user_id)
        admit = Admittance.objects.filter(for_user = user, on_page = request.user)
        if admit.exists():
            admit.delete()
            context = {'f': user.first_name, 'l': user.last_name}
            return JsonResponse(context)

@login_required
def ajax_posting(request, user_id):
    if request.method == 'POST' and request.is_ajax and user_id == request.user.id:
        author = get_object_or_404(User, id = request.user.id)
        text = request.POST['text']
        images = request.FILES.getlist('image')
        if text:
            if not bool(text and text.strip()) and not images:
                context = {'empty':True}
                return JsonResponse(context)
            post = Post.objects.create(
                    text = text,
                    author = author,
                    pub_date = datetime.datetime.now()
                    )
            if images:
                if len(images)>10:
                    context = {'too_much': True}
                    return JsonResponse(context)
            if images:
                imagelist = ''
                for image in images:
                    image = ImagePost.objects.create(
                        post = post,
                        image = image
                        )
                    imagelist = imagelist + "<img src = '" + image.image_ultra.url +  "' style='width: 50px; height: 50px'>" + " "
                context = {'text' : post.text, 'images': imagelist, 'id' : post.id, 'num_l': post.likes_quanity}
                return JsonResponse(context)
            else:
                context = {'text' : post.text, 'id' : post.id}
                return JsonResponse(context)
        else:
            if images:
                if len(images)>10:
                    context = {'too_much': True}
                    return JsonResponse(context)
                else:
                    post = Post.objects.create(
                                    author = author,
                                    pub_date = datetime.datetime.now()
                                    )
                    imagelist = ''
                    for image in images:
                        image = ImagePost.objects.create(
                            post = post,
                            image = image
                            )
                        imagelist = imagelist + "<img src = '" + image.image_ultra.url +  "' style='width: 50px; height: 50px'>" + " "
                    context = {'images': imagelist, 'id' : post.id, 'num_l': post.likes_quanity}
                    return JsonResponse(context)
            else:
                context = {'empty':True}
                return JsonResponse(context)




@login_required
def ajax_write(request, user_id):
    if request.method == "POST" and request.is_ajax:
        user = get_object_or_404(User, id = user_id)
        chats = Chat.objects.filter(member = user).filter(member = request.user)
        if chats.exists():
            for ch in chats:
                if ch.is_not_group_chat():
                    chat = ch
            if chat:
                text = request.POST['text']
                images = request.FILES.getlist('image')
                if text:
                    if not bool(text and text.strip()) and not images:
                        context = {'empty':True}
                        return JsonResponse(context)
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
                        for image in images:
                            image = ImageMessage.objects.create(
                                letter = message,
                                image = image
                                )
                        context = {'sent':True}
                    else:
                        context = {'sent':True}
                    return JsonResponse(context)
                else:
                    if images:
                        if len(images)>10:
                            context = {'too_much': True}
                            return JsonResponse(context)
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
                        context = {'sent':True}
                        return JsonResponse(context)
        else:
            chat = Chat.objects.create()
            chat.member.add(request.user)
            profile1 = get_object_or_404(Profile, user = request.user)
            profile1.dialogues.add(chat)
            chat.member.add(user)
            profile2 = get_object_or_404(Profile, user = user)
            profile2.dialogues.add(chat)
            text = request.POST['text']
            images = request.FILES.getlist('image')
            if text:
                if not bool(text and text.strip()) and not images:
                    context = {'empty':True}
                    return JsonResponse(context)
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
                    for image in images:
                        image = ImageMessage.objects.create(
                            letter = message,
                            image = image
                            )
                    context = {'sent':True}
                else:
                    context = {'sent':True}
                return JsonResponse(context)
            else:
                if images:
                    if len(images)>10:
                        context = {'too_much': True}
                        return JsonResponse(context)
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
                    context = {'sent':True}
                    return JsonResponse(context)

@login_required
def ajax_status(request, user_id):
    if request.method == 'POST' and request.is_ajax and user_id == request.user.id:
        profile = get_object_or_404(Profile, user = request.user)
        profile.status = request.POST.get('status-status')
        profile.save()
        key = make_template_fragment_key('first', [request.user.username])
        cache.delete(key)
        context = {'status' : profile.status}
        return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def ajax_like(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        post_id = (list(dict_k))[0]
        post = get_object_or_404(Post, id = post_id)
        owner_id = post.author.id
        if not post.user_can_likes(request.user):
            posttype = ContentType.objects.get_for_model(post)
            old_like = Like.objects.get(content_type__pk=posttype.id, object_id = post_id, liker = request.user)
            old_like.delete()
            post.likes_quanity = post.likes_quanity - 1
            post.save()
            notification = Notification.objects.filter(recipient = post.author, notificator = request.user, content_type__pk=posttype.id, object_id = post_id)
            if notification.exists():
                notification.delete()
            context = {'num_likes' : post.likes_quanity, 'post_id' : post_id}
            return JsonResponse (context)
        else:
            new_like = Like(content_object = post, liker = request.user)
            new_like.save()
            post.likes_quanity = post.likes_quanity + 1
            post.save()
            notification = Notification.objects.create(
                            recipient = post.author,
                            notificator = request.user,
                            time = datetime.datetime.now(),
                            text = 'liked your post',
                            about = 'Like',
                            content_object = post
                            )
            context = {'num_likes' : post.likes_quanity, 'post_id' : post_id}
            return JsonResponse (context)

@login_required
def ajax_like_post_detail(request, post_id):
    if request.method == 'POST' and request.is_ajax:
        post = get_object_or_404(Post, id = post_id)
        if not post.user_can_likes(request.user):
            posttype = ContentType.objects.get_for_model(post)
            old_like = Like.objects.get(content_type__pk=posttype.id, object_id = post_id, liker = request.user)
            old_like.delete()
            post.likes_quanity = post.likes_quanity - 1
            post.save()
            notification = Notification.objects.filter(recipient = post.author, notificator = request.user, content_type__pk=posttype.id, object_id = post_id)
            if notification.exists():
                notification.delete()
            context = {'num_likes' : post.likes_quanity}
            return JsonResponse (context)
        else:
            new_like = Like(content_object = post, liker = request.user)
            new_like.save()
            post.likes_quanity = post.likes_quanity + 1
            post.save()
            notification = Notification.objects.create(
                            recipient = post.author,
                            notificator = request.user,
                            time = datetime.datetime.now(),
                            text = 'liked your post',
                            about = 'Like',
                            content_object = post
                            )
            context = {'num_likes' : post.likes_quanity}
            return JsonResponse (context)

@login_required
def ajax_like_from_news(request):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        post_id = (list(dict_k))[0]
        post = get_object_or_404(Post, id = post_id)
        owner_id = post.author.id
        if not post.user_can_likes(request.user):
            if not post.user_can_likes(request.user):
                posttype = ContentType.objects.get_for_model(post)
                old_like = Like.objects.get(content_type__pk=posttype.id, object_id = post_id, liker = request.user)
                old_like.delete()
                post.likes_quanity = post.likes_quanity - 1
                post.save()
                notification = Notification.objects.filter(recipient = post.author, notificator = request.user, content_type__pk=posttype.id, object_id = post_id)
                if notification.exists():
                    notification.delete()
                context = {'num_likes' : post.likes_quanity, 'post_id' : post_id}
                return JsonResponse (context)
        else:
            new_like = Like(content_object = post, liker = request.user)
            new_like.save()
            post.likes_quanity = post.likes_quanity + 1
            post.save()
            notification = Notification.objects.create(
                            recipient = post.author,
                            notificator = request.user,
                            time = datetime.datetime.now(),
                            text = 'liked your post',
                            about = 'Like',
                            content_object = post
                            )
            context = {'num_likes' : post.likes_quanity, 'post_id' : post_id}
            return JsonResponse (context)

@login_required
def ajax_like_from_results(request):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        post_id = (list(dict_k))[0]
        post = get_object_or_404(Post, id = post_id)
        owner_id = post.author.id
        if not post.user_can_likes(request.user):
            if not post.user_can_likes(request.user):
                posttype = ContentType.objects.get_for_model(post)
                old_like = Like.objects.get(content_type__pk=posttype.id, object_id = post_id, liker = request.user)
                old_like.delete()
                post.likes_quanity = post.likes_quanity - 1
                post.save()
                notification = Notification.objects.filter(recipient = post.author, notificator = request.user, content_type__pk=posttype.id, object_id = post_id)
                if notification.exists():
                    notification.delete()
                context = {'num_likes' : post.likes_quanity, 'post_id' : post_id}
                return JsonResponse (context)
        else:
            new_like = Like(content_object = post, liker = request.user)
            new_like.save()
            post.likes_quanity = post.likes_quanity + 1
            post.save()
            notification = Notification.objects.create(
                            recipient = post.author,
                            notificator = request.user,
                            time = datetime.datetime.now(),
                            text = 'liked your post',
                            about = 'Like',
                            content_object = post
                            )
            context = {'num_likes' : post.likes_quanity, 'post_id' : post_id}
            return JsonResponse (context)


@login_required
def ajax_post_delete(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        post_id = (list(dict_k))[0]
        post = get_object_or_404(Post, id = post_id)
        if post.author == request.user:
            posttype = ContentType.objects.get_for_model(post)
            likes = Like.objects.filter(content_type__pk=posttype.id, object_id = post_id)
            notifications = Notification.objects.filter(content_type__pk=posttype.id, object_id = post_id)
            likes.delete()
            notifications.delete()
            if post.is_repost:
                post.repost.reposts_quanity-=1
                post.repost.save()
            post.delete()
            return HttpResponse()

@login_required
def ajax_post_delete_from_news(request):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        post_id = (list(dict_k))[0]
        post = get_object_or_404(Post, id = post_id)
        if post.author == request.user:
            posttype = ContentType.objects.get_for_model(post)
            likes = Like.objects.filter(content_type__pk=posttype.id, object_id = post_id)
            notifications = Notification.objects.filter(content_type__pk=posttype.id, object_id = post_id)
            likes.delete()
            notifications.delete()
            if post.is_repost:
                post.repost.reposts_quanity-=1
                post.repost.save()
            post.delete()
            return HttpResponse()

@login_required
def ajax_post_delete_from_results(request):
        dict_k = request.POST.keys()
        post_id = (list(dict_k))[0]
        post = get_object_or_404(Post, id = post_id)
        if post.author == request.user:
            posttype = ContentType.objects.get_for_model(post)
            likes = Like.objects.filter(content_type__pk=posttype.id, object_id = post_id)
            notifications = Notification.objects.filter(content_type__pk=posttype.id, object_id = post_id)
            likes.delete()
            notifications.delete()
            if post.is_repost:
                post.repost.reposts_quanity-=1
                post.repost.save()
            post.delete()
            return HttpResponse()

@login_required
def ajax_post_delete_from_detail(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if post.author == request.user:
        posttype = ContentType.objects.get_for_model(post)
        likes = Like.objects.filter(content_type__pk=posttype.id, object_id = post_id)
        notifications = Notification.objects.filter(content_type__pk=posttype.id, object_id = post_id)
        likes.delete()
        notifications.delete()
        if post.is_repost:
            post.repost.reposts_quanity-=1
            post.repost.save()
        post.delete()
        return HttpResponse()



@login_required
def ajax_repost(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        post_id = (list(dict_k))[0]
        post = get_object_or_404(Post, id = post_id)
        if not post.already_reposted(user = request.user):
            if post.is_repost:
                repost = Post.objects.create(
                        author = request.user,
                        repost = post.repost,
                        pub_date = datetime.datetime.now(),
                        is_repost = True
                        )
                post.repost.reposts_quanity = post.repost.reposts_quanity + 1
                post.save()
                notification = Notification.objects.create(
                                recipient = post.repost.author,
                                notificator = request.user,
                                time = datetime.datetime.now(),
                                text = 'shared your post',
                                about = 'Repost',
                                content_object = post.repost
                                )
                context = {'post_id' : post_id}
                return JsonResponse(context)
            else:
                repost = Post.objects.create(
                        author = request.user,
                        repost = post,
                        pub_date = datetime.datetime.now(),
                        is_repost = True
                        )
                post.reposts_quanity = post.reposts_quanity + 1
                post.save()
                notification = Notification.objects.create(
                                recipient = post.author,
                                notificator = request.user,
                                time = datetime.datetime.now(),
                                text = 'shared your post',
                                about = 'Repost',
                                content_object = post
                                )
                context = {'num_reposts' : post.reposts_quanity, 'post_id' : post_id}
                return JsonResponse(context)
        else:
            context = {'already_reposted' : True, 'post_id' : post_id}
            return JsonResponse(context)

@login_required
def ajax_repost_post_detail(request, post_id):
    if request.method == 'POST' and request.is_ajax:
        post = get_object_or_404(Post, id = post_id)
        if not post.already_reposted(user = request.user):
            if post.is_repost:
                repost = Post.objects.create(
                        author = request.user,
                        repost = post.repost,
                        pub_date = datetime.datetime.now(),
                        is_repost = True
                        )
                post.repost.reposts_quanity = post.repost.reposts_quanity + 1
                post.save()
                notification = Notification.objects.create(
                                recipient = post.repost.author,
                                notificator = request.user,
                                time = datetime.datetime.now(),
                                text = 'shared your post',
                                about = 'Repost',
                                content_object = post.repost
                                )
                return HttpResponse()
            else:
                repost = Post.objects.create(
                        author = request.user,
                        repost = post,
                        pub_date = datetime.datetime.now(),
                        is_repost = True
                        )
                post.reposts_quanity = post.reposts_quanity + 1
                post.save()
                notification = Notification.objects.create(
                                recipient = post.author,
                                notificator = request.user,
                                time = datetime.datetime.now(),
                                text = 'shared your post',
                                about = 'Repost',
                                content_object = post
                                )
                context = {'num_reposts' : post.reposts_quanity}
                return JsonResponse(context)
        else:
            context = {'already_reposted' : True}
            return JsonResponse(context)


@login_required
def ajax_repost_from_news(request):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        post_id = (list(dict_k))[0]
        post = get_object_or_404(Post, id = post_id)
        if not post.already_reposted(user = request.user):
            repost = Post.objects.create(
                    author = request.user,
                    repost = post,
                    pub_date = datetime.datetime.now(),
                    is_repost = True
                    )
            post.reposts_quanity = post.reposts_quanity + 1
            post.save()
            notification = Notification.objects.create(
                            recipient = post.author,
                            notificator = request.user,
                            time = datetime.datetime.now(),
                            text = 'shared your post',
                            about = 'Repost',
                            content_object = post
                            )
            context = {'num_reposts' : post.reposts_quanity, 'post_id' : post_id}
            return JsonResponse(context)
        else:
            context = {'already_reposted' : True, 'post_id' : post_id}
            return JsonResponse(context)

@login_required
def ajax_repost_from_results(request):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        post_id = (list(dict_k))[0]
        post = get_object_or_404(Post, id = post_id)
        if not post.already_reposted(user = request.user):
            repost = Post.objects.create(
                    author = request.user,
                    repost = post,
                    pub_date = datetime.datetime.now(),
                    is_repost = True
                    )
            post.reposts_quanity = post.reposts_quanity + 1
            post.save()
            notification = Notification.objects.create(
                            recipient = post.author,
                            notificator = request.user,
                            time = datetime.datetime.now(),
                            text = 'shared your post',
                            about = 'Repost',
                            content_object = post
                            )
            context = {'num_reposts' : post.reposts_quanity, 'post_id' : post_id}
            return JsonResponse(context)
        else:
            context = {'already_reposted' : True, 'post_id' : post_id}
            return JsonResponse(context)

@login_required
def ajax_simple_subscribe(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        first_user = request.user
        second_user = get_object_or_404(User, id = user_id)
        subscrib = Subscrib.objects.filter(
                    who = first_user,
                    to = second_user,
                    )
        if not subscrib.exists():
            subscrib = Subscrib.objects.create(
                        who = first_user,
                        to = second_user,
                        subs_date = datetime.datetime.now(),
                        )
            subscrib.to.profile.plus_popularity()
            notification = Notification.objects.create(
                        recipient = second_user,
                        notificator = first_user,
                        time = datetime.datetime.now(),
                        text = 'subscribed to your updates',
                        about = 'Subscribe'
                        )
            if first_user.profile.is_closed:
                admit = Admittance.objects.create(for_user = second_user, on_page = first_user)
            key = make_template_fragment_key('third', [request.user.username])
            cache.delete(key)
            key = make_template_fragment_key('third', [second_user.username])
            cache.delete(key)
            context = {'first_name' : second_user.first_name, 'last_name' : second_user.last_name}
            return JsonResponse(context)

@login_required
def ajax_simple_unsubscribe(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        first_user = request.user
        second_user = get_object_or_404(User, id = user_id)
        subscrib = Subscrib.objects.get(
                    who = first_user,
                    to = second_user,
                    )
        subscrib.to.profile.minus_popularity()
        subscrib.delete()
        key = make_template_fragment_key('third', [request.user.username])
        cache.delete(key)
        key = make_template_fragment_key('third', [second_user.username])
        cache.delete(key)
        context = {'first_name' : second_user.first_name, 'last_name' : second_user.last_name}
        return JsonResponse(context)

@login_required
def ajax_notif_update(request):
    if request.method == 'POST' and request.is_ajax:
        user = request.user
        notifications = Notification.objects.filter(recipient = user)
        for notification in notifications:
            notification.status = 'Read'
            notification.save()
        return HttpResponse()

@login_required
def ajax_comment(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        text = request.POST.get('comment-text')
        if not bool(text and text.strip()):
            context = {'empty':True}
            return JsonResponse(context)
        post = get_object_or_404(Post, id = request.POST.get('id'))
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = text,
                    com_date = datetime.datetime.now(),
                    post = post)
        post.comments_quanity = post.comments_quanity + 1
        post.save()
        notification = Notification.objects.create(
                        recipient = post.author,
                        notificator = request.user,
                        time = datetime.datetime.now(),
                        text = 'commented your post',
                        about = 'PostComment',
                        content_object = post
                        )
        context = {'num' : post.comments_quanity, 'id' : post.id, 'text' : comment.text,
                    'f_n': comment.commentator.first_name, 'l_n': comment.commentator.last_name, 'com_id':comment.id}
        return JsonResponse(context)

@login_required
def ajax_comment_from_news(request):
    if request.method == 'POST' and request.is_ajax:
        text = request.POST.get('comment-text')
        if not bool(text and text.strip()):
            context = {'empty':True}
            return JsonResponse(context)
        post = get_object_or_404(Post, id = request.POST.get('id'))
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = text,
                    com_date = datetime.datetime.now(),
                    post = post)
        post.comments_quanity = post.comments_quanity + 1
        post.save()
        notification = Notification.objects.create(
                        recipient = post.author,
                        notificator = request.user,
                        time = datetime.datetime.now(),
                        text = 'commented your post',
                        about = 'PostComment',
                        content_object = post
                        )
        context = {'num' : post.comments_quanity, 'id' : post.id, 'text' : comment.text,
                    'f_n': comment.commentator.first_name, 'l_n': comment.commentator.last_name}
        return JsonResponse(context)

@login_required
def ajax_comment_from_results(request):
    if request.method == 'POST' and request.is_ajax:
        text = request.POST.get('comment-text')
        if not bool(text and text.strip()):
            context = {'empty':True}
            return JsonResponse(context)
        post = get_object_or_404(Post, id = request.POST.get('id'))
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = text,
                    com_date = datetime.datetime.now(),
                    post = post)
        post.comments_quanity = post.comments_quanity + 1
        post.save()
        notification = Notification.objects.create(
                        recipient = post.author,
                        notificator = request.user,
                        time = datetime.datetime.now(),
                        text = 'commented your post',
                        about = 'PostComment',
                        content_object = post
                        )
        context = {'num' : post.comments_quanity, 'id' : post.id, 'text' : comment.text,
                    'f_n': comment.commentator.first_name, 'l_n': comment.commentator.last_name}
        return JsonResponse(context)


@login_required
def ajax_comment_comment(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        elder_comment = get_object_or_404(Comment, id = request.POST.get('id2'))
        raw_text = request.POST.get('comment-text')
        splitter = str(elder_comment.commentator.first_name) + ","
        if raw_text.startswith(splitter):
            splitted_text = raw_text.split(splitter)
            if len(splitted_text) > 2:
                text = ''.join(splitted_text[1:])
            else:
                text = splitted_text[1].strip()
        else:
            text = raw_text
        if not bool(text and text.strip()):
            context = {'empty':True}
            return JsonResponse(context)
        post = elder_comment.post
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = text,
                    com_date = datetime.datetime.now(),
                    post = post,
                    answer_to = elder_comment)
        post.comments_quanity = post.comments_quanity + 1
        post.save()
        notification = Notification.objects.create(
                        recipient = elder_comment.commentator,
                        notificator = request.user,
                        time = datetime.datetime.now(),
                        text = 'answered your comment',
                        about = 'CommentComment',
                        content_object = elder_comment
                        )
        context = {'num' : post.comments_quanity, 'text' : comment.text, 'f_n': comment.commentator.first_name, 'l_n': comment.commentator.last_name,
                        'who' : elder_comment.commentator.first_name, 'man_id' : elder_comment.commentator.id, 'com_id': elder_comment.id}
        return JsonResponse(context)

@login_required
def ajax_comment_comment_from_news(request):
    if request.method == 'POST' and request.is_ajax:
        elder_comment = get_object_or_404(Comment, id = request.POST.get('id2'))
        raw_text = request.POST.get('comment-text')
        splitter = str(elder_comment.commentator.first_name) + ","
        if raw_text.startswith(splitter):
            splitted_text = raw_text.split(splitter)
            if len(splitted_text) > 2:
                text = ''.join(splitted_text[1:])
            else:
                text = splitted_text[1].strip()
        else:
            text = raw_text
        if not bool(text and text.strip()):
            context = {'empty':True}
            return JsonResponse(context)
        post = elder_comment.post
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = text,
                    com_date = datetime.datetime.now(),
                    post = post,
                    answer_to = elder_comment)
        post.comments_quanity = post.comments_quanity + 1
        post.save()
        notification = Notification.objects.create(
                        recipient = elder_comment.commentator,
                        notificator = request.user,
                        time = datetime.datetime.now(),
                        text = 'answered your comment',
                        about = 'CommentComment',
                        content_object = elder_comment
                        )
        context = {'num' : post.comments_quanity, 'text' : comment.text, 'f_n': comment.commentator.first_name, 'l_n': comment.commentator.last_name,
                        'who' : elder_comment.commentator.first_name, 'man_id' : elder_comment.commentator.id, 'com_id': elder_comment.id}
        return JsonResponse(context)

@login_required
def ajax_comment_comment_from_results(request):
    if request.method == 'POST' and request.is_ajax:
        elder_comment = get_object_or_404(Comment, id = request.POST.get('id2'))
        raw_text = request.POST.get('comment-text')
        splitter = str(elder_comment.commentator.first_name) + ","
        if raw_text.startswith(splitter):
            splitted_text = raw_text.split(splitter)
            if len(splitted_text) > 2:
                text = ''.join(splitted_text[1:])
            else:
                text = splitted_text[1].strip()
        else:
            text = raw_text
        if not bool(text and text.strip()):
            context = {'empty':True}
            return JsonResponse(context)
        post = elder_comment.post
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = text,
                    com_date = datetime.datetime.now(),
                    post = post,
                    answer_to = elder_comment)
        post.comments_quanity = post.comments_quanity + 1
        post.save()
        notification = Notification.objects.create(
                        recipient = elder_comment.commentator,
                        notificator = request.user,
                        time = datetime.datetime.now(),
                        text = 'answered your comment',
                        about = 'CommentComment',
                        content_object = elder_comment
                        )
        context = {'num' : post.comments_quanity, 'text' : comment.text, 'f_n': comment.commentator.first_name, 'l_n': comment.commentator.last_name,
                        'who' : elder_comment.commentator.first_name, 'man_id' : elder_comment.commentator.id, 'com_id': elder_comment.id}
        return JsonResponse(context)

@login_required
def ajax_comment_from_detail(request, post_id):
    if request.method == 'POST' and request.is_ajax:
        text = request.POST.get('comment-text')
        if not bool(text and text.strip()):
            context = {'empty':True}
            return JsonResponse(context)
        post = get_object_or_404(Post, id = post_id)
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = text,
                    com_date = datetime.datetime.now(),
                    post = post)
        post.comments_quanity = post.comments_quanity + 1
        post.save()
        notification = Notification.objects.create(
                        recipient = post.author,
                        notificator = request.user,
                        time = datetime.datetime.now(),
                        text = 'commented your post',
                        about = 'PostComment',
                        content_object = post
                        )
        context = {'num' : post.comments_quanity, 'text' : comment.text,
                    'f_n': comment.commentator.first_name, 'l_n': comment.commentator.last_name, 'my_id' : comment.commentator.id, 'com_id': comment.id}
        return JsonResponse(context)

@login_required
def ajax_comment_comment_from_detail(request, post_id):
    if request.method == 'POST' and request.is_ajax:
        raw_text = str(request.POST.get('comment-text'))
        if not bool(raw_text and raw_text.strip()):
            context = {'empty':True}
            return JsonResponse(context)
        id_to = int(request.POST.get('id_to'));
        user_to = get_object_or_404(User, id =id_to)
        splitter = str(user_to.first_name) + ","
        if raw_text.startswith(splitter):
            splitted_text = raw_text.split(splitter)
            if len(splitted_text) > 2:
                text = ''.join(splitted_text[1:])
            else:
                text = splitted_text[1].strip()
            if not bool(text and text.strip()):
                context = {'empty':True}
                return JsonResponse(context)
        post = get_object_or_404(Post, id = post_id)
        elder_comment = get_object_or_404(Comment, id = request.POST.get('id_com'))
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = text,
                    com_date = datetime.datetime.now(),
                    post = post,
                    answer_to = elder_comment)
        post.comments_quanity = post.comments_quanity + 1
        post.save()
        notification = Notification.objects.create(
                        recipient = elder_comment.commentator,
                        notificator = request.user,
                        time = datetime.datetime.now(),
                        text = 'answered your comment',
                        about = 'CommentComment',
                        content_object = elder_comment
                        )
        context = {'num' : post.comments_quanity, 'text' : comment.text, 'f_n': comment.commentator.first_name, 'l_n': comment.commentator.last_name,
                        'who' : elder_comment.commentator.first_name, 'my_id' : comment.commentator.id, 'com_id': comment.id, 'man_id' : elder_comment.commentator.id}
        return JsonResponse(context)
