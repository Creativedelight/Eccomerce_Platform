
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.shortcuts import redirect, get_object_or_404
from .models import Shoe, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    shoes = Shoe.objects.all()

    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart_item_count = CartItem.objects.filter(session_key=session_key).count()

    return render(request, 'store/home.html', {
        'shoes': shoes,
        'cart_item_count': cart_item_count
    })

@login_required
def add_to_cart(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, shoe=shoe)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart_item, created = CartItem.objects.get_or_create(session_key=session_key, shoe=shoe)

    if not created:
        cart_item.quantity += 1
    cart_item.save()  # ✅ This ensures it is saved to the database

    messages.success(request, f"{shoe.name} added to cart!")
    return redirect('home')


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart_items = CartItem.objects.filter(session_key=session_key)

    return render(request, 'store/cart.html', {'cart_items': cart_items})


def remove_from_cart(request, shoe_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(user=request.user, shoe_id=shoe_id).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
            cart_item = CartItem.objects.filter(session_key=session_key, shoe_id=shoe_id).first()

        if cart_item:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            messages.error(request, 'Item not found in your cart.')

    return redirect('view_cart')



@login_required
def update_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()  # ✅ This line must be here
                messages.success(request, "Cart updated successfully.")
            else:
                cart_item.delete()
                messages.success(request, "Item removed from cart.")
        except ValueError:
            messages.error(request, "Invalid quantity entered.")
    
    return redirect('view_cart')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {
        'form': form,
        'register_form': CustomUserCreationForm()
    })


def user_register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('home')
        else:
            print("Form errors:", form.errors.as_data())  # ✅ DEBUG LINE
            messages.error(request, "Registration failed. Please fix the errors below.")
            return render(request, 'store/login.html', {
                'form': AuthenticationForm(),
                'register_form': form
            })
    return redirect('login')

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
