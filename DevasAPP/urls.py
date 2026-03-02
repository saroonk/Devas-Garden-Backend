from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bloglisting/', views.bloglisting, name='bloglisting'),
    path('blogdetails/<slug:slug>/', views.blogdetails, name='blogdetails'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contactus/', views.contactus, name='contactus'),
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
    path('productdetails/', views.productdetails, name='productdetails'),
    path('products/', views.products, name='products'),
    path('returnpolicy/', views.returnpolicy, name='returnpolicy'),
    path('terms/', views.terms, name='terms'),
    path('trackorder/', views.trackorder, name='trackorder'),


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),

    path('update-cart/', views.update_cart_quantity, name='update_cart_quantity'),

]
