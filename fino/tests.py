from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from fino.utils import DateUtils


from .models import Cattegory, Account, Transaction
from .forms import AccountModelForm, Account_delete_form

from decimal import *

import datetime

# Create your tests here.


def create_cattegory(user, name, description, is_receita):
    return user.cattegory_set.create(user=user, name=name,
                                     description=description, is_receita=is_receita)


def create_account(user, name, description, total):
    return user.account_set.create(user=user, name=name,
                                   description=description, total=total)


def create_transaction(account, cattegory, description, total, is_completed, date):
    return account.transaction_set.create(cattegory=cattegory,
                                          description=description, total=total,
                                          is_completed=is_completed, date=date)


class SimpleTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'root', 'lennon@thebeatles.com', 'root')
        self.account = self.user.account_set.create(name='root account',
                                                    description='root account description',
                                                    total=100)
        self.cattegory = self.user.cattegory_set.create(name='category from root',
                                                        description='description of cattegory root', is_receita=True)
        self.transaction = self.account.transaction_set.create(cattegory=self.cattegory,
                                                               description='transaction from root', total=200, is_completed=True,
                                                               date=date.today())

    def test_nothing(self):
        self.assertIs(True, True)

    def test_false(self):
        is_logged = self.client.login(username='root', password='root')

        response = True
        #response = self.client.get(reverse('fino:home_page'))
        c = Cattegory.objects.create(name='teste2', description='asdsa',
                                     is_receita=True)
        self.assertIs(is_logged, True)


