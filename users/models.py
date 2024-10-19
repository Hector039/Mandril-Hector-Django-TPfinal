from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, CheckConstraint
from .manager import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    class Meta:
        constraints = [CheckConstraint(condition=Q(age__gte=18), name = 'age_gt18', violation_error_message='Your age must be greater than 18 years')]
        
    class userRole(models.TextChoices):
        admin = 'admin'
        premium = 'premium'
        user = 'user'

    username = None
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=200, unique=True)
    age = models.IntegerField()
    avatar = models.ImageField(upload_to='avatars', default='/avatars/default.png')
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=7, choices=userRole, default=userRole.user)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "age", "password"]

    objects = CustomUserManager()
