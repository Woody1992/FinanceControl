from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'incomes'
urlpatterns = [
    path('', views.IncomeIndexView.as_view(), name='index'),
    path('add-income', views.AddIncomeView.as_view(), name='add_income'),
    path('delete-income/<int:pk>', views.DeleteIncomeView.as_view(), name='delete_income'),
    path('edit-income/<int:pk>', views.EditIncomeView.as_view(), name='edit_income'),
    path('search-income/', csrf_exempt(views.SearchIncomeView.as_view()), name='search_income'),
]