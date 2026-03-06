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
    path('productdetails/<slug:slug>/', views.productdetails, name='productdetails'),
    path('products/', views.products, name='products'),
    path("products/category/<slug:slug>/", views.products, name="products_by_category"),

    path('returnpolicy/', views.returnpolicy, name='returnpolicy'),
    path('terms/', views.terms, name='terms'),
    path('shippinganddeliveryPolicy/', views.shippinganddeliveryPolicy, name='shippinganddeliveryPolicy'),
    path('trackorder/', views.trackorder, name='trackorder'),


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),

    path('update-cart/', views.update_cart_quantity, name='update_cart_quantity'),


    path('wishlist/', views.wishlist, name='wishlist'),

    path('search/', views.search, name='search'),

    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),


    path('calculate-shipping/', views.calculate_shipping, name='calculate_shipping'),

    path("place-order/",views.place_order,name="place_order"),
    path("payment-success/",views.payment_success,name="payment_success"),
    path("order-success/",views.order_success,name="order_success"),



]
