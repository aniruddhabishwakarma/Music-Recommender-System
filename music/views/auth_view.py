from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from music.models.auth_model import *  # ✅ Your Profile model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password


def login_view(request):
    show_register_toast = request.session.pop("registration_success", False)
    show_logout_toast = request.session.pop("logout_success", False)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # ✅ Check if user has NOT set a security answer
            if not hasattr(user, 'profile') or not user.profile.security_answer:
                return redirect("set_security_question")

            request.session["login_success"] = True
            return redirect("home")
        else:
            messages.error(request, "❌ Invalid credentials.", extra_tags="login")

    if request.session.get("open_register"):
        del request.session["open_register"]

    return render(request, "music/auth/login.html", {
        "show_register_toast": show_register_toast,
        "show_logout_toast": show_logout_toast
    })


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        full_name = request.POST.get("full_name")
        contact_number = request.POST.get("contact_number")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

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

        user = User.objects.create_user(username=username, email=email, password=password1)
        Profile.objects.create(user=user, full_name=full_name, contact_number=contact_number)

        request.session["registration_success"] = True
        return redirect("login")

    return render(request, "music/auth/register.html")


def logout_view(request):
    logout(request)
    request.session["logout_success"] = True
    return redirect("login")


def check_username(request):
    username = request.GET.get("username")
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})


def check_email(request):
    email = request.GET.get("email")
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})


@login_required
def set_security_question(request):
    questions = SecurityQuestion.objects.all()

    if request.method == "POST":
        question_id = request.POST.get("question")
        answer = request.POST.get("answer").strip().lower()

        profile = request.user.profile
        profile.security_question_id = question_id
        profile.security_answer = answer
        profile.save()

        request.session["security_question_set"] = True
        return redirect("home")

    return render(request, "music/auth/set_security_question.html", {
        "questions": questions
    })


def forgot_password_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            profile = user.profile

            if not profile.security_question or not profile.security_answer:
                messages.error(request, "❌ User has no security question set.")
                return redirect("forgot_password")

            request.session['reset_username'] = username
            return redirect("verify_security_question", username=username)

        except User.DoesNotExist:
            messages.error(request, "❌ User not found.")

    return render(request, "music/auth/forgot_password.html")


def verify_security_question_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    question = profile.security_question.question_text

    if request.method == "POST":
        answer = request.POST.get("answer").strip().lower()
        if answer == profile.security_answer.lower():
            request.session["verified_user"] = user.username
            return redirect("reset_password")
        else:
            messages.error(request, "❌ Incorrect answer. Try again.")

    return render(request, "music/auth/verify_security_question.html", {
        "question": question
    })


def reset_password_confirm_view(request):
    username = request.session.get("verified_user")
    if not username:
        return redirect("forgot_password")

    user = get_object_or_404(User, username=username)

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "❌ Passwords do not match.")
        else:
            user.set_password(new_password)
            user.save()
            request.session.pop("verified_user")
            request.session.pop("reset_username", None)
            messages.success(request, "✅ Password reset successful. Please login.")
            return redirect("login")

    return render(request, "music/auth/reset_password_form.html")
