from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('product_list', views.product_list, name='product_list'),
    path('about/', views.about_us, name='about_us'),
    path('products/', views.product_list, name='product_list'),
    path('logout/', views.logout_view, name='logout'),
]
