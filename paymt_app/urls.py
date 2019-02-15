from django.contrib import admin
from django.urls import path, include

#from tx_list import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('tx_list.urls')),
]
