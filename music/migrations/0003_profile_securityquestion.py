# Generated by Django 5.1.6 on 2025-03-21 13:03

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_alter_song_album'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('contact_number', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a valid 10-digit Nepali phone number starting with 98 or 97.', regex='^(98|97)\\d{8}$')])),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SecurityQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(choices=[('pet_name', 'What is the name of your first pet?'), ('school', 'What was your first school?'), ('first_movie', 'Whaich was you first movie in theater?'), ('childhood_friend', 'Who was your childhood best friend?')], max_length=50)),
                ('answer', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='security_question', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