class Cattegory_views_test(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            'root', 'teste@gmail.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'teste@gmail.com', 'root2')
        self.user3 = User.objects.create_user(
            'root3', 'teste@gmail.com', 'root3')

        self.cat1_data = {
            'name': 'teste',
            'description': 'test',
            'is_receita': True,
        }
        self.cat2_data = {
            'name': 'cattegory2',
            'description': 'cattegory2 description',
            'is_receita': False,
        }


class Account_views_test_new_user(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            'root', 'teste@gmail.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'teste@gmail.com', 'root2')

        self.user3 = User.objects.create_user(
            'root3', 'test@gmail.com', 'root3')
        self.account1 = create_account(self.user3, 'user3 account',
                                       'user3 descriptions account', True)
        self.account2 = create_account(self.user3, 'user3 account is not mine',
                                       'user3 descriptions account', True)

    def test_create_account_get_with_no_user(self):
        response = self.client.get(reverse('fino:account_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_account_post_with_no_user(self):
        data = {
            'name': 'teste_account',
            'description': 'test description account',
            'total': 0,
        }
        self.response = self.client.post(reverse('fino:account_create'), data)
        self.assertEqual(self.response.status_code, 302)

    def test_account_list_get_with_no_user(self):
        response = self.client.get(reverse('fino:account_list'))
        self.assertEqual(response.status_code, 302)

    def test_user_count(self):
        count = User.objects.all().count()
        self.assertEqual(count, 3)

    def test_account_view_get_with_user_no_data(self):
        is_logged = self.client.login(username='root', password='root')
        self.assertEqual(is_logged, True)

        response = self.client.get(reverse('fino:account_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_create_account_post_with_new_user_no_data(self):

        is_logged = self.client.login(username='root', password='root')
        self.assertEqual(is_logged, True)

        data = {
            'name': 'teste_account',
            'description': 'test description account',
            'total': 0,
        }
        response = self.client.post(reverse('fino:account_create'), data)
        self.assertEqual(response.status_code, 302)

        contas = response.wsgi_request.user.account_set.count()
        self.assertEqual(contas, 1)

    def test_create_account_view_simultaneusly(self):
        is_logged = self.client.login(username='root', password='root')
        self.assertEqual(is_logged, True)

        data = {
            'name': 'teste_account',
            'description': 'test description account',
            'total': 0,
        }

        response = self.client.post(reverse('fino:account_create'), data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('fino:account_create'), data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('fino:account_create'), data)
        self.assertEqual(response.status_code, 302)

        contas = response.wsgi_request.user.account_set.all().count()
        self.assertEqual(contas, 3)

    def test_account_list_view_with_new_user(self):
        self.client.login(username='root', password='root')

        response = self.client.get(reverse('fino:account_list'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['list_objects'].count(), 0)

    def test_account_list_view_with_accounts(self):
        self.client.login(username='root', password='root')

        response = self.client.get(reverse('fino:account_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 0)

        create_account(response.wsgi_request.user, 'teste', 'description', 100)
        response = self.client.get(reverse('fino:account_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 1)

        create_account(response.wsgi_request.user, 'teste', 'description', 200)
        response = self.client.get(reverse('fino:account_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 2)

    def test_Account_eddit_get_no_user_view(self):

        response = self.client.get(
            reverse('fino:account_edit', args=[self.account1.id]))
        self.assertEqual(response.status_code, 302)

    def test_Account_eddit_new_user_acessing_others_account_view(self):
        self.client.login(username='root2', password='root2')
        response = self.client.get(
            reverse('fino:account_edit', args=[self.account2.id]))
        self.assertEqual(response.status_code, 403)

    def test_Account_eddit_user_acessing_others_account_view(self):

        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:account_list'))
        self.assertEqual(response.status_code, 200)

        create_account(response.wsgi_request.user, 'teste', 'description', 200)
        response = self.client.get(
            reverse('fino:account_edit', args=[self.account2.id]))
        self.assertEqual(response.status_code, 403)

    def test_Account_eddit_user_acessing_own_account_view(self):

        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:account_list'))
        self.assertEqual(response.status_code, 200)

        account = create_account(
            response.wsgi_request.user, 'teste', 'description', 200)
        response = self.client.get(
            reverse('fino:account_edit', args=[account.id]))
        self.assertEqual(response.status_code, 200)
        a = response.context['form'].save(commit=False)
        self.assertEqual(account, a)

    def test_delete_anonymous_user(self):
        response = self.client.get(
            reverse('fino:account_delete', args=[self.account2.id]))
        self.assertEqual(response.status_code, 302)

    def test_delete_other_user_account_get_with_new_user(self):
        self.client.login(username='root2', password='root2')
        response = self.client.get(
            reverse('fino:account_delete', args=[self.account2.id]))
        self.assertEqual(response.status_code, 403)

    def test_delete_get_with_new_user_invalid_account_id(self):
        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:account_delete', args=[0]))
        self.assertEqual(response.status_code, 404)

    def test_delete_account_get_post_with_new_user(self):
        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:account_list'))
        account = create_account(response.wsgi_request.user,
                                 'name_test', 'description', False)
        response = self.client.get(
            reverse('fino:account_delete', args=[account.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.wsgi_request.user.account_set.all().count(), 1)

        account = create_account(response.wsgi_request.user, 'name_test',
                                 'description', False)
        response = self.client.get(
            reverse('fino:account_delete', args=[account.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.wsgi_request.user.account_set.all().count(), 2)

        response = self.client.post(reverse('fino:account_delete',
                                            args=[account.id]), {'resposta': True})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.wsgi_request.user.account_set.all().count(), 1)

        response = self.client.get(reverse('fino:account_list'))
        self.assertEqual(response.context['list_objects'].count(), 1)


class Cattegory_views_test_new_user(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            'root', 'teste@gmail.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'teste@gmail.com', 'root2')

        self.user3 = User.objects.create_user(
            'root3', 'test@gmail.com', 'root3')
        self.cattegory1 = create_cattegory(
            self.user3, 'user3 cattegory', 'user3 descriptions cattegory', True)
        self.cattegory2 = create_cattegory(self.user3, 'user3 cattegory is not mine',
                                           'user3 descriptions cattegory', True)

    def test_create_cattegory_get_with_no_user(self):
        response = self.client.get(reverse('fino:cattegory_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_cattegory_post_with_no_user(self):
        data = {
            'name': 'teste_cattegory',
            'description': 'test description cattegory',
            'is_receita': True,
        }
        self.response = self.client.post(
            reverse('fino:cattegory_create'), data)
        self.assertEqual(self.response.status_code, 302)

    def test_cattegory_list_get_with_no_user(self):
        response = self.client.get(reverse('fino:cattegory_list'))
        self.assertEqual(response.status_code, 302)

    def test_user_count(self):
        count = User.objects.all().count()
        self.assertEqual(count, 3)

    def test_create_cattegory_view_get_with_user_no_data(self):
        is_logged = self.client.login(username='root', password='root')
        self.assertEqual(is_logged, True)

        response = self.client.get(reverse('fino:cattegory_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_create_cattegory_post_with_new_user_no_data(self):

        is_logged = self.client.login(username='root', password='root')
        self.assertEqual(is_logged, True)

        data = {
            'name': 'teste_cattegory',
            'description': 'test description cattegory',
            'is_receita': True,
        }
        response = self.client.post(reverse('fino:cattegory_create'), data)
        self.assertEqual(response.status_code, 302)

        contas = response.wsgi_request.user.cattegory_set.count()
        self.assertEqual(contas, 1)

    def test_create_cattegory_view_simultaneusly(self):
        is_logged = self.client.login(username='root', password='root')
        self.assertEqual(is_logged, True)

        data = {
            'name': 'teste_cattegory',
            'description': 'test description cattegory',
            'is_receita': True,
        }

        response = self.client.post(reverse('fino:cattegory_create'), data)
        self.assertEqual(response.status_code, 302)

        data = {
            'name': 'teste_cattegory',
            'description': 'test description cattegory',
            'is_receita': False,
        }

        response = self.client.post(reverse('fino:cattegory_create'), data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('fino:cattegory_create'), data)
        self.assertEqual(response.status_code, 302)

        contas = response.wsgi_request.user.cattegory_set.all().count()
        self.assertEqual(contas, 3)

    def test_cattegory_list_view_with_new_user(self):
        self.client.login(username='root', password='root')

        response = self.client.get(reverse('fino:cattegory_list'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['list_objects'].count(), 0)

    def test_cattegory_list_view_with_cattegorys(self):
        self.client.login(username='root', password='root')

        response = self.client.get(reverse('fino:cattegory_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 0)

        create_cattegory(response.wsgi_request.user,
                         'teste', 'description', False)
        response = self.client.get(reverse('fino:cattegory_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 1)

        create_cattegory(response.wsgi_request.user,
                         'teste', 'description', True)
        response = self.client.get(reverse('fino:cattegory_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 2)

    def test_Cattegory_eddit_get_no_user_view(self):

        response = self.client.get(reverse('fino:cattegory_edit',
                                           args=[self.cattegory1.id]))
        self.assertEqual(response.status_code, 302)

    def test_Cattegory_eddit_new_user_acessing_others_cattegory_view(self):
        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:cattegory_edit',
                                           args=[self.cattegory2.id]))
        self.assertEqual(response.status_code, 403)

    def test_Cattegory_eddit_user_acessing_others_cattegory_view(self):

        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:cattegory_list'))
        self.assertEqual(response.status_code, 200)

        create_cattegory(response.wsgi_request.user,
                         'teste', 'description', False)
        response = self.client.get(reverse('fino:cattegory_edit',
                                           args=[self.cattegory2.id]))
        self.assertEqual(response.status_code, 403)

    def test_Cattegory_eddit_user_acessing_own_cattegory_view(self):

        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:cattegory_list'))
        self.assertEqual(response.status_code, 200)

        cattegory = create_cattegory(response.wsgi_request.user,
                                     'teste', 'description', True)
        response = self.client.get(reverse('fino:cattegory_edit',
                                           args=[cattegory.id]))
        self.assertEqual(response.status_code, 200)
        a = response.context['form'].save(commit=False)
        self.assertEqual(cattegory, a)

    def test_delete_anonymous_user(self):
        response = self.client.get(reverse('fino:cattegory_delete',
                                           args=[self.cattegory2.id]))
        self.assertEqual(response.status_code, 302)

    def test_delete_get_others_cattegory_with_new_user(self):
        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:cattegory_delete',
                                           args=[self.cattegory2.id]))
        self.assertEqual(response.status_code, 403)

    def test_delete_get_with_new_user_invalid_cattegory_id(self):
        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:cattegory_delete', args=[0]))
        self.assertEqual(response.status_code, 404)

    def test_delete_get_post_view(self):
        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:cattegory_list'))
        cattegory = create_cattegory(response.wsgi_request.user, 'name_test',
                                     'description', False)
        response = self.client.get(reverse('fino:cattegory_delete',
                                           args=[cattegory.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.wsgi_request.user.cattegory_set.all().count(), 1)

        cattegory = create_cattegory(response.wsgi_request.user,
                                     'name_test', 'description', False)
        response = self.client.get(reverse('fino:cattegory_delete',
                                           args=[cattegory.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.wsgi_request.user.cattegory_set.all().count(), 2)

        response = self.client.post(reverse('fino:cattegory_delete',
                                            args=[cattegory.id]), {'resposta': True})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.wsgi_request.user.cattegory_set.all().count(), 1)
        print("heeeere")
        response = self.client.get(reverse('fino:cattegory_list'))
        self.assertEqual(response.context['list_objects'].count(), 1)


class Transaction_views_test(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            'root', 'teste@gmail.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'teste@gmail.com', 'root2')
        self.user3 = User.objects.create_user(
            'root3', 'test@gmail.com', 'root3')

        self.cat_receita1 = create_cattegory(self.user1, 'salario name',
                                             'description of sallary cattegory', is_receita=True)
        self.cat_receita2 = create_cattegory(self.user1, 'investimento name',
                                             'description of investimento cattegory', is_receita=True)
        self.cat_receita3 = create_cattegory(self.user1, 'doação name',
                                             'description of doação cattegory', is_receita=True)

        self.cat_despesa1 = create_cattegory(self.user1, 'casa name',
                                             'description of casa cattegory', is_receita=False)
        self.cat_despesa2 = create_cattegory(self.user1, 'comida name',
                                             'description of comida cattegory', is_receita=False)
        self.cat_despesa3 = create_cattegory(self.user1, 'roupa name',
                                             'description of roupa cattegory', is_receita=False)

        self.account1 = create_account(
            self.user1, 'carteira', 'description of carteira', 1000.00)
        self.account2 = create_account(
            self.user1, 'banco bradesco', 'description of bradesco', 0)
        self.account3 = create_account(
            self.user1, 'banco inter', 'description of inter', 2.50)

    def test_set_up(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 3)

        cattegory_count = Cattegory.objects.all().count()
        self.assertEqual(cattegory_count, 6)

        account_count = Account.objects.all().count()
        self.assertEqual(account_count, 3)

    def test_create_transaction_get_with_no_user(self):
        response = self.client.get(reverse('fino:transaction_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_transaction_post_with_no_user(self):
        data = {
            'account': self.account1.id,
            'cattegory': self.cat_receita1.id,
            'description': 'description of account1 and cattegory 1',
            'total': 100,
            'is_completed': True,
            'date': date.today(),
        }
        self.response = self.client.post(
            reverse('fino:transaction_create'), data)
        self.assertEqual(self.response.status_code, 302)

    def test_transaction_list_get_with_no_user(self):
        response = self.client.get(reverse('fino:transaction_list'))
        self.assertEqual(response.status_code, 302)

    def test_create_transaction_view_get_with_user_no_data(self):
        is_logged = self.client.login(username='root', password='root')
        self.assertEqual(is_logged, True)

        response = self.client.get(reverse('fino:transaction_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_create_transaction_post_account_adding(self):

        is_logged = self.client.login(username='root', password='root')
        self.assertEqual(is_logged, True)
        total_before = self.account1.total
        data = {
            'account': self.account1.id,
            'cattegory': self.cat_receita1.id,
            'description': 'description of account1 and cattegory 1',
            'total': 100,
            'is_completed': True,
            'date': date.today(),
        }
        response = self.client.post(reverse('fino:transaction_create'), data)

        self.assertEqual(response.status_code, 302)

        transactions_count = Transaction.objects.all().count()
        self.assertEqual(transactions_count, 1)

        account = Account.objects.get(id=self.account1.id)
        self.assertEqual(account.total, total_before + data['total'])

    def test_view_create_transaction_with_negative_and_zero_total_post_account_adding(self):

        is_logged = self.client.login(username='root', password='root')
        self.assertEqual(is_logged, True)
        total_before = self.account1.total
        data = {
            'account': self.account1.id,
            'cattegory': self.cat_receita1.id,
            'description': 'description of account1 and cattegory 1',
            'total': -100,
            'is_completed': True,
            'date': date.today(),
        }
        response = self.client.post(reverse('fino:transaction_create'), data)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Você deve acicionar um valor positivo!")

        data = {
            'account': self.account1.id,
            'cattegory': self.cat_receita1.id,
            'description': 'description of account1 and cattegory 1',
            'total': 0,
            'is_completed': True,
            'date': date.today(),
        }
        response = self.client.post(reverse('fino:transaction_create'), data)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "isso não foi de graça!!")

        transactions_count = Transaction.objects.all().count()
        self.assertEqual(transactions_count, 0)

        account = Account.objects.get(id=self.account1.id)
        self.assertEqual(account.total, total_before)

    def test_create_transaction_view_simultaneusly(self):
        is_logged = self.client.login(username='root', password='root')
        self.assertEqual(is_logged, True)

        total_before = self.account1.total
        data = {
            'account': self.account1.id,
            'cattegory': self.cat_receita1.id,
            'description': 'description of account1 and cattegory 1',
            'total': 100.0,
            'is_completed': True,
            'date': date.today(),
        }
        response = self.client.post(reverse('fino:transaction_create'), data)
        self.assertEqual(response.status_code, 302)

        transactions_count = Transaction.objects.all().count()
        self.assertEqual(transactions_count, 1)

        account = Account.objects.get(id=self.account1.id)
        self.assertEqual(account.total, total_before + data['total'])

        total_before = account.total
        data = {
            'account': self.account1.id,
            'cattegory': self.cat_despesa1.id,
            'description': 'description of account1 and cattegory 1',
            'total': 50,
            'is_completed': True,
            'date': date.today(),
        }
        response = self.client.post(reverse('fino:transaction_create'), data)
        self.assertEqual(response.status_code, 302)

        transactions_count = Transaction.objects.all().count()
        self.assertEqual(transactions_count, 2)

        account = Account.objects.get(id=self.account1.id)
        self.assertEqual(account.total, total_before - data['total'])

        total_before = account.total
        data = {
            'account': self.account1.id,
            'cattegory': self.cat_receita2.id,
            'description': 'description of account1 and cattegory 1',
            'total': 10,
            'is_completed': False,
            'date': date.today(),
        }
        response = self.client.post(reverse('fino:transaction_create'), data)
        self.assertEqual(response.status_code, 302)

        transactions_count = Transaction.objects.all().count()
        self.assertEqual(transactions_count, 3)

        account = Account.objects.get(id=self.account1.id)
        self.assertEqual(account.total, total_before)

    def test_transaction_list_view_with_new_user(self):
        self.client.login(username='root', password='root')

        response = self.client.get(reverse('fino:transaction_list'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['list_objects'].count(), 0)

    def test_transaction_list_view_with_transactions(self):
        self.client.login(username='root', password='root')

        response = self.client.get(reverse('fino:transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 0)

        create_transaction(self.account1, self.cat_receita1, 'description',
                           10.2, True, datetime.date.today())
        response = self.client.get(reverse('fino:transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 1)

        create_transaction(self.account1, self.cat_despesa1, 'description',
                           0.5, False, datetime.date.today())
        response = self.client.get(reverse('fino:transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 2)

        create_transaction(self.account2, self.cat_despesa2, 'description',
                           100, True, datetime.date.today())
        response = self.client.get(reverse('fino:transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 3)

        create_transaction(self.account2, self.cat_receita2, 'description',
                           999, False, datetime.date.today())
        response = self.client.get(reverse('fino:transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['list_objects'].count(), 4)

    def test_Transaction_eddit_get_no_user_view(self):
        transaction1 = create_transaction(
            self.account1, self.cat_receita1, 'description', 100, True, date.today())

        response = self.client.get(
            reverse('fino:transaction_edit', args=[transaction1.id]))
        self.assertEqual(response.status_code, 302)

    def test_Transaction_eddit_new_user_acessing_others_transaction_view(self):
        self.client.login(username='root', password='root')

        transaction1 = create_transaction(
            self.account1, self.cat_receita1, 'description', 100, True, date.today())

        account2 = create_account(self.user2, 'name', 'description', 1000)
        cat2 = create_cattegory(self.user2, 'name', 'description', True)
        transaction2 = create_transaction(
            account2, cat2, 'description', 100, True, date.today())

        response = self.client.get(
            reverse('fino:transaction_edit', args=[transaction2.id]))
        self.assertEqual(response.status_code, 403)

    def test_Transaction_eddit_user_acessing_own_transaction_view(self):
        self.client.login(username='root2', password='root2')
        response = self.client.get(reverse('fino:transaction_list'))
        self.assertEqual(response.status_code, 200)

        account2 = create_account(
            response.wsgi_request.user, 'name', 'description', 1000)
        cat2 = create_cattegory(
            response.wsgi_request.user, 'name', 'description', True)
        transaction = create_transaction(
            account2, cat2, 'description', 100, True, date.today())

        response = self.client.get(
            reverse('fino:transaction_edit', args=[transaction.id]))
        self.assertEqual(response.status_code, 200)
        a = response.context['form'].save(commit=False)
        self.assertEqual(transaction, a)

    def test_delete_anonymous_user(self):

        account2 = create_account(self.user1, 'name', 'description', 1000)
        cat2 = create_cattegory(self.user1, 'name', 'description', True)
        transaction = create_transaction(
            account2, cat2, 'description', 100, True, date.today())

        response = self.client.get(
            reverse('fino:transaction_delete', args=[transaction.id]))
        self.assertEqual(response.status_code, 302)

    def test_delete_get_others_transaction_with_new_user(self):
        self.client.login(username='root2', password='root2')

        account2 = create_account(self.user1, 'name', 'description', 1000)
        cat2 = create_cattegory(self.user1, 'name', 'description', True)
        transaction = create_transaction(
            account2, cat2, 'description', 100, True, date.today())

        response = self.client.get(
            reverse('fino:transaction_delete', args=[transaction.id]))

        self.assertEqual(response.status_code, 403)

    def test_delete_get_with_new_user_invalid_transaction_id(self):
        self.client.login(username='root2', password='root2')
        response = self.client.get(
            reverse('fino:transaction_delete', args=[0]))
        self.assertEqual(response.status_code, 404)

    def test_delete_get_post_with_new_user(self):
        self.client.login(username='root2', password='root2')

        response = self.client.get(reverse('fino:transaction_list'))

        account2 = create_account(
            response.wsgi_request.user, 'name', 'description', 1000)
        cat2 = create_cattegory(
            response.wsgi_request.user, 'name', 'description', True)
        transaction = create_transaction(
            account2, cat2, 'description', 100, True, date.today())

        response = self.client.get(
            reverse('fino:transaction_delete', args=[transaction.id]))
        self.assertEqual(response.status_code, 200)

        transactions = Transaction.objects.filter(
            account__user=response.wsgi_request.user)
        self.assertEqual(transactions.count(), 1)

        transaction = create_transaction(
            account2, cat2, 'description', 100, True, date.today())
        response = self.client.get(
            reverse('fino:transaction_delete', args=[transaction.id]))
        self.assertEqual(response.status_code, 200)
        transactions = Transaction.objects.filter(
            account__user=response.wsgi_request.user)
        self.assertEqual(transactions.count(), 2)

        response = self.client.post(reverse('fino:transaction_delete', args=[
                                    transaction.id]), {'resposta': True})
        self.assertEqual(response.status_code, 302)
        transactions = Transaction.objects.filter(
            account__user=response.wsgi_request.user)
        self.assertEqual(transactions.count(), 1)

        response = self.client.get(reverse('fino:transaction_list'))
        self.assertEqual(response.context['list_objects'].count(), 1)


class HomePageTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root', 'teste@gmail.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'teste@gmail.com', 'root2')
        self.user3 = User.objects.create_user(
            'root3', 'test@gmail.com', 'root3')

        self.cat_receita1 = create_cattegory(self.user1, 'salario name',
                                             'description of sallary cattegory', is_receita=True)
        self.cat_receita2 = create_cattegory(self.user1, 'investimento name',
                                             'description of investimento cattegory', is_receita=True)
        self.cat_receita3 = create_cattegory(self.user1, 'doação name',
                                             'description of doação cattegory', is_receita=True)

        self.cat_despesa1 = create_cattegory(self.user1, 'casa name',
                                             'description of casa cattegory', is_receita=False)
        self.cat_despesa2 = create_cattegory(self.user1, 'comida name',
                                             'description of comida cattegory', is_receita=False)
        self.cat_despesa3 = create_cattegory(self.user1, 'roupa name',
                                             'description of roupa cattegory', is_receita=False)

        self.account1 = create_account(
            self.user1, 'carteira', 'description of carteira', 1000.00)
        self.account2 = create_account(
            self.user1, 'banco bradesco', 'description of bradesco', 0)
        self.account3 = create_account(
            self.user1, 'banco inter', 'description of inter', 2.50)

    def test_get_home_page_no_user(self):
        response = self.client.get(reverse('fino:home_page'))
        self.assertEqual(response.status_code, 302)

    def test_get_home_page_view_new_user(self):

        data = {
            'username': 'username',
            'password1': 'lips1997',
            'password2': 'lips1997',
        }

        response = self.client.post(reverse('fino:signup'), data)

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('fino:home_page'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['saldo'], 0)
        self.assertEqual(response.context['receitas'], None)
        self.assertEqual(response.context['despesas'], None)
        self.assertEqual(response.context['despesas_pendentes'], None)
        self.assertEqual(response.context['receitas_pendentes'], None)
        self.assertEqual(response.context['despesa_por_categoria'], {})

    def test_get_home_page_view_new_user(self):

        data = {
            'username': 'username',
            'password1': 'lips1997',
            'password2': 'lips1997',
        }

        response = self.client.post(reverse('fino:signup'), data)

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('fino:home_page'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['saldo'], 0)
        self.assertEqual(response.context['receitas'], 'None')
        self.assertEqual(response.context['despesas'], 'None')
        self.assertEqual(response.context['despesas_pendentes'], 'None')
        self.assertEqual(response.context['receitas_pendentes'], 'None')

    def test_get_home_page_add_data(self):

        data = {
            'username': 'username',
            'password1': 'lips1997',
            'password2': 'lips1997',
        }

        response = self.client.post(reverse('fino:signup'), data)

        ac = create_account(response.wsgi_request.user,
                            'banco', 'description', 0)

        accounts = response.wsgi_request.user.account_set.all()

        cattegories_receitas = response.wsgi_request.user.cattegory_set.all().filter(is_receita=True)
        cattegories_despesas = response.wsgi_request.user.cattegory_set.all().filter(
            is_receita=False)

        total_before = 0

        print('----accounts')
        print(cattegories_receitas.filter(
            name__startswith='Salário').get().name)

        t_data = {
            'account': accounts.filter(name__startswith='Carteira').get().id,
            'cattegory': cattegories_receitas.filter(name__startswith='Salário').get().id,
            'description': 'description of account1 and cattegory 1',
            'total': 100,
            'is_completed': True,
            'date': date.today(),
        }

        response = self.client.post(reverse('fino:transaction_create'), t_data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('fino:home_page'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['saldo'], total_before + 100)
        self.assertEqual(response.context['receitas'], '100')
        self.assertEqual(response.context['despesas'], 'None')
        self.assertEqual(response.context['despesas_pendentes'], 'None')
        self.assertEqual(response.context['receitas_pendentes'], 'None')

        total_before = response.context['saldo']

        t_data = {
            'account': accounts.filter(name__startswith='Carteira').get().id,
            'cattegory': cattegories_despesas.filter(name__startswith='Roupa').get().id,
            'description': 'description of account1 and cattegory 1',
            'total': 30,
            'is_completed': True,
            'date': date.today(),
        }

        response = self.client.post(reverse('fino:transaction_create'), t_data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('fino:home_page'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['saldo'], 70)
        self.assertEqual(response.context['receitas'], str(100))
        self.assertEqual(response.context['despesas'], str(30))
        self.assertEqual(response.context['despesas_pendentes'], 'None')
        self.assertEqual(response.context['receitas_pendentes'], 'None')
        total_before = response.context['saldo']

        t_data = {
            'account': accounts.filter(name__startswith='Carteira').get().id,
            'cattegory': cattegories_despesas.filter(name__startswith='Moradia').get().id,
            'description': 'description of account1 and cattegory 1',
            'total': 10,
            'is_completed': False,
            'date': date.today(),
        }

        response = self.client.post(reverse('fino:transaction_create'), t_data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('fino:home_page'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['saldo'], total_before)
        self.assertEqual(response.context['receitas'], str(100))
        self.assertEqual(response.context['despesas'], str(30))
        self.assertEqual(response.context['despesas_pendentes'], '10')
        self.assertEqual(response.context['receitas_pendentes'], 'None')
        total_before = response.context['saldo']

        t_data = {
            'account': accounts.filter(name__startswith='Carteira').get().id,
            'cattegory': cattegories_receitas.filter(name__startswith='Salário').get().id,
            'description': 'description of account1 and cattegory 1',
            'total': 150.10,
            'is_completed': False,
            'date': date.today(),
        }

        response = self.client.post(reverse('fino:transaction_create'), t_data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('fino:home_page'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['saldo'], Decimal(total_before))
        self.assertEqual(response.context['receitas'], '100')
        self.assertEqual(response.context['despesas'], str(30))
        self.assertEqual(response.context['despesas_pendentes'], str(10))
        self.assertEqual(
            Decimal(response.context['receitas_pendentes']), Decimal('150.10'))


# faltam--------
# não permitir edição de formulario
# não permitir reenvio de erro de formilario invalido
# detail view tests


class DateUtilTest(TestCase):
    def test_has_date_months(self):
        self.assertEqual(DateUtils.MONTHS['1'], "Janeiro")
        self.assertEqual(DateUtils.MONTHS['12'], "Dezembro")

    def test_get_previous_month(self):
        today = datetime.date(year=2022, month=2, day=1)
        previous_month_date = DateUtils.get_previous_month_date(today)
        self.assertEqual(previous_month_date.month, 1)
        self.assertEqual(previous_month_date.year, 2022)

    def test_get_previous_month(self):
        today = datetime.date(year=2022, month=2, day=1)
        previous_month_date = DateUtils.get_previous_month_date(today)
        self.assertEqual(previous_month_date.month, 1)
        self.assertEqual(previous_month_date.year, 2022)

    def test_get_previous_month_without_parameter(self):
        today = datetime.date.today()
        previous_month_date = DateUtils.get_previous_month_date(today)

        previous_month_date2 = DateUtils.get_previous_month_date()
        self.assertEqual(previous_month_date.month, previous_month_date2.month)
        self.assertEqual(previous_month_date.year, previous_month_date2.year)

    def test_get_next_month_date(self):
        today = datetime.date(year=2022, month=2, day=28)
        previous_month_date = DateUtils.get_next_month_date(today)
        self.assertEqual(previous_month_date.month, 3)
        self.assertEqual(previous_month_date.year, 2022)

    def test_get_next_month_without_parameter(self):
        today = datetime.date.today()
        previous_month_date = DateUtils.get_next_month_date(today)

        previous_month_date2 = DateUtils.get_next_month_date()
        self.assertEqual(previous_month_date.month, previous_month_date2.month)
        self.assertEqual(previous_month_date.year, previous_month_date2.year)

    def test_is_valid_date_with_valid_date(self):
        isValidDate = DateUtils.isValidDate(year=2022, month=5, day=15)
        self.assertTrue(isValidDate)

    def test_is_valid_date_with_invalid_date(self):
        isValidDate = DateUtils.isValidDate(year=2022, month=15, day=20)
        self.assertFalse(isValidDate)
