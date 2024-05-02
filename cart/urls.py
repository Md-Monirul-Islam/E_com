from django.urls import path
from . import views

app_name = 'cart_app'

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add-cart/<int:product_id>/', views.add_cart, name='add_cart'),
]
