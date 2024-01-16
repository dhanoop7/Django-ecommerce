from django.urls import path
from .import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('middle', views.MiddlePage, name='middlepage'),
    path('contact/', views.Contact, name='contact'),
    path('register/', views.Register, name='register'),
    path('login/', views.UserLogin, name='login'),
    path('logout/', views.UserLogin, name='logout'),
    path('profile/', views.Profile, name='profile'),
    path('emailsent/', views.EmailSend, name='emailsent'),
    path('updatedemail/', views.UpdatedEmail, name='updatedemail'),
    path('viewprofile/', views.ViewProfile, name='viewprofile'),
    path('products/', views.Products, name='products'),
    path('addcategory/', views.AddCategory, name='addcategory'),
    path('additem/', views.AddProduct, name='additem'),
    path('deleteproduct/<int:product_id>/', views.DeleteProduct, name='deleteproduct'),
    path('editproduct/<int:product_id>/', views.EditProduct, name='editproduct'),
    path('details/<int:product_id>/', views.ProductDetail, name='details'),
]
