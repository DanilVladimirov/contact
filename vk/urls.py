from django.contrib import admin
from django.urls import path
from contact.views import (start_page,
                           register,
                           login_user,
                           logout_user,
                           page,
                           home,
                           settings_page,
                           follows_page)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_page, name='start_page'),
    path('register/', register, name='register_page'),
    path('login/', login_user, name='login_page'),
    path('logout/', logout_user, name='logout_page'),
    path('<int:pid>/', page, name='page'),
    path('settings/', settings_page, name='settings_page'),
    path('home/', home, name='home'),
    path('follows/', follows_page, name='follows_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
