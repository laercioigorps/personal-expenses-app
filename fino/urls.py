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
    path('login/', auth_views.LoginView.as_view(template_name='fino/login.html'),
         name='login_page'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home_page'),
    #path('dashboard', views.newview, name= 'home_page'),

    path('conta/criar', views.create_account_view, name='account_create'),
    path('conta/<int:id>', views.detail_account_view, name='account_detail'),
    path('conta/<int:id>/editar', views.edit_account_view, name='account_edit'),
    path('conta/<int:id>/delete', views.delete_account_view, name='account_delete'),
    path('contas/', views.list_account_view, name='account_list'),

    path('categoria/criar/', views.create_cattegory_view, name='cattegory_create'),
    path('acategoria/<int:id>', views.detail_cattegory_view,
         name='cattegory_detail'),
    path('categoria/<int:id>/editar',
         views.edit_cattegory_view, name='cattegory_edit'),
    path('categoria/<int:id>/deletar',
         views.delete_cattegory_view, name='cattegory_delete'),
    path('categorias/all', views.list_cattegory_view, name='cattegory_list'),
    path('categorias/', views.categorias_view, name='cattegory_list_by_date'),
    path('categorias/<int:month>/<int:year>',
         views.list_cattegory_by_month_year_view, name='cattegory_list_by_month_year'),


    path('transaction/', views.create_transaction_view, name='transaction_create'),
    path('transaction/create/<str:types>',
         views.create_transaction_by_type_view, name='transaction_by_type/create'),
    path('transacao/<int:id>', views.detail_transaction_view,
         name='transaction_detail'),
    path('transacao/<int:id>/edit',
         views.edit_transaction_view, name='transaction_edit'),
    path('transacao/<int:id>/delete',
         views.delete_transaction_view, name='transaction_delete'),
    path('transacoes/list/', views.list_transaction_view, name='transaction_list'),
    path('transacoes/<int:month>/<int:year>',
         views.list_transaction_view_by_month, name='transaction_list_by_month_year'),
    path('transacoes/', views.transacoes_view, name='transacoes'),

]
