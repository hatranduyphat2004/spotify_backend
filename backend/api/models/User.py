from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError

# Quản lý User


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        # Kiểm tra email
        if not email:
            raise ValidationError("Users must have an email address")
        if not password:
            raise ValueError("Password is required")
        email = self.normalize_email(email)  # Chuyển hóa email
        # Trạng thái tài khoản mặc định là active
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Mã hóa mật khẩu nếu có
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self.create_user(email, username, password, **extra_fields)

# Định nghĩa User Model


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    account_type = models.CharField(max_length=20, default='free', choices=[
        ('free', 'Free'), ('premium', 'Premium')])
    country = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='users/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, default='user', choices=[
        ('user', 'USER'), ('admin', 'ADMIN')])
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
