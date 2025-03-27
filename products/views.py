from django.shortcuts import render, redirect
from .models import * 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse


# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "Account created successfully! Please sign in.")
            return redirect('home')  
        else:
            messages.error(request, "Error creating account. Please check the form.")
    else:
        form = UserCreationForm()  

    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                messages.success(request, f"welcome, {user.username}!")
                return redirect('product_list')
            
            else:
                messages.error(request, 'invalid user name or password')
                return render(request, 'signin.html')
        else:
            messages.error(request, "Both username and password are required.")
    return render(request, 'signin.html')
    


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def newly_arrived(request):
    new_products = Product.objects.filter(is_new=True)
    return render(request, 'newly_arrived.html', {'new_products': new_products})

def about_us(request):
    return render(request, 'about.html')

def logout_view(request):
    logout(request)
    return redirect('signin')

def create_order(request):
    if request.method == 'POST':
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        
        if cart_items.exists():
            order = Order.objects.create(user=user) 
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )
            order.calculate_total_price()  
            cart_items.delete()  

            return redirect('order_confirmation')  
    return redirect('cart')  

def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)  
    cart_total = sum(item.quantity * item.product.price for item in cart_items)  
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

def create_order(request):
    if request.method == 'POST':
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        if cart_items.exists():
            order = Order.objects.create(user=user)
        for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )
        order.calculate_total_price()
        cart_items.delete()
        return redirect('order_confirmation', order_id=order.id)
    return redirect('cart')

def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect('create_order')
    return render(request, 'order_confirmation.html', {'order': order})


def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found!'}, status=404)
        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, 
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
          
            if cart_item.quantity + 1 > product.stock:
                return JsonResponse({'error': 'Not enough stock available!'}, status=400)
            cart_item.quantity += 1
            cart_item.save()
        else:
        
            if product.stock < 1:
                return JsonResponse({'error': 'Not enough stock available!'}, status=400)

        return JsonResponse({'message': 'Item added to cart successfully!'})

    return JsonResponse({'error': 'Invalid request method!'}, status=400)