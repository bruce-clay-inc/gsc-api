from django.contrib import admin
from django.urls import path
from gsc.views import SyncDataView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sync/', SyncDataView.as_view(), name='sync'),
]
