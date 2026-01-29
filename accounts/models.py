from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone number"
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name="Image"
    )

    is_worker = models.BooleanField(
        default=False,
        verbose_name="Worker"
    )

    is_manager = models.BooleanField(
        default=False,
        verbose_name="Manager"
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
