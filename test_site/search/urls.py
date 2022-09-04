from django.urls import path

from .views import *

app_name = 'search'
urlpatterns = [

    path('search/', SearchMain.as_view(), name='search'),
    path('search/<str:cat>/<str:search>/', SearchCat.as_view(), name='search_cat'),

]