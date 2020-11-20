from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import ELearningUserManager


class User(AbstractBaseUser, PermissionsMixin):
    class CategoryChoices(models.TextChoices):
        TEACHER = 'teacher', 'teacher'
        STUDENT = 'student', 'student'

    # class StatusChoices(models.TextChoices):
    #     ACTIVE = 'active', 'active'
    #     INACTIVE = 'inactive', 'inactive'

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    category = models.CharField(
        max_length=10, choices=CategoryChoices.choices, default=CategoryChoices.STUDENT)
    # status = models.CharField(
    #     max_length=10, choices=StatusChoices.choices, default=StatusChoices.INACTIVE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    date_joined = None
    last_login = None

    objects = ELearningUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username
