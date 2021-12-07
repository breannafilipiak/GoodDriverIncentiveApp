"""DriverIncentive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from catalog.views import login_view
from django.contrib import admin
from django.urls import path
from catalog import views
from catalog.forms import (PwdResetConfirmForm, PwdResetForm)
from django.conf.urls import url
from django.urls import path, include
# from catalog.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^su/', include('django_su.urls')),
    path('', views.home, name = 'home'),
    path('login/', login_view.as_view(template_name = 'catalog/login.html'), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="catalog/password_reset.html",
                                                                 success_url='password_reset_email_confirm',
                                                                 email_template_name='catalog/password_reset_email.html',
                                                                 form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='catalog/password_reset_confirm.html',
                                                                                                success_url='password_reset_complete/',
                                                                                                form_class=PwdResetConfirmForm),
                                                                                                name="password_reset_confirm"),
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="catalog/reset_status.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/password_reset_complete/',
         TemplateView.as_view(template_name="catalog/reset_status.html"), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(next_page = '/login'), name='logout'),
    path('create_account/', views.create_account, name = 'create_account'),
    path('profile/', views.profile, name = 'profile' ),
    path('profile/edit/', views.edit_profile, name = 'edit_profile' ),
    path('apply/', views.application, name = 'apply'),
    path('products/', views.products, name = 'products'),
    path('product/<slug:slug>/', views.product, name = 'product'),
    path('category/<slug:category_slug>/', views.category, name = 'category'),
    path('cart/', views.cart, name = 'cart'),
    path('add/', views.add_to_cart, name = 'add_to_cart'),
    path('remove/', views.remove_from_cart, name = 'remove_from_cart'),
    path('update/', views.update_cart, name = 'update_cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('send_request/', views.send_application_request, name = 'send_request'),
    path('place_order/', views.place_order, name = 'place_order'),
    path('search_etsy/', views.search_etsy, name = 'search_etsy'),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="user_wishlist"),
    path("all_updates", views.all_updates, name="all_updates"),
]
