import random
from django.core.mail import send_mail
from django.contrib.auth import login
from allauth.account.forms import SignupForm
from django import forms
from django.shortcuts import redirect

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Имя', required=True)
    last_name = forms.CharField(max_length=30, label='Фамилия', required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        # 🔐 Генерация кода
        code = str(random.randint(100000, 999999))
        user.email_code = code
        user.email_confirmed = False
        user.save()

        # ✉️ Отправка письма
        send_mail(
            subject='Код подтверждения почты',
            message=f'Здравствуйте, {user.first_name}!\n\nВаш код подтверждения: {code}',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

        # 🔑 Вход в систему
        login(request, user)

        # 🔁 Переход на страницу подтверждения
        return redirect('confirm_email')

from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar', 'bio']