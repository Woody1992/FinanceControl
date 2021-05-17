from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search-dashboard/', csrf_exempt(views.SearchDashboardView.as_view()), name='search_dashboard'),
]
