from django.urls import path
from . import views as v
from django.contrib.auth import views


urlpatterns = [
    path('signup/', v.SignUp.as_view(), name='signup'),
]
