from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expence/', include('expenses.urls', namespace='expenses')),
    path('', include('dashboard.urls', namespace='dashboard')),
    path('income/', include('incomes.urls', namespace='incomes')),
    path('', include('usersettings.urls', namespace='usersettings')),
    path('authentication/', include('authentication.urls', namespace='authentication')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
