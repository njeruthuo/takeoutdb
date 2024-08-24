from django.urls import path
from .views import SignupView, LoginWithToken, UserInfoView
from rest_framework.authtoken import views

urlpatterns = [
    path('signup/', SignupView.as_view(),
         name='signup'),
    path('login-auth/', LoginWithToken.as_view()),
    path('user-information/', UserInfoView.as_view()),
]
