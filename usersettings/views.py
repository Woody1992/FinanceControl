from django.contrib import messages
from django.shortcuts import render
from django.views import View
import json
from django.conf import settings
from . models import UserSettings


class CurrencySettingsView(View):
    currency_data = []
    file_path = settings.BASE_DIR / 'currencies.json'
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    def get(self, request, *args, **kwargs):
        user_preferences = None
        if UserSettings.objects.filter(user=request.user).exists():
            user_preferences = UserSettings.objects.get(user=request.user)

        content = {
            'user_preferences': user_preferences,
            'currencies': CurrencySettingsView.currency_data
        }

        return render(request, 'usersettings/settings.html', content)

    def post(self, request, *args, **kwargs):
        print(request.POST['currency'])
        currency = request.POST['currency']
        user_preferences = None
        if UserSettings.objects.filter(user=request.user).exists():
            user_preferences = UserSettings.objects.get(user=request.user)
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserSettings.objects.create(user=request.user, currency=currency)
            user_preferences.currency = currency

        context = {
            'user_preferences': user_preferences,
            'currencies': CurrencySettingsView.currency_data
        }
        messages.success(request, 'Currency changed to ' + user_preferences.currency)
        return render(request, 'usersettings/settings.html', context)


class AccountSettingView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'usersettings/account_settings.html')
