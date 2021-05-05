from api.views import (api_gaga,
                       user_data,
                       HelloView)
from django.urls import path
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('', api_gaga),
    path('user-data/', user_data, name='user_data_api'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', HelloView.as_view(), name='hello'),
]
