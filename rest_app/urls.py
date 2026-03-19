from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                      # home.html
    path('menu/', views.dish_list, name='list'),            # list.html
    path('dish/<int:id>/', views.dish_detail, name='detail'), # dish_detail.html
    path('cart/', views.cart_detail, name='cart_detail'),   # cart_detail.html
    path('order/new/', views.order_create, name='order_create'), # order_create.html
    path('orders/history/', views.order_history, name='history'), # order_history.html
    path('login/', views.user_login, name='login'),         # login.html
    path('register/', views.user_register, name='register'), # register.html
]