from django.contrib import admin
from django.urls import path
from gsc.views import SyncDataView
from gsc.views import QueryDataView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sync/', SyncDataView.as_view(), name='sync'),
    path('query/', QueryDataView.as_view(), name='query_data'),
]
