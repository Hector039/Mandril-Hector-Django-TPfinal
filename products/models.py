from django.db import models
from users.models import CustomUser

# Create your models here.
class Product(models.Model):
    class ProducCategory(models.TextChoices):
        electronics = 'electronics'
        furniture = 'furniture'
        accesories = 'accesories'
        computing = 'computing'
        other = 'other'

    title =         models.CharField(max_length=200)
    description =   models.TextField(blank=True)
    price =         models.DecimalField(max_digits=7, decimal_places=2)
    stock =         models.IntegerField()
    category =      models.CharField(max_length=15, choices=ProducCategory, default=ProducCategory.other)
    owner =         models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created =       models.DateTimeField(auto_now_add=True)
    status =        models.BooleanField(default=True)

    def __str__(self):
        return self.title