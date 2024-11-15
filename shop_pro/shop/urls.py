from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import HomePageView, ProductDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout_confirm/', views.logout_confirm, name='logout_confirm'),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
     path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
     path('about/', views.about , name='about'),
      path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/<int:quantity_change>/', views.update_cart_quantity, name='update_cart_quantity'),



]
