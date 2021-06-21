import json
import random
from datetime import datetime, timedelta
import jwt
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import storage
from django.http import HttpResponse
from django.shortcuts import (render,
                              redirect,
                              get_object_or_404)
from django.utils.translation import gettext, ugettext

from contact.forms import (MyUserForm,
                           CreatePost,
                           UserSettings,
                           ImageUser,
                           BackGroundUser,
                           UserNameSurname,
                           UploadImageForm,
                           UploadBackPublicForm,
                           UploadLogoPublicForm,
                           InfoPublicForm,
                           CreatePublicForm)
from django.contrib.auth import authenticate, login, logout
from contact.models import (PageUsers,
                            Post,
                            CommentsPost,
                            Follows,
                            Message,
                            Room,
                            Followers,
                            ImagesUser,
                            Public,
                            Types)
from django.contrib.auth.models import User
from vk import settings


def random_name():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    return randomstr


def start_page(request):
    return render(request, 'start-page.html')


def register(request):
    form = MyUserForm()
    storage.used = True
    if request.POST:
        form = MyUserForm(request.POST)
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
    context = {}
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
                context = {'error': True}

        return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
def page(request, pid):
    form_post = CreatePost(request.POST)
    action = request.POST.get("action")
    is_followed = False
    page_user = PageUsers.objects.get(id=pid)
    user = User.objects.get(id=page_user.user_id)
    check_follow = Follows.objects.get_or_create(user=User.objects.get(username=request.user.username))
    check_follow = Follows.objects.get(user=User.objects.get(username=request.user.username))
    check_follow = check_follow.another_user.filter(username=user.username)
    followers = Followers.objects.get_or_create(user=user)[0]
    print(followers)
    if request.POST and action == "upload":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_img = form.save()
            page_user.imgs.add(new_img)
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
        followers = Followers.objects.get(user=user_to_follow)
        followers.another_users.add(curr_user)
        is_followed = True
    if request.POST and action == "unfollow":
        page_ = PageUsers.objects.get(id=pid)
        user_page = User.objects.get(id=page_.user_id)
        curr_user = User.objects.get(username=request.user.username)
        follow = Follows.objects.get(user=curr_user)
        follow.another_user.remove(user_page)
        followers = Followers.objects.get(user=user_page)
        followers.another_users.remove(curr_user)
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
    img_user = list(page_user.imgs.all())[-3:]

    context = {'page': get_object_or_404(PageUsers, id=pid),
               'form_post': form_post,
               'posts': posts,
               'is_followed': is_followed,
               'img_user': img_user,
               'followers': followers}
    return render(request, 'page.html', context)


def home(request):
    user = User.objects.get(username=request.user.username)
    page_user = PageUsers.objects.get(user=user)
    return redirect('page', page_user.id)


def settings_page(request):
    form = UserSettings(request.POST)
    form_img = ImageUser(request.POST)
    form_back = BackGroundUser(request.POST)
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
    users_username = User.objects.filter(username__icontains=query)
    if len(query.split(' ')) == 2:
        query_split = query.split(' ')
        users_fistlast_name = User.objects.filter(first_name__icontains=query_split[0],
                                                  last_name__icontains=query_split[1])
        users = users_username.union(users_fistlast_name)
    else:
        users_first_name = User.objects.filter(first_name__icontains=query)
        users_last_name = User.objects.filter(last_name__icontains=query)
        users = users_username.union(users_first_name)
        users = users.union(users_last_name)
    publics = Public.objects.filter(title__icontains=query).exclude(black_list__in=[request.user])
    type_pub = Types.objects.filter(name__icontains=query)
    if type_pub.exists():
        publics_type = Public.objects.filter(type_public=type_pub[0]).exclude(black_list__in=[request.user])
        publics = list(publics) + list(publics_type)
    context.update({'users': users,
                    'publics': publics})
    return render(request, 'search-page.html', context)


def follow_user(request):
    if request.POST:
        user_to_follow = User.objects.get(id=request.POST['user_id'])
        curr_user = User.objects.get(username=request.user.username)
        follow = Follows.objects.get(user=curr_user)
        follow.another_user.add(user_to_follow)
        followers = Followers.objects.get_or_create(user=user_to_follow)
        followers[0].another_users.add(curr_user)
    return HttpResponse('')


def unfollow_user(request):
    if request.POST:
        user_page = User.objects.get(id=request.POST['user_id'])
        curr_user = User.objects.get(username=request.user.username)
        follow = Follows.objects.get(user=curr_user)
        follow.another_user.remove(user_page)
        followers = Followers.objects.get_or_create(user=user_page)
        followers[0].another_users.remove(curr_user)
    return HttpResponse('')


@login_required
def user_follows(request, user_id):
    user = User.objects.get(id=user_id)
    context = {'users': user.follows.another_user.all()}
    return render(request, 'user-follows-page.html', context)


def testindex(request):
    return render(request, 'testindex.html')


