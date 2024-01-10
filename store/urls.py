from django.urls import path
from .import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('middle', views.MiddlePage, name='middlepage'),
    path('contact/', views.Contact, name='contact'),
    path('register/', views.Register, name='register'),
    path('login/', views.UserLogin, name='login'),
    path('logout/', views.UserLogin, name='logout'),
    path('products/', views.Products, name='products'),
]
