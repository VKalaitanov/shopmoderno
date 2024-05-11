from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, FormView, TemplateView

from .decorators import redirect_authenticated_users
from .forms import (
    LoginUserForm, RegisterUserForm,
    ProfileUserForm, UserPasswordChangeForm
)


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + str(timestamp) + str(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()


@method_decorator(redirect_authenticated_users('users:login'), name='dispatch')
class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    next_page = 'moderno:home'


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('users:login'))


@method_decorator(redirect_authenticated_users('users:register'), name='dispatch')
class RegisterUserView(FormView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:email_confirmation_sent')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Пользователь неактивен до подтверждения email
        user.save()

        # Отправка на email ссылку для активации
        current_site = get_current_site(self.request).domain
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        activation_url = reverse_lazy(
            'users:confirm_email',
            kwargs={'uidb64': uid, 'token': token}
        )

        message = (
            f'Активация email на сайте {current_site}, если вы не регистрировались \n'
            f'на нашем сайте, игнорируйте это сообщение. \n'
            f'Иначе пожалуйста, перейдите по следующей ссылке, чтобы подтвердить \n'
            f'свой адрес электронной почты: http://{current_site}{activation_url}'
        )

        send_mail(
            'Подтвердите свой электронный адрес',
            message,
            'kalaitanov93@yandex.ru',
            [user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class UserConfirmEmailView(View):

    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'
    extra_context = {'title': 'Письмо активации отправлено'}


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'
    extra_context = {'title': 'Ваш электронный адрес активирован'}


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'
    extra_context = {'title': 'Ваш электронный адрес не активирован'}


class ProfileUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