@login_required
def room(request, room_name):
    user_now = request.user
    context = {}
    if Room.objects.filter(name=room_name, user1=user_now).exists() or Room.objects.filter(name=room_name,
                                                                                           user2=user_now).exists():
        username = request.user.username
        messages = Room.objects.get(name=room_name).messages.all()
        room_ = Room.objects.get(name=room_name)
        if room_.user1.id == request.user.id:
            context.update({'user': room_.user2})
        else:
            context.update({'user': room_.user1})
        context.update({'room_name': room_name,
                        'username': username,
                        'messages': messages})
        return render(request, 'room.html', context)
    else:
        return redirect('start_page')


@login_required
def create_or_go_room(request, another_user):
    user1 = request.user
    user2 = User.objects.get(id=another_user)

    if Room.objects.filter(user1=request.user, user2=user2).exists():
        room_name = Room.objects.filter(user1=request.user, user2=user2)[0].name
        return redirect('room', room_name=room_name)
    elif Room.objects.filter(user1=user2, user2=user1).exists():
        room_name = Room.objects.filter(user2=user1, user1=user2)[0].name
        return redirect('room', room_name=room_name)
    else:
        new_room = Room.objects.create(name=random_name(), user1=user1, user2=user2)
        new_room.save()
        return redirect('room', room_name=new_room.name)


@login_required
def followers_user(request, user_id):
    followers = Followers.objects.get_or_create(user=User.objects.get(id=user_id))
    followers = followers[0].another_users.all()
    context = {'users': followers}

    return render(request, 'user-follows-page.html', context)


@login_required
def news_page(request):
    users = Follows.objects.get(user=request.user).another_user.all()
    publics = PageUsers.objects.get(user=request.user).publics.all()
    posts = None
    if users.exists():
        for user in users:
            if user.pageusers_set.get().post_set.all().exists():
                if posts is None:
                    posts = user.pageusers_set.get().post_set.all()
                else:
                    posts = posts.union(user.pageusers_set.get().post_set.all())

    if publics.exists():
        posts_pubs = None
        for pub in publics:
            if pub.posts.all():
                if posts_pubs is None:
                    posts_pubs = pub.posts.all()
                else:
                    posts_pubs = posts_pubs.union(pub.posts.all())
            if posts is not None:
                if len(posts_pubs) != 0:
                    posts = posts.union(posts_pubs)
            else:
                if len(posts_pubs) != 0:
                    posts = posts_pubs
            posts = posts.order_by('-id')

    context = {'posts': posts}

    return render(request, 'news-page.html', context)


@login_required
def all_photos_user(request, pageid):
    page_user = PageUsers.objects.get(id=pageid)
    img_user = page_user.imgs.order_by('-id')
    context = {'imgs': img_user}

    return render(request, 'all-photos-user.html', context)


@login_required
def del_img_user(request):
    data_response = {}
    if request.POST:
        img = ImagesUser.objects.get(id=request.POST.get('img_id'))
        img.delete()
        data_response.update({'success': True})
    return HttpResponse(json.dumps(data_response), content_type='application/json')


@login_required
def rooms_page(request):
    context = {}
    user = request.user
    rooms = []
    for room_ in Room.objects.filter(user1=user):
        rooms.append(room_)
    for room_ in Room.objects.filter(user2=user):
        rooms.append(room_)
    context = {'rooms': rooms}
    print(rooms)

    return render(request, 'rooms-page.html', context)


@login_required
def add_comment(request):
    data_response = {}
    if request.POST:
        post = Post.objects.get(id=request.POST.get("id"))
        comment = CommentsPost.objects.create(user=request.user,
                                              text=request.POST.get("text_post"))
        comment.save()
        post.comments.add(comment)
        data_response.update({'user_img': comment.user.pageusers_set.get().logo.url,
                              'upage_id': comment.user.pageusers_set.get().id,
                              'first_name': comment.user.first_name,
                              'last_name': comment.user.last_name,
                              'comm_text': comment.text,
                              'post_id': post.id})
    data_response.update({'success': True})
    return HttpResponse(json.dumps(data_response), content_type='application/json')


@login_required
def public_page(request, pib):
    context = {}
    public = Public.objects.get(id=pib)
    if request.user in public.black_list.all():
        return redirect('start_page')
    action = request.POST.get('action')
    context.update({'public': public})
    if request.POST and action == 'sub':
        user = request.user
        user.pageusers_set.get().publics.add(public)
    if request.POST and action == 'unsub':
        user = request.user
        user.pageusers_set.get().publics.remove(public)
    if request.POST and action == "upload":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_img = form.save()
            public.imgs.add(new_img)
    if request.POST and action == "new_post":
        post = Post.objects.create(label=request.POST.get('label'),
                                   text=request.POST.get('text'))
        post.save()
        public.posts.add(post)
    return render(request, 'public-page.html', context)


