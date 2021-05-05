from django.contrib import admin
from django.urls import path, include
from contact.views import (start_page,
                           register,
                           login_user,
                           logout_user,
                           page,
                           home,
                           settings_page,
                           oauth_page,
                           name_surname_page,
                           search_func,
                           follow_user,
                           unfollow_user,
                           user_follows)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('', start_page, name='start_page'),
    path('register/', register, name='register_page'),
    path('login/', login_user, name='login_page'),
    path('logout/', logout_user, name='logout_page'),
    path('<int:pid>/', page, name='page'),
    path('settings/', settings_page, name='settings_page'),
    path('home/', home, name='home'),
    path('oauth/', oauth_page, name='oauth_page'),
    path('next_step/', name_surname_page, name='name_surname_page'),
    path('search/', search_func, name='search_page'),
    path('follow_user/', follow_user, name='follow_user'),
    path('unfollow_user/', unfollow_user, name='unfollow_user'),
    path('user_follows/<int:user_id>/', user_follows, name='user_follows_page')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
