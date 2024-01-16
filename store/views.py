from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Product,CustomUser,UserProfile,Category

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


from django.contrib.auth.decorators import user_passes_test

def check_admin(user):
    if not user.is_superuser:
        return False
    return True

@login_required
@user_passes_test(check_admin , login_url='login')
def AddCategory(request):
    error_message = None

    if request.method == "POST":
        name = request.POST.get('name')
        
        if name:
            existing_category = Category.objects.filter(name=name).first()
            if not existing_category:
                new_category = Category(name=name)
                new_category.save()
                return redirect('addcategory')
            else:
                error_message = 'Category with this name already exists.'

    return render(request, 'addcategory.html', {'error_message': error_message})

@login_required
@user_passes_test(check_admin , login_url='login')
def AddProduct(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        categories= request.POST.get('categories')
        image = request.FILES.get('image')

        product = Product(
            title=title,
            description=description,
            price=price,
            image=image
        )
        product.save()
        product.categories.add(categories)

        return redirect('products')


    categories = Category.objects.all()
    return render(request, 'additem.html', {'categories': categories})

@login_required
@user_passes_test(check_admin , login_url='login')
def DeleteProduct(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'deleteproduct.html', {'product': product})



@login_required
@user_passes_test(check_admin , login_url='login')
def EditProduct(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')

        category_id = request.POST.get('categories')
        category = get_object_or_404(Category, pk=category_id)
        product.category = category

        new_image = request.FILES.get('image')
        if new_image:
            product.image = new_image


        product.save()
        return redirect('products')
    return render(request, 'editproduct.html', {'product': product, 'categories': categories})






from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@login_required
def Profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.email = email
        user_profile.phone_number = phone_number

        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile.profile_picture = profile_picture

        user_profile.save()

        subject = 'Profile Update'
        from_email = 'dhanoopdharan@gmail.com'
        to_email = [user_profile.email]

        html_content = render_to_string('emailsend.html', {'user_profile': user_profile})

        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")

        msg.send()

        return render(request, 'updatedemail.html', {'user_profile': user_profile})

    return render(request, 'profile.html', {'user_profile': user_profile})



@login_required
def EmailSend(request):
    return render(request, 'emailsend.html')
@login_required
def UpdatedEmail(request):
    return render(request, 'updatedemail.html')


@login_required
def ViewProfile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'viewprofile.html',{'user_profile': user_profile} )




@login_required
def Products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

@login_required
def ProductDetail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'details.html' , {'product': product})




