from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseForbidden
from .models import Category, Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Product

# registration for user with inblit authentication
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

#home page
from django.views.generic import View

class HomePageView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        context = {
            'products': products,
            'categories': categories
        }
        return render(request, 'shop/home.html', context)
    
    
class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'shop/product_detail.html', {'product': product})

# logout for user account
def logout_confirm(request):
    return render(request, 'shop/logout_confirm.html')




def product_list(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

def product_create(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})

def product_update(request, pk):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form})

def product_delete(request, pk):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'shop/product_delete.html', {'product': product})


def about(request):
    return render(request, 'shop/about.html')


@login_required
def add_to_cart(request, product_id):
    # Get the product the user is trying to add to the cart
    product = get_object_or_404(Product, id=product_id)

    # Get the quantity from the form
    try:
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if no quantity provided
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Invalid quantity.")

    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # If the product already exists in the cart, update the quantity
        cart_item.quantity += quantity
        cart_item.save()
    else:
        # If the product doesn't exist in the cart, set the quantity
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart_detail')  # Redirect to the cart page

@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    total_price = sum(item.product.price * item.quantity for item in cart.items.all())

    return render(request, 'shop/cart_detail.html', {
        'cart': cart,
        'total_price': total_price
    })

@login_required
def update_cart_quantity(request, item_id, quantity_change):
    # Get the cart for the logged-in user
    cart = Cart.objects.get(user=request.user)
    
    # Get the cart item that we need to update
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    # Update the quantity of the item based on the quantity_change (add or subtract)
    new_quantity = cart_item.quantity + quantity_change
    
    # Ensure the quantity doesn't drop below 1
    if new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        # Optionally, you can remove the item if the quantity is 0 or less
        cart_item.delete()

    return redirect('cart_detail')  # Redirect back to the cart details page