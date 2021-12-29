from django.contrib import admin
from django.urls import path, include
from directory import views

api_path = path("api/", include('directory.api.urls'))

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    api_path
]
