"""cube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from .views import *
from .api import *

urlpatterns = [
    path('api/sign/in/', SignInAPIView.as_view()),
    path('api/sign/up/', SignUpAPIView.as_view()),
    path('api/sign/out/', SignOutAPIView.as_view()),
    path('api/sign/updateAuthToken/', UpdateAuthTokenAPIView.as_view()),
    path('api/sign/getAuthToken/', GetAuthTokenAPIView.as_view()),
    path('api/subscribeToUser/', SubscribeToUserAPIView.as_view()),
    path('api/account/editProfile/', EditUserProfileAPIView.as_view()),

    path('api/create/post/', CreatePostAPIView.as_view()),
    path('api/create/comment/', CreateCommentAPIView.as_view()),
    path('api/delete/post/', DeletePostAPIView.as_view()),
    path('api/delete/comment/', DeleteCommentAPIView.as_view()),

    path('api/likeModel/', LikeModelAPIView.as_view()),

    path('api/get/post/', GetPostAPIView.as_view()),

    # path('api/get/user/'),
    # path('api/get/comment/'),
    # path('api/get/comments'),

    path('', HomePageView.as_view()),

    path('sign/', SignView.as_view(), name='sign'),
    path('account/<str:username>/', AccountView.as_view(), name='account_view'),
    path('account/<str:username>/subscribers/', AccountSubscribersView.as_view(), name='account_subscribers'),
    path('account/<str:username>/subscriptions/', AccountSubscriptionsView.as_view(), name='account_subscriptions'),
    path('account/<str:username>/settings/', AccountSettingsView.as_view(), name='account_settings'),

    path('create/post/', CreatePostView.as_view(), name='post_create'),
    path('post/<int:pk>/', ViewPostView.as_view(), name='post_view'),

    path('api/docs/', ApiDocsView.as_view()),
]
