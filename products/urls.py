from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import getProductView, getProducts, buyProduct, updateProduct, deleteProduct, createProductView

urlpatterns = [
    path('product-detail/<int:pk>/', getProductView.as_view(), name='product-detail'),
    path('product-buy/<int:pid>/', buyProduct, name='product-buy'),
    path('product-update/<int:pid>/', updateProduct, name='product-update'),
    path('product-delete/<int:pid>/', deleteProduct, name='product-delete'),
    path('product-create/', login_required(createProductView.as_view()), name='product-create'),
    path('', getProducts, name='home')
]