from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from utils.roles_utils import get_all_roles_names
import uuid


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    role = models.CharField(max_length=255)
    created_at = models.DateField(auto_now=True)
