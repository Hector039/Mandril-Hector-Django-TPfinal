from django.urls import path
from .views import getProduct, getProducts, buyProduct, updateProduct, deleteProduct, createProduct

urlpatterns = [
    path('product-detail/<int:pid>/', getProduct, name='product-detail'),
    path('product-buy/<int:pid>/', buyProduct, name='product-buy'),
    path('product-update/<int:pid>/', updateProduct, name='product-update'),
    path('product-delete/<int:pid>/', deleteProduct, name='product-delete'),
    path('product-create/', createProduct, name='product-create'),
    path('', getProducts, name='home')
]