from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.models import Profile, Subscrib, Notification, Admittance, Alert
from posts.models import Post, Comment, ImagePost
from profiles.forms import RegistrationForm, ProfileForm, AvatarForm, StatusForm, ChangeEmailForm
import datetime
from datetime import timezone
from datetime import timedelta
from posts.forms import PostForm, CommentForm, CommentCommentForm
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from likes.models import Like
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from messenger.forms import MessageForm, ImageMessageForm
from messenger.models import Message, Chat, ImageMessage
from django.contrib.auth.views import PasswordContextMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode



UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


@login_required
def news(request):
    profile = get_object_or_404(Profile, user = request.user)
    subscribs = Subscrib.objects.filter(who = request.user)
    form_st = StatusForm(prefix = 'status')
    form_com = CommentForm(prefix = 'comment')
    form_c_c = CommentCommentForm(prefix = 'com_com')
    subscrib = Subscrib.objects.filter(who = request.user)
    subscrib_onme = Subscrib.objects.filter(to = request.user)
    if profile.has_unread_notif():
        notif = True
    else:
        notif = False
    i = 0
    for d in profile.dialogues.all():
        if d.has_unread_messages(request.user):
            i = i+1
    if i >0:
        unread = True
    else:
        unread = False
    users = []
    for s in subscribs:
        user = s.to
        users.append(user)
    users.append(request.user)
    news_posts = Post.objects.filter(author__in = users)[:10]
    context = {'news_posts' : news_posts, 'profile':profile, 'form_st' : form_st, 'notif': notif, 'unread' : unread,
                'form_com' : form_com, 'form_c_c':form_c_c, 'subscrib' : subscrib, 'subscrib_onme':subscrib_onme}
    return render (request, 'root/news.html', context)

@login_required
def ajax_scroll_news(request):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
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
                if post.repost.image_box():
                    imagelist = ''
                    for im in post.repost.image_box():
                        imagelist = imagelist + "<a href=" + im.image.url + "><img src = '" + im.image_ultra.url +  "' style='width: 50px; height: 50px'></a>" + " "
                    post_context = {'text' : post.repost.text, 'f_n' : post.author.first_name, 'l_n':post.author.last_name, 'date' : post.pub_date, 'id':post.id,
                                    'avatar' : image, 'link' : author_link, 'repost' : repost, 'images' : imagelist, 'you_liked' :you_liked, 'l_q' : post.likes_quanity,
                                    'c_q':post.comments_quanity
                                    }
                else:
                    post_context = {'text' : post.text, 'f_n' : post.author.first_name, 'l_n':post.author.last_name, 'date' : post.pub_date, 'id':post.id,
                                    'avatar' : image, 'link' : author_link, 'repost' : repost, 'you_liked' :you_liked, 'l_q' : post.likes_quanity, 'c_q':post.comments_quanity
                                    }
            else:
                repost = False
                if post.image_box():
                    imagelist = ''
                    for im in post.image_box():
                        imagelist = imagelist + "<a href=" + im.image.url + "><img src = '" + im.image_ultra.url +  "' style='width: 50px; height: 50px'></a>" + " "
                    post_context = {'text' : post.text, 'f_n' : post.author.first_name, 'l_n':post.author.last_name, 'date' : post.pub_date, 'id':post.id,
                                    'avatar' : image, 'link' : author_link, 'repost' : repost, 'images' : imagelist, 'you_liked' :you_liked, 'l_q' : post.likes_quanity,
                                    'c_q':post.comments_quanity
                                    }
                else:
                    post_context = {'text' : post.text, 'f_n' : post.author.first_name, 'l_n':post.author.last_name, 'date' : post.pub_date, 'id':post.id,
                                    'avatar' : image, 'link' : author_link, 'repost' : repost, 'you_liked' :you_liked, 'l_q' : post.likes_quanity,
                                    'c_q':post.comments_quanity
                                    }
            if post.author != request.user:
                post_context.update({'repost_button':True})
            else:
                post_context.update({'delete_cross':True})
            if post.all_comments():
                commentlist = ''
                for com in post.all_comments():
                    if com.is_to_comment():
                        link = "http://localhost:8000/" + str(com.answer_to.commentator.id)
                        commentlist = commentlist + "<li class='list-group-item one-comment' name ='"+ str(com.id) +"'>"+"<p>" + com.commentator.first_name + " " + com.commentator.last_name + "</p><p><a href="+link + ">" +com.answer_to.commentator.first_name+ "</a>, "+com.text+"</p><p>"+str(com.com_date)+"</p></li>"
                    else:
                        commentlist = commentlist + "<li class='list-group-item one-comment' name ='"+ str(com.id) +"'>"+"<p>" + com.commentator.first_name + " " + com.commentator.last_name + "</p><p>"+com.text+"</p><p>"+str(com.com_date)+"</p></li>"
                post_context.update({'comments':commentlist})
            post_context.update({'r_q': post.reposts_quanity})
            context.update({i:post_context})
            i = i + 1
        return JsonResponse(context)

