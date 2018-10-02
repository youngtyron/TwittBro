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
from posts.forms import PostForm, CommentForm
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
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

class OnePostView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'root/one_post.html'
    pk_url_kwarg = 'post_id'


    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            obj = 'object not exists'
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object == 'object not exists':
            return redirect ('news')
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user in self.object.who_liked():
            context['red'] =  True
        profile = get_object_or_404(Profile, user = self.request.user)
        context['profile'] = profile
        i = 0
        for d in profile.dialogues.all():
            if d.has_unread_messages(self.request.user):
                i = i+1
        if i >0:
            context['unread'] = True
        else:
            context['unread'] = False
        if profile.has_unread_notif():
            context['notif'] = True
        else:
            context['notif'] = False
        context['subscrib_onme'] = Subscrib.objects.filter(to = self.request.user)
        context['my_subscribs'] = Subscrib.objects.filter(who = self.request.user)
        context['form_com'] = CommentForm(prefix = 'comment')
        return context


class PeopleListView(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = 'people'
    template_name = 'root/people.html'

    def get_queryset(self):
        name = self.request.GET.get('name')
        if name != None:
            N  = name.split(' ')
            if N == ['']:
                return Profile.objects.all()[:10]
            i = 0
            results = []
            while i <len(N):
                users = User.objects.filter(first_name__icontains = N[i]) | User.objects.filter(last_name__icontains = N[i])
                print(users)
                for u in users:
                    results.append(u.profile)
                i+=1
            return results
        else:
            return Profile.objects.all()[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user = self.request.user)
        context['profile'] = profile
        if profile.has_unread_notif():
            notif = True
        else:
            notif = False
        context['notif'] = notif
        subscrib_onme = Subscrib.objects.filter(to = self.request.user)
        my_subscribs = Subscrib.objects.filter(who = self.request.user)
        context['subscrib_onme'] = subscrib_onme
        context['my_subscribs'] = my_subscribs
        i = 0
        for d in profile.dialogues.all():
            if d.has_unread_messages(self.request.user):
                i = i+1
        if i >0:
            unread = True
        else:
            unread = False
        context['unread'] = unread
        return context

@login_required
def search(request):
    q1 = request.GET.get('question')
    Q  = q1.split(' ')
    if Q == ['']:
        return redirect('mywall')
    i = 0
    results = Post.objects.none()
    while i <len(Q):
        results = results|Post.objects.filter(text__icontains = Q[i])[:10]
        i+=1
    profile = Profile.objects.get(user = request.user)
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
    subscrib_onme = Subscrib.objects.filter(to = request.user)
    my_subscribs = Subscrib.objects.filter(who = request.user)
    form_com = CommentForm(prefix = 'comment')
    context = {'results':results, 'profile':profile, 'notif':notif, 'subscrib_onme':subscrib_onme, 'my_subscribs':my_subscribs, 'unread':unread, 'form_com':form_com}
    return render(request, 'root/search_results.html', context)


UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


@login_required
def news(request):
    profile = get_object_or_404(Profile, user = request.user)
    subscribs = Subscrib.objects.filter(who = request.user)
    form_st = StatusForm(prefix = 'status')
    form_com = CommentForm(prefix = 'comment')
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
                'form_com' : form_com, 'subscribs' : subscribs, 'subscrib_onme':subscrib_onme}
    return render (request, 'root/news.html', context)


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
                    'notif': notif, 'form_com' : form_com, 'subscrib_onme':subscrib_onme, 'taboo' : taboo}
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
                        'subscrib_onme':subscrib_onme, 'form_mes' : form_mes, 'form_im':form_im, 'taboo' : taboo, 'fol':fol, 'black':black}
        else:
            context = {'post' : posts, 'profile' : profile, 'subscrib' : subscrib, 'you_subscribed' : False, 'form_com' : form_com,
                     'subscrib_onme':subscrib_onme, 'form_mes' : form_mes, 'form_im':form_im, 'taboo' : taboo, 'fol':fol, 'black':black}
    return render(request, 'root/wall.html', context)


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


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user = request.user)
    if request.method == 'POST':
        form_em = ChangeEmailForm(request.POST)
        print(request.POST.get('email'))
        if request.POST.get('email') == '':
            if request.POST.get('private') == 'close-it':
                profile.is_closed = True
                profile.save()
            elif request.POST.get('private') == 'open-it':
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
            profile.is_closed = True
            profile.save()
        elif request.POST.get('private') == 'open-it':
            profile.is_closed = False
            profile.save()
    form_em = ChangeEmailForm()
    subscrib_onme = Subscrib.objects.filter(to = request.user)
    my_subscribs = Subscrib.objects.filter(who = request.user)
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
    context = {'profile' : profile, 'form_em':form_em, 'subscrib_onme':subscrib_onme, 'my_subscribs':my_subscribs, 'notif':notif, 'unread':unread}
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
            return redirect ('avatarize')
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
def liked_objects(request):
    like = Like.objects.filter(liker = request.user).order_by('-when')
    profile = get_object_or_404(Profile, user = request.user)
    subscrib_onme = Subscrib.objects.filter(to = request.user)
    my_subscribs = Subscrib.objects.filter(who = request.user)
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
    return render(request, 'root/liked.html', {'like' : like, 'profile' : profile, 'notif':notif, 'subscrib_onme':subscrib_onme, 'my_subscribs':my_subscribs, 'unread':unread})

@login_required
def avatarize(request):
    create_url = "http://localhost:8000/create_profile/"
    if request.META['HTTP_REFERER'] == create_url:
        context = {'first_visit':True}
    else:
        context = {}
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.user.id
            profile = get_object_or_404(Profile, user = request.user)
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            key = make_template_fragment_key('first', [request.user.username])
            cache.delete(key)
            messages.success(request, 'Your avatar was updated!', extra_tags='alert alert-success alert-dismissible fade-show')
            return redirect ('wall', user_id)
        else:
            form = AvatarForm()
            context.update({'form' : form})
            return render(request, 'profiles/avatarize.html', context)
    else:
        form = AvatarForm()
        context.update({'form' : form})
        return render(request, 'profiles/avatarize.html', context)

@login_required
def notifications(request):
    user = request.user
    profile = get_object_or_404(Profile, user = user)
    notification = Notification.objects.filter(recipient = user)
    subscrib_onme = Subscrib.objects.filter(to = request.user)
    my_subscribs = Subscrib.objects.filter(who = request.user)
    for n in notification:
        if n.is_older_than_day() and n.status == 'Read':
            n.delete()
    for n in notification:
        if n.about != 'Subscribe' and n.content_object == None:
            n.delete()
    notification = Notification.objects.filter(recipient = user)
    i = 0
    for d in profile.dialogues.all():
        if d.has_unread_messages(request.user):
            i = i+1
    if i >0:
        unread = True
    else:
        unread = False
    return render(request, 'root/notifications.html', {'notification' : notification, 'profile' : profile, 'my_subscribs':my_subscribs, 'subscrib_onme':subscrib_onme, 'unread':unread})
