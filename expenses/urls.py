from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'expenses'
urlpatterns = [
    path('', views.ExpenceIndexView.as_view(), name='index'),
    path('add-expense', views.AddExpenseView.as_view(), name='add_expense'),
    path('delete-expense/<int:pk>', views.DeleteExpenseView.as_view(), name='delete_expense'),
    path('edit-expense/<int:pk>', views.EditExpenseView.as_view(), name='edit_expense'),
    path('search-expenses/', csrf_exempt(views.SearchRequestView.as_view()), name='search_expenses'),
]