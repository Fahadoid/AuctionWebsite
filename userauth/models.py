from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.apps import apps


class UserManager(BaseUserManager):
    """Custom UserManager for user models with no username. Code is based on
    django's source code in django/contrib/auth/models.py"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a normal user with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """The user model"""

    objects = UserManager()

    username = None
    email = models.EmailField(unique=True)
    dob = models.DateField(null=False)
    avatar = models.ImageField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["dob"]

    def to_dict(self):
        """return user into dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "dob": self.dob,
            "avatar_path": self.avatar.url if self.avatar else None,
        }
