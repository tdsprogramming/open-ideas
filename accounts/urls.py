from django.urls import path

from .views import (
    profile_view,
    UserCreateView,
    UserLoginView,
    UserLogoutView,
)
#     UserPasswordChangeDoneView,
#     UserPasswordChangeView,
#     UserPasswordResetCompleteView,
#     UserPasswordResetConfirmView,
#     UserPasswordResetDoneView,
#     UserPasswordResetView
# )

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:slug>/', profile_view, name='profile'),
    path('create/', UserCreateView.as_view(), name='create'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
