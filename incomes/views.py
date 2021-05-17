from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.utils.timezone import now
from django.db.models import Q
from usersettings.models import UserSettings
from .models import Incomes, Source
from django.contrib.auth.mixins import LoginRequiredMixin


class IncomeIndexView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        incomes = Incomes.objects.filter(owner=request.user)
        paginator = Paginator(incomes, 3)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        user_currency = None
        if UserSettings.objects.filter(user=request.user).exists():
            user_currency = UserSettings.objects.get(user=request.user).currency
        context = {
            'incomes': incomes,
            'currency': user_currency,
            'page_obj': page_obj
        }

        return render(request, 'incomes/index.html', context)


class AddIncomeView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        sources = Source.objects.all()
        context = {
            'sources': sources,
        }
        return render(request, 'incomes/add_income.html', context)

    def post(self, request, *args, **kwargs):
        sources = Source.objects.all()
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']
        user_currency = None
        if UserSettings.objects.filter(user=request.user).exists():
            user_currency = UserSettings.objects.get(user=request.user).currency
        context = {
            'sources': sources,
            'values': request.POST,
            'currency': user_currency
        }

        if not date:
            date = now()

        if not amount:
            messages.error(request, 'Amount must be added')
            return render(request, 'incomes/add_income.html', context)

        Incomes.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            source=source,
            date=date)
        if user_currency:
            messages.success(request, f'Income for {user_currency[:4]}{amount} has been added')
        else:
            messages.success(request, f'Income for {amount} has been added')
        return redirect('incomes:index')


class DeleteIncomeView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk, *args, **kwargs):
        income = Incomes.objects.get(id=pk, owner=request.user)
        income.delete()
        messages.success(request, 'Income has been deleted')
        return redirect('incomes:index')


class EditIncomeView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk, *args, **kwargs):
        income = Incomes.objects.get(id=pk, owner=request.user)
        sources = Source.objects.all()

        context = {
            'income': income,
            'sources': sources
        }
        return render(request, 'incomes/edit_income.html', context)

    def post(self, request, pk, *args, **kwargs):
        income = Incomes.objects.get(id=pk, owner=request.user)
        sources = Source.objects.all()
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']

        context = {
            'income': income,
            'sources': sources,

        }

        if not date:
            date = now()

        if not amount:
            income.amount = None
            messages.error(request, 'Amount must be added')
            return render(request, 'incomes/edit_income.html', context)

        income.owner = request.user
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description

        income.save()

        messages.success(request, 'Income updated  successfully')
        return redirect('incomes:index')


class SearchIncomeView(View):
    def post(self, request, *args, **kwargs):
        search_srt = json.loads(request.body).get('searchText')  # searchText from js

        incomes = Incomes.objects.filter(
            Q(owner=request.user)
            & (Q(amount__istartswith=search_srt)
               | Q(date__istartswith=search_srt)
               | Q(description__icontains=search_srt)
               | Q(source__icontains=search_srt)
               )
        )
        data = incomes.values()

        return JsonResponse(list(data), safe=False)

