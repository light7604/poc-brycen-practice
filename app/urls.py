from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('shop/search', views.shopSearch, name="shop_search"),
    path('shop/', views.shopSearch, name="shop_search"),
    path('shop_detail/', views.shopDetail, name="shop_detail"),
    path('shoping_cart/', views.shopCart, name="shop_cart"),
    path('shop_category/', views.shopCategory, name="shop_category"),
    path('contact/', views.contact, name="contact"),

]