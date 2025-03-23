from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.templatetags.static import static

# ✅ Custom Validator: Ensures number starts with 98 or 97 and is exactly 10 digits
contact_number_validator = RegexValidator(
    regex=r'^(98|97)\d{8}$',
    message="Enter a valid 10-digit Nepali phone number starting with 98 or 97."
)


class SecurityQuestion(models.Model):
    question_text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.question_text
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150)
    contact_number = models.CharField(
        max_length=10, 
        validators=[contact_number_validator],
        unique=True
    )
    profile_picture = models.ImageField(
    upload_to="profile_pics/",
    blank=True,
    null=True,
    default="profile_pics/default.jpg"  # ✅ Corrected path
    )
    security_question = models.ForeignKey(SecurityQuestion, on_delete=models.SET_NULL, null=True, blank=True)
    security_answer = models.CharField(max_length=255, blank=True)  # ✅ Optional at first

    def __str__(self):
        return self.user.username
