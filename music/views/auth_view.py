from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from music.models.auth_model import Profile  # ✅ Your Profile model

def login_view(request):
    show_register_toast = request.session.pop("registration_success", False)
    show_logout_toast = request.session.pop("logout_success", False)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session["login_success"] = True
            return redirect("home")
        else:
            messages.error(request, "❌ Invalid credentials.", extra_tags="login")

    if request.session.get("open_register"):
        del request.session["open_register"]

    return render(request, "music/auth/login.html", {
        "show_register_toast": show_register_toast,
        "show_logout_toast": show_logout_toast  # ✅ NEW
    })



# ✅ Register View
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        full_name = request.POST.get("full_name")
        contact_number = request.POST.get("contact_number")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # 🔐 Validation
        if password1 != password2:
            messages.error(request, "❌ Passwords do not match.", extra_tags="register")
            return render(request, "music/auth/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "❌ Username is already taken.", extra_tags="register")
            return render(request, "music/auth/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "❌ Email is already registered.", extra_tags="register")
            return render(request, "music/auth/register.html")

        if Profile.objects.filter(contact_number=contact_number).exists():
            messages.error(request, "❌ Contact number is already in use.", extra_tags="register")
            return render(request, "music/auth/register.html")

        # ✅ Create user and profile
        user = User.objects.create_user(username=username, email=email, password=password1)
        Profile.objects.create(user=user, full_name=full_name, contact_number=contact_number)

        # ✅ Instead of messages, set toast session flag
        request.session["registration_success"] = True
        return redirect("login")  # Redirect to login to show popup

    return render(request, "music/auth/register.html")

# Logout Function
def logout_view(request):
    logout(request)
    request.session["logout_success"] = True  # ✅ Flag for toast
    return redirect("login")


# ✅ AJAX: Username availability
def check_username(request):
    username = request.GET.get("username")
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})


# ✅ AJAX: Email availability
def check_email(request):
    email = request.GET.get("email")
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})
