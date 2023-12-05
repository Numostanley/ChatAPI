from django.urls import path
from .views import UserRegister, UserDataAPI, UserLoginView

urlpatterns = [
    path('register', UserRegister.as_view()),
    path('get-details', UserDataAPI.as_view()),
    path('login', UserLoginView.as_view()),
]
