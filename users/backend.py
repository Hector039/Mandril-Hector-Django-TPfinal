from .models import CustomUser
from django.contrib.auth.backends import BaseBackend

class CustomBackend(BaseBackend):
    def authenticate(self, req=None, username=None, password=None):
        user = CustomUser.objects.get(email=username)
        print(user)

        if user is None:
            return None

        if user.check_password(password):
            return user     
        else:
            return None

    def get_user(self, uid):
        try:
            return CustomUser.objects.get(id=uid)
        except CustomUser.DoesNotExist:
            return None