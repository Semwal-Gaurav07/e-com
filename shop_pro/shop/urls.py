from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomePageView,
    RegisterView,
    LogoutConfirmView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    CategoryProductsView,
    AddToCartView,
    CartDetailView,
    UpdateCartQuantityView,
    CheckoutView,
    OrderHistoryView,
    checkout_success_view,
    about
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout_confirm/', LogoutConfirmView.as_view(), name='logout_confirm'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Product management
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    
    # Category and About
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
    path('about/', about, name='about'),

    # Cart
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:item_id>/<str:action>/', UpdateCartQuantityView.as_view(), name='update_cart_quantity'),

    # Checkout and Orders
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout-success/', checkout_success_view, name='checkout_success'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
]