def wall(request, user_id):
    profile = get_object_or_404(Profile, user = user_id)
    if request.user.profile.has_access(profile.user):
        posts = Post.objects.filter(author = user_id)[:10]
        taboo = False
        if request.user.profile.is_closed:
            black = True
        else:
            black = False
    else:
        taboo = True
        post = False
        black = False
    subscrib = Subscrib.objects.filter(who = user_id)
    subscrib_onme = Subscrib.objects.filter(to = user_id)
    form_com = CommentForm(prefix = 'comment')
    form_c_c = CommentCommentForm(prefix = 'com_com')
    if user_id == request.user.id:
        i = 0
        for d in profile.dialogues.all():
            if d.has_unread_messages(request.user):
                i = i+1
        if i >0:
            unread = True
        else:
            unread = False
        form = PostForm()
        form_st = StatusForm(prefix = 'status')
        if profile.has_unread_notif():
            notif = True
        else:
            notif = False
        context = {'post' : posts, 'form' : form, 'profile' : profile, 'subscrib' : subscrib, 'form_st' : form_st, 'unread' : unread,
                    'notif': notif, 'form_com' : form_com, 'form_c_c':form_c_c, 'subscrib_onme':subscrib_onme, 'taboo' : taboo}
    else:
        if profile.is_follower(request.user):
            fol = True
        else:
            fol = False
        form_mes = MessageForm()
        form_im = ImageMessageForm()
        curr_subscrib = Subscrib.objects.filter(who = request.user, to = profile.user)
        if curr_subscrib.exists():
            context = {'post' : posts, 'profile' : profile, 'subscrib' : subscrib, 'you_subscribed' : True, 'form_com' : form_com,
                        'form_c_c':form_c_c, 'subscrib_onme':subscrib_onme, 'form_mes' : form_mes, 'form_im':form_im, 'taboo' : taboo, 'fol':fol, 'black':black}
        else:
            context = {'post' : posts, 'profile' : profile, 'subscrib' : subscrib, 'you_subscribed' : False, 'form_com' : form_com,
                        'form_c_c':form_c_c, 'subscrib_onme':subscrib_onme, 'form_mes' : form_mes, 'form_im':form_im, 'taboo' : taboo, 'fol':fol, 'black':black}
    return render(request, 'root/wall.html', context)


