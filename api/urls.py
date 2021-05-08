from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CreateUserView, UserViewSet

users_router = DefaultRouter()
users_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='token'),
    path('v1/registration/', CreateUserView.as_view({'post': 'create'}),
         name='registration'),

    path('v1/', include(users_router.urls)),
]
