from django.urls import path
from .views import closeSession, updateUserView, signInView, signUpView, ChangePassword

urlpatterns = [
    path('signin/', signInView.as_view(), name='signin'),
    path('signup/', signUpView.as_view(), name='signup'),
    path('account/', updateUserView.as_view() , name='account'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('logout/', closeSession, name='logout'),
]