def del_post(request):
    data_response = {}
    if request.POST:
        post = Post.objects.get(id=request.POST.get('post_id'))
        post.delete()
        data_response.update({'success': True})
    return HttpResponse(json.dumps(data_response), content_type='application/json')


def public_settings(request, pib):
    context = {}
    public = Public.objects.get(id=pib)
    if request.user in public.black_list.all():
        return redirect('start_page')
    action = request.POST.get('action')
    context = {'public': public}
    if not request.user.id == public.creator.id and not request.user in public.admins.all():
        return redirect('public_page', pib=pib)
    if request.POST and action == 'logo':
        form_logo = UploadLogoPublicForm(request.POST, request.FILES, instance=public)
        if form_logo.is_valid():
            form_logo.save()
    if request.POST and action == 'back':
        form_back = UploadBackPublicForm(request.POST, request.FILES, instance=public)
        if form_back.is_valid():
            form_back.save()
    if request.POST and action == 'info':
        form_info = InfoPublicForm(request.POST, instance=public)
        if form_info.is_valid():
            form_info.save()

    return render(request, 'public-settings-page.html', context)


@login_required
def public_subscribers(request, pib):
    context = {}
    public = Public.objects.get(id=pib)
    if request.user in public.black_list.all():
        return redirect('start_page')
    action = request.POST.get('action')
    users = [user.user for user in public.pageusers_set.all()]
    context.update({'users': users, 'public': public})
    if request.POST and action == 'search':
        users = []
        users_ = User.objects.filter(username__icontains=request.POST.get('query'))
        for user in users_:
            if user.pageusers_set.get() in public.pageusers_set.all():
                users.append(user)
        context.update({'users': users})

    return render(request, 'public-search-page.html', context)


@login_required
def set_admin(request):
    data_response = {}
    if request.POST:
        public = Public.objects.get(id=request.POST.get('public_id'))
        user = User.objects.get(id=request.POST.get('user_id'))
        if not user in public.admins.all():
            public.admins.add(user)
            data_response.update({'success': True})
        else:
            public.admins.remove(user)
            data_response.update({'success': False})

        return HttpResponse(json.dumps(data_response), content_type='application/json')


@login_required
def set_moder(request):
    data_response = {}
    if request.POST:
        public = Public.objects.get(id=request.POST.get('public_id'))
        user = User.objects.get(id=request.POST.get('user_id'))
        if not user in public.moders.all():
            public.moders.add(user)
            data_response.update({'success': True})
        else:
            public.moders.remove(user)
            data_response.update({'success': False})

        return HttpResponse(json.dumps(data_response), content_type='application/json')


@login_required
def public_imgs_page(request, pib):
    public = Public.objects.get(id=pib)
    if request.user in public.black_list.all():
        return redirect('start_page')
    imgs_public = public.imgs.order_by('-id')
    action = request.POST.get('action')
    context = {'imgs': imgs_public, 'public': public}

    return render(request, 'all-photos-public.html', context)


@login_required
def add_to_blacklist(request):
    data_response = {}
    if request.POST:
        public = Public.objects.get(id=request.POST.get('public_id'))
        user = User.objects.get(id=request.POST.get('user_id'))
        for post in public.posts.all():
            if post.comments.exists():
                for comment in post.comments.all():
                    if comment.user.id == user.id:
                        comment.delete()
        public.black_list.add(user)
        user.pageusers_set.get().publics.remove(public)
        data_response = {'success': True}
    return HttpResponse(json.dumps(data_response), content_type='application/json')


@login_required
def del_from_blacklist(request):
    data_response = {}
    if request.POST:
        public = Public.objects.get(id=request.POST.get('public_id'))
        user = User.objects.get(id=request.POST.get('user_id'))
        public.black_list.remove(user)
        data_response = {'success': True}
    return HttpResponse(json.dumps(data_response), content_type='application/json')


@login_required
def sub_to_public(request):
    data_response = {}
    if request.POST:
        public = Public.objects.get(id=request.POST.get('pub_id'))
        user = request.user
        if public in user.pageusers_set.get().publics.all():
            user.pageusers_set.get().publics.remove(public)
            data_response = {'success': False}
        else:
            user.pageusers_set.get().publics.add(public)
            data_response = {'success': True}
        return HttpResponse(json.dumps(data_response), content_type='application/json')


@login_required
def publics_user(request, user_id):
    user = User.objects.get(id=user_id)
    context = {'pubs': user.pageusers_set.get().publics.all()}

    return render(request, 'publics-user-page.html', context)


@login_required
def create_public(request):
    types = Types.objects.all()
    if request.POST:
        form = CreatePublicForm(request.POST, request.FILES)
        if form.is_valid():
            new_pub = form.save()
            type_ = Types.objects.get(id=request.POST.get('type_id'))
            new_pub.creator = request.user
            new_pub.type_public = type_
            new_pub.save()
            request.user.pageusers_set.get().publics.add(new_pub)
            return redirect('public_page', pib=new_pub.id)
    context = {'types': types}
    return render(request, 'create-pub-page.html', context)