def ajax_scroll_wall(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        dict_k = request.POST.keys()
        old_page = int((list(dict_k))[0])
        first_border = old_page*10
        second_border = first_border+10
        posts = Post.objects.filter(author = user_id)[first_border:second_border]
        context = {}
        i = 0
        for post in posts:
            post_context = {'pub_date':post.pub_date, 'l_q':post.likes_quanity, 'r_q':post.reposts_quanity, 'c_q': post.comments_quanity, 'id':post.id}
            if post.text:
                post_context.update({'text':post.text})
            if post.image_box():
                imagelist = ''
                for im in post.image_box():
                    imagelist = imagelist + "<a href=" + im.image.url + "><img src = '" + im.image_ultra.url +  "' style='width: 50px; height: 50px'></a>" + " "
                post_context.update({'images':imagelist})
            if post.is_repost:
                author_link = "http://localhost:8000/" + str(post.repost.author.id)
                post_context.update({'repost': True, 'author_link' : author_link, 'f_n':post.repost.author.first_name, 'l_n':post.repost.author.last_name})
            if request.user == post.author:
                post_context.update({'your_post':True})
            if request.user in post.who_liked():
                post_context.update({'red':True})
            if post.all_comments():
                commentlist = ''
                for com in post.all_comments():
                    if com.is_to_comment():
                        link = "http://localhost:8000/" + str(com.answer_to.commentator.id)
                        commentlist = commentlist + "<li class='list-group-item one-comment' name ='"+ str(com.id) +"'>"+"<p>" + com.commentator.first_name + " " + com.commentator.last_name + "</p><p><a href="+link + ">" +com.answer_to.commentator.first_name+ "</a>, "+com.text+"</p><p>"+str(com.com_date)+"</p></li>"
                    else:
                        commentlist = commentlist + "<li class='list-group-item one-comment' name ='"+ str(com.id) +"'>"+"<p>" + com.commentator.first_name + " " + com.commentator.last_name + "</p><p>"+com.text+"</p><p>"+str(com.com_date)+"</p></li>"
                post_context.update({'comments':commentlist})
            context.update({i:post_context})
            i = i + 1
        return JsonResponse(context)


@login_required
def delete_user_action(request):
    user = request.user
    user.delete()
    return redirect('login')

@login_required
def delete_user_confirm(request):
    return render(request, 'profiles/delete_user_confirm.html')

class MyPasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = ('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
            alert = Alert.objects.filter(user = user)
            alert.delete()
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context



def search(request):
    q1 = request.GET.get('question')
    Q  = q1.split(' ')
    if Q == ['']:
        return redirect('mywall')
    i = 0
    results = Post.objects.none()
    while i <len(Q):
        results = results|Post.objects.filter(text__icontains = Q[i])
        i+=1
    context = {'results':results}
    return render(request, 'root/search_results.html', context)

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user = request.user)
    if request.method == 'POST':
        form_em = ChangeEmailForm(request.POST)
        print(request.POST.get('email'))
        if request.POST.get('email') == '':
            print('null')
            if request.POST.get('private') == 'close-it':
                print('close')
                profile.is_closed = True
                profile.save()
            elif request.POST.get('private') == 'open-it':
                print('open')
                profile.is_closed = False
                profile.save()
        else:
            if  form_em.is_valid():
                profile.user.email = form_em.cleaned_data['email']
                profile.user.save()
            else:
                context = {'profile' : profile, 'form_em':form_em}
                return render(request, 'profiles/edit_profile.html', context)
        if request.POST.get('private') == 'close-it':
            print('close')
            profile.is_closed = True
            profile.save()
        elif request.POST.get('private') == 'open-it':
            print('open')
            profile.is_closed = False
            profile.save()
    form_em = ChangeEmailForm()
    context = {'profile' : profile, 'form_em':form_em}
    return render(request, 'profiles/edit_profile.html', context)

def first_page(request):
    if request.user.is_authenticated:
        return redirect('news')
    else:
        return redirect ('login')

def e_handler404(request):
    return render (request, '404.html')

def e_handler500(request):
    return render (request, '500.html')


def mywall(request):
    if request.user.is_authenticated:
        my_id = request.user.id
        return redirect('wall', my_id)
    else:
        return redirect ('login')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username = username)
        if user.exists():
            alerts = Alert.objects.filter(user = user[0])
            if len(alerts)<3:
                user = authenticate(request, username = username, password = password)
                if user is not None:
                    alert = Alert.objects.filter(user = user)
                    alert.delete()
                    login(request, user)
                    profile = Profile.objects.filter(user = request.user)
                    if profile:
                        return redirect('wall', user.id)
                    else:
                        return redirect('create_profile')
                else:
                    user = User.objects.filter(username = username)
                    if user.exists():
                        Alert.objects.create(user = user[0])
                        messages.error(request, 'Wrong username or password', extra_tags='alert alert-success alert-dismissible fade-show')
            else:
                alert = "Somebody tried to get your account with wrong password. We'll send you the mail to recet password"
                context = {'alert' : alert}
                return redirect ('password_reset')
        return render(request, 'login.html')
    return render(request, 'login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect ('login')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username = username, email = email, password = password, first_name = first_name, last_name = last_name)
            messages.success(request, 'Thanks for registration', extra_tags='alert alert-success alert-dismissible fade-show')
            return redirect('login')
        else:
            form = RegistrationForm()
            return render (request, 'registration.html', {'form' : form})
    else:
        form = RegistrationForm()
        return render (request, 'registration.html', {'form' : form})


@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            new_profile = form.save(commit = False)
            new_profile.user = request.user
            new_profile.registrated = datetime.datetime.now()
            new_profile.save()
            profile_id = new_profile.user.id
            messages.success(request, 'Your profile is created!', extra_tags='alert alert-success alert-dismissible fade-show')
            return redirect ('wall', profile_id)
        else:
            form = ProfileForm()
            return render(request, 'profiles/create_profile.html', {'form':form})
    else:
        form = ProfileForm()
        return render(request, 'profiles/create_profile.html', {'form':form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was changed!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/change_password.html', {'form': form})


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
            post = Post.objects.create(
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
                context = {'images': imagelist, 'id' : post.id, 'num_l': post.likes_quanity}
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
def liked_objects(request):
    like = Like.objects.filter(liker = request.user).order_by('-when')
    profile = get_object_or_404(Profile, user = request.user)
    return render(request, 'root/liked.html', {'like' : like, 'profile' : profile})



@login_required
def ajax_status(request, user_id):
    if request.method == 'POST' and request.is_ajax and user_id == request.user.id:
        profile = get_object_or_404(Profile, user = request.user)
        profile.status = request.POST.get('status-status')
        profile.save()
        context = {'status' : profile.status}
        return HttpResponse(json.dumps(context), content_type='application/json')


@login_required
def ajax_status_from_news(request):
    if request.method == 'POST' and request.is_ajax:
        profile = get_object_or_404(Profile, user = request.user)
        profile.status = request.POST.get('status-status')
        profile.save()
        context = {'status' : profile.status}
        return JsonResponse(context)

@login_required
def ajax_like(request, user_id):
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
                return HttpResponse (json.dumps(context), content_type='application/json')
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
            post.delete()
            return HttpResponse('done')

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
            post.delete()
            return HttpResponse('done')

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
            posttype = ContentType.objects.get_for_model(post)
            repost = Post.objects.get(author = request.user, repost = post)
            repost.delete()
            post.reposts_quanity = post.reposts_quanity - 1
            post.save()
            notification = Notification.objects.filter(recipient = post.author, notificator = request.user, content_type__pk=posttype.id, object_id = post_id)
            if notification.exists():
                notification.delete()
            context = {'num_reposts' : post.reposts_quanity, 'post_id' : post_id}
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
            notification = Notification.objects.create(
                        recipient = second_user,
                        notificator = first_user,
                        time = datetime.datetime.now(),
                        text = 'subscribed to your updates',
                        about = 'Subscribe'
                        )
            if first_user.profile.is_closed:
                admit = Admittance.objects.create(for_user = second_user, on_page = first_user)
            context = {'first_name' : second_user.first_name, 'last_name' : second_user.last_name}
            return JsonResponse(context)

@login_required
def ajax_simple_unsubscribe(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        first_user = request.user
        second_user = get_object_or_404(User, id = user_id)
        subscrib = Subscrib.objects.filter(
                    who = first_user,
                    to = second_user,
                    )
        subscrib.delete()
        context = {'first_name' : second_user.first_name, 'last_name' : second_user.last_name}
        return JsonResponse(context)

@login_required
def avatarize(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.user.id
            profile = get_object_or_404(Profile, user = request.user)
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            messages.success(request, 'Your avatar was updated!', extra_tags='alert alert-success alert-dismissible fade-show')
            return redirect ('wall', user_id)
        else:
            form = AvatarForm()
            return render(request, 'profiles/avatarize.html', {'form' : form})
    else:
        form = AvatarForm()
        return render(request, 'profiles/avatarize.html', {'form' : form})

@login_required
def notifications(request):
    user = request.user
    profile = get_object_or_404(Profile, user = user)
    notification = Notification.objects.filter(recipient = user)
    for n in notification:
        if n.is_older_than_day() and n.status == 'Read':
            n.delete()
    notification = Notification.objects.filter(recipient = user)
    return render(request, 'root/notifications.html', {'notification' : notification, 'profile' : profile})

@login_required
def ajax_notif_update(request):
    if request.method == 'POST' and request.is_ajax:
        user = request.user
        notifications = Notification.objects.filter(recipient = user)
        for notification in notifications:
            notification.status = 'Read'
            notification.save()
        return HttpResponse('Done')

@login_required
def ajax_comment(request, user_id):
    if request.method == 'POST' and request.is_ajax:
        post = get_object_or_404(Post, id = request.POST.get('id'))
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = request.POST.get('comment-text'),
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
def ajax_comment_from_news(request):
    if request.method == 'POST' and request.is_ajax:
        post = get_object_or_404(Post, id = request.POST.get('id'))
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = request.POST.get('comment-text'),
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
        post = elder_comment.post
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = request.POST.get('com_com-text'),
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
        post = elder_comment.post
        comment = Comment.objects.create(
                    commentator = request.user,
                    text = request.POST.get('com_com-text'),
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
