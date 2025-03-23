# ✅ views/user_view.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from music.models.auth_model import Profile
from django.contrib.auth import update_session_auth_hash

@login_required
def profile(request):
    show_info_toast = request.session.pop("info_updated", False)
    show_password_toast = request.session.pop("password_updated", False)

    return render(request, "music/profile.html", {
        "show_info_toast": show_info_toast,
        "show_password_toast": show_password_toast
    })



@login_required
def update_profile_info(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        contact_number = request.POST.get("contact_number")

        # Update info
        user = request.user
        user.email = email
        user.save()

        profile = user.profile
        profile.full_name = full_name
        profile.contact_number = contact_number
        profile.save()

        request.session["info_updated"] = True
        return redirect("profile")



@login_required
def update_profile_picture(request):
    if request.method == "POST" and request.FILES.get("profile_picture"):
        profile_picture = request.FILES["profile_picture"]
        request.user.profile.profile_picture = profile_picture
        request.user.profile.save()

        messages.success(request, "🖼️ Profile picture updated!")
        return redirect("profile")


@login_required
def update_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):
            messages.error(request, "❌ Incorrect current password.")
        elif new_password != confirm_password:
            messages.error(request, "❌ Passwords do not match.")
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            request.session["password_updated"] = True

        return redirect("profile")
