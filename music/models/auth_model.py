from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.templatetags.static import static

# ✅ Custom Validator: Ensures number starts with 98 or 97 and is exactly 10 digits
contact_number_validator = RegexValidator(
    regex=r'^(98|97)\d{8}$',
    message="Enter a valid 10-digit Nepali phone number starting with 98 or 97."
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150)
    contact_number = models.CharField(
        max_length=10, 
        validators=[contact_number_validator],
        unique=True  # Ensures contact numbers are not duplicated
    )
    profile_picture = models.ImageField(
    upload_to="profile_pics/", 
    blank=True, 
    null=True,
    default='music/images/default_profile.jpg'  # or use your function if serving from static
)

    def __str__(self):
        return self.user.username


# ✅ Security Question Model
class SecurityQuestion(models.Model):
    QUESTION_CHOICES = [
        ("pet_name", "What is the name of your first pet?"),
        ("school", "What was your first school?"),
        ("first_movie", "Whaich was you first movie in theater?"),
        ("childhood_friend", "Who was your childhood best friend?"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="security_question")
    question = models.CharField(max_length=50, choices=QUESTION_CHOICES)
    answer = models.CharField(max_length=255)  # Stores hashed or plain text answer

    def __str__(self):
        return f"{self.user.username} - {self.get_question_display()}"
