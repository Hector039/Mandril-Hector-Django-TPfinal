from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **others_fields):
        if not email:
            raise ValueError("Email is missing")
        if not password:
            raise ValueError("Password is missing")
        email = self.normalize_email(email) 
        user = self.model(email=email, **others_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **others_fields):
        others_fields.setdefault("is_staff", True)
        others_fields.setdefault("is_superuser", True)
        others_fields.setdefault("is_active", True)

        if others_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if others_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **others_fields)