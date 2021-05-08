from django.urls import include, path
from rest_framework.authtoken import views

from rest_framework.routers import DefaultRouter

from .views import CreateUserView, UserViewSet

users_router = DefaultRouter()
users_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    # path('auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),

    path('v1/registration/', CreateUserView.as_view({'post': 'create'})),
    path('v1/', include(users_router.urls)),

    # path('auth/email/',
    #      APIAuthCodeRequestViewSet.as_view({'post': 'create'})),
    #
    # path('auth/token/', APIAuthConfirm.as_view({'post': 'create'})),
    #
    #
    # path('token/', TokenObtainPairView.as_view(),
    #      name='token_obtain_pair'),
    #
    # path('token/refresh/', TokenRefreshView.as_view(),
    #      name='token_refresh'),
]

