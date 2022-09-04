from django.urls import path

from .views import *

app_name = 'divisions'
urlpatterns = [
    path('division/<slug:slug>/', DivisionList.as_view(), name='division'),
]