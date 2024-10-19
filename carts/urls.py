from django.urls import path
from .views import getCart, emptyCart, deleteProductCart, buyCart, addToCart

urlpatterns = [
    path('cart-detail/<int:uid>/', getCart, name='cart-detail'),
    path('empty-cart/<int:uid>/', emptyCart, name='empty-cart'),
    path('cart-product-delete/<int:uid>/<int:pid>', deleteProductCart, name='cart-product-delete'),
    path('cart-buy/<int:uid>/', buyCart, name='cart-buy'),
    path('add-to-cart/<int:uid>/<int:pid>/', addToCart, name='add-to-cart'),
]