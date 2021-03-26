from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.contrib.auth.views import PasswordContextMixin
from django.views.generic import CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('signup')
    template_name = 'signup.html'

