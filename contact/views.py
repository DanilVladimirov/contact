from datetime import datetime, timedelta

import jwt
from django.contrib.staticfiles import storage
from django.http import HttpResponse
from django.shortcuts import (render,
                              redirect, get_object_or_404)
from contact.forms import MyUserForm, CreatePost, UserSettings, ImageUser, BackGroundUser, UserNameSurname
from django.contrib.auth import authenticate, login, logout
from contact.models import PageUsers, Post, CommentsPost, Follows
from django.contrib.auth.models import User
from vk import settings


def start_page(request):
    return render(request, 'start-page.html')


def register(request):
    form = MyUserForm(request.POST)
    storage.used = True
    if request.POST:
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            user.first_name = 'Noname'
            user.last_name = 'Dodik'
            user.save()
            page_user = PageUsers.objects.create(user=user)
            page_user.save()
            login(request, user)
            return redirect('name_surname_page')
    context = {'form': form}
    return render(request, 'register.html', context)


def name_surname_page(request):
    form = UserNameSurname(request.POST)
    context = {}
    if request.POST:
        user = User.objects.get(id=request.user.id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        return redirect('home')
    context.update({'form': form})
    return render(request, 'name-surname-page.html', context)


def login_user(request):
    storage.used = True
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,
                                username=username,
                                password=password)
            if user is not None:
                login(request, user)
                if request.session.get('oauth') == True:
                    return redirect('oauth_page')
                return redirect('home')
            else:
                pass
        context = {}
        return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_page')


def page(request, pid):
    form_post = CreatePost(request.POST)
    action = request.POST.get("action")
    is_followed = False
    page_user = PageUsers.objects.get(id=pid)
    user = User.objects.get(id=page_user.user_id)
    check_follow = Follows.objects.get_or_create(user=User.objects.get(username=request.user.username))
    check_follow = Follows.objects.get(user=User.objects.get(username=request.user.username))
    check_follow = check_follow.another_user.filter(username=user.username)
    if len(check_follow) == 1:
        is_followed = True
    if request.POST and action == "delete_post":
        post_to_remove = Post.objects.get(id=request.POST.get("id"))
        Post.delete(post_to_remove)
    if request.POST and action == "follow":
        page_user = PageUsers.objects.get(id=pid)
        user_to_follow = User.objects.get(id=page_user.user_id)
        curr_user = User.objects.get(username=request.user.username)
        follow = Follows.objects.get(user=curr_user)
        follow.another_user.add(user_to_follow)
        is_followed = True
    if request.POST and action == "unfollow":
        page_ = PageUsers.objects.get(id=pid)
        user_page = User.objects.get(id=page_.user_id)
        curr_user = User.objects.get(username=request.user.username)
        follow = Follows.objects.get(user=curr_user)
        follow.another_user.remove(user_page)
        is_followed = False
    if request.POST:
        if form_post.is_valid():
            form_post.save()
            post = Post.objects.create(label=form_post.cleaned_data['label'],
                                       text=form_post.cleaned_data['text'],
                                       page=PageUsers.objects.get(id=pid))
            post.save()
    posts = Post.objects.filter(page=PageUsers.objects.get(id=pid))

    if request.POST and action == "add_comm":
        user = User.objects.get(username=request.user.username)
        post = Post.objects.get(id=request.POST.get("id"))
        comment = CommentsPost.objects.create(user=user,
                                              text=request.POST.get("text_post"))
        comment.save()
        post.comments.add(comment)
    context = {'page': get_object_or_404(PageUsers, id=pid),
               'form_post': form_post,
               'posts': posts,
               'is_followed': is_followed}
    return render(request, 'page.html', context)


def home(request):
    user = User.objects.get(username=request.user.username)
    page_user = PageUsers.objects.get(user=user)
    return redirect('page', page_user.id)


def settings_page(request):
    form = UserSettings(request.POST)
    form_img = ImageUser()
    form_back = BackGroundUser()
    action = request.POST.get('action')
    if request.POST and action == 'user_name':
        if form.is_valid():
            user = User.objects.filter(username=request.user.username)
            user.update(first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'])
    if request.POST and action == 'logo':
        user = User.objects.get(username=request.user.username)
        page_user = PageUsers.objects.filter(user=user)
        form_img = ImageUser(request.POST, request.FILES, instance=page_user[0])
        if form_img.is_valid():
            form_img.save()
    if request.POST and action == 'back_change':
        user = User.objects.get(username=request.user.username)
        page_user = PageUsers.objects.filter(user=user)
        form_back = BackGroundUser(request.POST, request.FILES, instance=page_user[0])
        if form_back.is_valid():
            form_back.save()
    return render(request, 'settings.html', {'form': form, 'form_img': form_img, 'form_back': form_back})


# авторизація через цю соц мережу
def oauth_page(request):
    action = request.POST.get('action')
    site = request.GET.get('site')
    token = ''
    if not request.user.is_authenticated:
        request.session.update({'site': site, 'oauth': True})
        return redirect('login_page')
    if request.POST and action == 'login':
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': request.user.id,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        if request.session.get('oauth') == True:
            site = request.session.get('site')
            request.session.update({'oauth': False})
        return redirect("http://" + site + "?token=" + token)
    return render(request, 'oauth-page.html')


def search_func(request):
    context = {}
    query = request.GET.get('q')
    users = User.objects.filter(username__icontains=query)
    context.update({'users': users})
    return render(request, 'search-page.html', context)


def follow_user(request):
    if request.POST:
        user_to_follow = User.objects.get(id=request.POST['user_id'])
        curr_user = User.objects.get(username=request.user.username)
        follow = Follows.objects.get(user=curr_user)
        follow.another_user.add(user_to_follow)
    return HttpResponse('')


def unfollow_user(request):
    if request.POST:
        user_page = User.objects.get(id=request.POST['user_id'])
        curr_user = User.objects.get(username=request.user.username)
        follow = Follows.objects.get(user=curr_user)
        follow.another_user.remove(user_page)
    return HttpResponse('')


def user_follows(request, user_id):
    user = User.objects.get(id=user_id)
    context = {'users': user.follows.another_user.all()}
    return render(request, 'user-follows-page.html', context)
