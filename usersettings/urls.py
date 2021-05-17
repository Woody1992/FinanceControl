from django.urls import path
from . import views


app_name = 'usersettings'
urlpatterns = [
    path('settings/', views.CurrencySettingsView.as_view(), name='settings'),
    path('account-settings/', views.AccountSettingView.as_view(), name='account_settings')
]
