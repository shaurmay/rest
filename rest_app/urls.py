from django.urls import path
from . import views

app_name = 'rest_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.dish_list, name='list'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:dish_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:dish_id>/', views.cart_remove, name='cart_remove'),
    
    path('order/create/', views.order_create, name='order_create'),
    path('order/history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/delete/', views.order_delete, name='order_delete'),
    
    # Авторизація
    # path('login/', views.user_login, name='login'),
    # path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('client/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
]

