from django.urls import path

from .views import *

app_name = 'staff'
urlpatterns = [

    path('staff/', StaffList.as_view(), name='staff'),
    path('search_staff/', SearchStaff.as_view(), name='search_staff'),
    path('staff/filter/', StaffSortList.as_view(), name='staff_sort'),
    path('staff/<slug:slug>/', StaffSingle.as_view(), name='staff_single'),


]