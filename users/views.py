from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import random
from django.http import JsonResponse
from allauth.account.views import LoginView, SignupView
from django.contrib.auth import login as auth_login

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = []
            for field, error_list in form.errors.items():
                errors.extend(error_list)
            return JsonResponse({"success": False, "error": errors[0] if errors else "Ошибка входа"})
        return super().form_invalid(form)

    def form_valid(self, form):
        auth_login(self.request, form.user_cache)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "redirect_url": "/"})
        return super().form_valid(form)

class CustomSignupView(SignupView):
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return super().form_invalid(form)

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # или "user_profile", в зависимости от urls.py
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "account/edit_profile.html", {"form": form})


@login_required
def confirm_email(request):
    if request.method == 'POST':
        if 'resend' in request.POST:
            # 🔁 Генерация нового кода
            code = str(random.randint(100000, 999999))
            request.user.email_code = code
            request.user.save()

            send_mail(
                subject='Повторный код подтверждения',
                message=f'Здравствуйте, {request.user.first_name}!\n\nВаш новый код подтверждения: {code}',
                from_email=None,
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            messages.success(request, 'Новый код отправлен на вашу почту.')
            return redirect('confirm_email')

        # Проверка кода
        code = request.POST.get('code')
        if code == request.user.email_code:
            request.user.email_confirmed = True
            request.user.email_code = ''
            request.user.save()
            messages.success(request, 'Почта успешно подтверждена!')
            return redirect('home')
        else:
            messages.error(request, 'Неверный код подтверждения.')

    return render(request, 'users/confirm_email.html')

@login_required
def profile(request):
    return render(request, 'account/profile.html')

@csrf_protect
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Ваш аккаунт был удалён.')
        return redirect('account_login')  # или на главную
    return redirect('profile')