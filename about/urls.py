from django.urls import path
from .views import getAbout

urlpatterns = [
    path('', getAbout, name='about')
]