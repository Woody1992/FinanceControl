import json
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from expenses.models import Expense, Category
from incomes.models import Incomes, Source
from itertools import chain
from usersettings.models import UserSettings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.filter(owner=request.user)
        incomes = Incomes.objects.filter(owner=request.user)

        expenses_and_incomes = sorted(chain(expenses, incomes), key=lambda instance: instance.date, reverse=True)

        paginator = Paginator(list(expenses_and_incomes), 7)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        user_currency = None
        if UserSettings.objects.filter(user=request.user).exists():
            user_currency = UserSettings.objects.get(user=request.user).currency

        context = {
            'all_obj': expenses_and_incomes,
            'currency': user_currency,
            'page_obj': page_obj
        }

        return render(request, 'dashboard/index.html', context)


class SearchDashboardView(View):
    def post(self, request, *args, **kwargs):
        search_srt = json.loads(request.body).get('searchText')  # searchText from js

        expenses = Expense.objects.filter(
            Q(owner=request.user)
            & (Q(amount__istartswith=search_srt)
               | Q(date__icontains=search_srt)
               | Q(description__icontains=search_srt)
               | Q(category__icontains=search_srt)
               )
        )
        incomes = Incomes.objects.filter(
            Q(owner=request.user)
            & (Q(amount__istartswith=search_srt)
               | Q(date__icontains=search_srt)
               | Q(description__icontains=search_srt)
               | Q(source__icontains=search_srt)
               )
        )
        data1 = expenses.values()
        data2 = incomes.values()

        return JsonResponse((list(data1), list(data2)), safe=False)
