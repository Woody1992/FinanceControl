from django.shortcuts import render, redirect
from django.views import View
from .models import Expense, Category
from django.contrib import messages
from usersettings.models import UserSettings
from django.utils.timezone import now
from django.core.paginator import Paginator
import json
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin


class ExpenceIndexView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.filter(owner=request.user)
        # expenses_sum = Expense.objects.filter(owner=request.user).aggregate(Sum('amount'))
        # for i in expenses_sum.values():
        #     print(i)

        paginator = Paginator(expenses, 7)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        user_currency = None
        if UserSettings.objects.filter(user=request.user).exists():
            user_currency = UserSettings.objects.get(user=request.user).currency
        context = {
            'expenses': expenses,
            'currency': user_currency,
            'page_obj': page_obj
        }
        return render(request, 'expenses/index.html', context)


class AddExpenseView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'values': request.POST,
        }
        return render(request, 'expenses/add_expense.html', context)

    def post(self, request, *args, **kwargs):
        categories = Category.objects.all()
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']
        user_currency = None
        if UserSettings.objects.filter(user=request.user).exists():
            user_currency = UserSettings.objects.get(user=request.user).currency

        context = {
            'categories': categories,
            'values': request.POST,
            'currency': user_currency
        }

        if not date:
            date = now()
        if not amount:
            messages.error(request, 'Amount must be added')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            category=category,
            date=date)
        if user_currency:
            messages.success(request, f'Expense for { user_currency[:4]}{amount} has been added')
        else:
            messages.success(request, f'Expense for {amount} has been added')
        return redirect('expenses:index')


class EditExpenseView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk, *args, **kwargs):
        expense = Expense.objects.get(id=pk, owner=request.user)
        categories = Category.objects.all()
        context = {
            'expense': expense,
            'categories': categories
        }
        return render(request, 'expenses/edit_expense.html', context)

    def post(self, request, pk, *args, **kwargs):
        expense = Expense.objects.get(id=pk, owner=request.user)
        categories = Category.objects.all()
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']

        context = {
            'expense': expense,
            'categories': categories
        }
        if not date:
            date = now()
        if not amount:
            expense.amount = None
            messages.error(request, 'Amount must be added')
            return render(request, 'expenses/edit_expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()

        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses:index')


class DeleteExpenseView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk, *args, **kwargs):
        expense = Expense.objects.get(id=pk, owner=request.user)
        expense.delete()
        messages.success(request, 'Expense has been deleted')
        return redirect('expenses:index')


class SearchRequestView(View):
    def post(self, request, *args, **kwargs):
        search_srt = json.loads(request.body).get('searchText')  # searchText from js

        expenses = Expense.objects.filter(
            Q(owner=request.user)
            & (Q(amount__istartswith=search_srt)
               | Q(date__istartswith=search_srt)
               | Q(description__icontains=search_srt)
               | Q(category__icontains=search_srt)
               )
        )
        data = expenses.values()

        return JsonResponse(list(data), safe=False)
