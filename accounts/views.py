from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

#     PasswordChangeDoneView,
#     PasswordChangeView,
#     PasswordResetCompleteView,
#     PasswordResetConfirmView,
#     PasswordResetDoneView,
#     PassowrdResetView
# )

from ideas.models import Idea
from projects.models import Project

User = get_user_model()

def profile_view(request, slug):
    # request.session['chat_users'] = ""
    u = User.objects.get(slug = slug)
    context = {
        'user': u,
        'ideas': Idea.objects.filter(originator = u),
        'projects': Project.objects.filter(creator = u)
    }
    return render(request, 'accounts/profile.html', context)

class UserCreateView(CreateView):
    model = User
    template_name = 'accounts/create.html'
    fields = [
        'first_name',
        'last_name',
        'email',
        'password'
    ]

    def form_valid(self, form):
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        redirect  = super().form_valid(form)
        self.request.session['chat_users'] = [model_to_dict(u, fields=['username', 'slug']) for u in User.objects.all().order_by('id')]
        return redirect

class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


# class UserPasswordChangeDoneView(PasswordChangeDoneView):
#     pass
#
# class UserPasswordChangeView(PasswordChangeView):
#     pass
#
# class UserPasswordResetCompleteView(PasswordResetCompleteView):
#     pass
#
# class UserPasswordResetConfirmView(PasswordResetConfirmView):
#     pass
#
# class UserPasswordResetDoneView(PasswordResetDoneView):
#     pass
#
# class UserPasswordResetView(PasswordResetView):
#     pass
