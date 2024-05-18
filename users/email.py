from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_activate_email_message(user_id):
    """
    Функция отправки письма с подтверждением для аккаунта
    """
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    current_site = Site.objects.get_current().domain
    token = default_token_generator.make_token(user)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse_lazy(
        'users:confirm_email',
        kwargs={'uidb64': uid, 'token': token}
    )
    subject = f'Активируйте свой аккаунт, {user.username}!'
    message = render_to_string('users/activate_email_send.html', {
        'user': user,
        'activation_url': f'https://{current_site}{activation_url}',
    })
    return user.email_user(subject, message)
