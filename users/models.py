from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
 

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )

    user_code = models.CharField(max_length=10, unique=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def save(self, *args, **kwargs):

        if not self.user_code:
            last_user = CustomUser.objects.all().order_by('id').last()

            if last_user and last_user.user_code:
                last_id = int(last_user.user_code[1:])
                new_id = last_id + 1
            else:
                new_id = 1

            self.user_code = f"U{new_id:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
