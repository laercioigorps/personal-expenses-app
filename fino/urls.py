"""food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'fino'
urlpatterns = [
path('teste/', views.teste_view, name=""),
    path('signup/', views.signup_view, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='fino/login.html'),name='login'),
    path('', views.home_view, name= 'home_page'),
    path('dashboard', views.newview, name= 'home_page'),

    path('account/', views.create_account_view, name='account_create'),
    path('account/<int:id>', views.detail_account_view,name='account_detail'),
    path('account/<int:id>/edit', views.edit_account_view,name='account_edit'),
    path('account/<int:id>/delete', views.delete_account_view,name='account_delete'),
    path('account/list/', views.list_account_view, name='account_list'),

    path('cattegory/', views.create_cattegory_view, name ='cattegory_create'),
    path('cattegory/<int:id>', views.detail_cattegory_view,name='cattegory_detail'),
    path('cattegory/<int:id>/edit', views.edit_cattegory_view,name='cattegory_edit'),
    path('cattegory/<int:id>/delete', views.delete_cattegory_view,name='cattegory_delete'),
    path('cattegory/list/', views.list_cattegory_view, name='cattegory_list'),

    path('transaction/', views.create_transaction_view, name= 'transaction_create'),
    path('transaction/create/<str:types>', views.create_transaction_by_type_view, name= 'transaction_by_type/create'),
    path('transaction/<int:id>', views.detail_transaction_view,name='transaction_detail'),
    path('transaction/<int:id>/edit', views.edit_transaction_view,name='transaction_edit'),
    path('transaction/<int:id>/delete', views.delete_transaction_view,name='transaction_delete'),
    path('transaction/list/', views.list_transaction_view, name='transaction_list'),
    
]
