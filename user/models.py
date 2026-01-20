import uuid

from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, BaseModel):
    """
    Custom user model for Battle Score.
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "uid", "public_id"]

    email = models.EmailField(_("Email Address"), unique=True)
    public_id = models.UUIDField(help_text=_("Identifiant unique utilisé sur les sites partenaires"), unique=True, default=uuid.uuid4, editable=False)
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=True)


class Profile(BaseModel):
    """
    Private customer profile linked to a user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    pseudo = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Client(BaseModel):
    """
    Billing profile (company, association, ...) linked to a user.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients")
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    vat_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
