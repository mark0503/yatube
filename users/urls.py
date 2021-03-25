from django.urls import path
from . import views as v

urlpatterns = [
    path('signup/', v.SignUp.as_view(), name='signup'),
]
