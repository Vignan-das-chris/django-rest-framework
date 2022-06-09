from django.urls import re_path as url, path
from climates import views

urlpatterns = [

    path('login/', views.user_login, name='login'),
    url(r'^', views.climate_list),
]
