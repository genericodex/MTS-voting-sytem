from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(UserManager):
    def _create_user(self, stud_no, email, password, **extra_fields):
        if not stud_no:
            raise ValueError("The student number must be set")
        if not email:
            raise ValueError("The email must be set")
        
        email = self.normalize_email(email)
        user = self.model(stud_no=stud_no, email=email, **extra_fields)
        print(f"Raw password before hashing: {password}")
        user.make_password(password)
        print(f"Hashed password: {user.password}")
        user.save()
        return user

    def create_user(self, stud_no, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(stud_no, email, password, **extra_fields)

    def create_superuser(self, stud_no, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", '1')  # Admin user type

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(stud_no, email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE = (('1', "Admin"), ('2', "Voter"))
    username = None  # Removed username, using stud_no instead
    stud_no = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(default='2', choices=USER_TYPE, max_length=1)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "stud_no"  # Use stud_no for authentication
    REQUIRED_FIELDS = ["email"]  # Email is required for superuser creation

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
class ApprovedStudent(models.Model):
    student_number = models.CharField(max_length=10, unique=True)  # Student number field

    def __str__(self):
        return self.student_number