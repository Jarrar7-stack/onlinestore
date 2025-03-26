from django.shortcuts import render, redirect
from .models import * 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Create a new user
            messages.success(request, "Account created successfully! Please sign in.")
            return redirect('home')  # Redirect to Sign-In page after successful signup
        else:
            messages.error(request, "Error creating account. Please check the form.")
    else:
        form = UserCreationForm()  # Display an empty sign-up form for GET requests

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
    return render(request, 'signin.html')