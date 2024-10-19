from django.db import models
from users.models import CustomUser
from products.models import Product

# Create your models here.
class Cart(models.Model):
    userId =        models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    productId =     models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =      models.IntegerField(default=1)

    class Meta:
        constraints = [models.CheckConstraint(condition=~models.Q(userId=models.F("productId")), name = 'owner_constraint'), 
                       models.UniqueConstraint(fields=['userId', 'productId'], name='unique_product')]

    