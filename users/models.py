from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models


class UserManger(BaseUserManager):
    def create_user(self, email, password, *args, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.create(email=email, *args, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        user = self.create_user(email, password, *args, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractUser,PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

    @property
    def username(self):
        return self.name
