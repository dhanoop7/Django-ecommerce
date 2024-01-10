from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Product,CustomUser

# Create your views here.
def Home(request):
    return render(request, 'home.html')

def MiddlePage(request):
    return render(request, 'middlepage.html')

def Contact(request):
    return render(request, 'contact.html')

def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if CustomUser.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different username."
            return render(request, 'register.html', {'error_message': error_message})
        if confirm_password == password:
            CustomUser.objects.create_user(username=username, password=password)
            return redirect('login')
        else:
            error_message = 'Password does not match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')


def UserLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('products')
        else:
            return render(request, 'login.html', {'error_message':"Invalid login credentials!, If you do not have an account Sign up"})
    return render(request, 'login.html')

def UserLogOut(request):
    logout(request)
    return redirect('login')

@login_required
def Products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})