import hashlib
import time
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

BOT_TOKEN = "8040853048:AAEgH78gXXU-pAyMQi5M3-BZbSxabUv0yAA"

@csrf_exempt
def telegram_login(request):
    data = request.GET.dict()
    if not data:
        return HttpResponseBadRequest("No data provided")

    received_hash = data.pop("hash", None)
    if not received_hash:
        return HttpResponseBadRequest("No hash provided")

    # Check auth_date is fresh
    if abs(time.time() - int(data.get("auth_date", 0))) > 86400:
        return HttpResponseBadRequest("Login link expired")

    # Generate check string
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hmac_string = hashlib.sha256((check_string).encode()).hexdigest()

    if hmac_string != received_hash:
        return HttpResponseBadRequest("Invalid login")

    # Auth or create user
    user, created = User.objects.get_or_create(
        username=f"tg_{data['id']}",
        defaults={
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", ""),
        },
    )
    login(request, user)
    return redirect("/")