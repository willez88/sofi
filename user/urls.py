from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from .views import (
    LoginView, ProfileCreateView, ProfileDetailView, ProfileUpdateView,
)

app_name = 'user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path(
        'reset/password_reset/',
        views.PasswordResetView.as_view(
            template_name='user/password_reset_form.html',
            email_template_name='user/password_reset_email.html',
            success_url=reverse_lazy('user:password_reset_done')
        ),
        name='password_reset'
    ),
    path(
        'password_reset_done/',
        views.PasswordResetDoneView.as_view(
            template_name='user/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(
            template_name='user/password_reset_confirm.html',
            success_url=reverse_lazy('user:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(
            template_name='user/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path(
        'cambiar-clave/',
        login_required(views.PasswordChangeView.as_view(
            template_name='user/password_change_form.html',
            success_url=reverse_lazy('user:password_change_done')
        )),
        name='password_change'
    ),
    path(
        'cambiar-clave-hecho/',
        login_required(views.PasswordChangeDoneView.as_view(
            template_name='user/password_change_done.html'
        )),
        name='password_change_done'
    ),
    path('registrar/', ProfileCreateView.as_view(), name='create'),
    path(
        'actualizar/<int:pk>/', ProfileUpdateView.as_view(), name='update'
    ),
    path('detalle/<int:pk>/', ProfileDetailView.as_view(), name='detail')
]
