from django.urls import path, re_path

from nio_app import views
from nio_app.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('staff/', Staff_DivList.as_view(), name='staff'),
    path('staff/<slug:div_slug>/', StaffDetailList.as_view(), name='div_staff-detail'),
    path('staff/<slug:div_slug>/<slug:staff_slug>/', PersonDetailList.as_view(), name='person-detail'),
    path('divisions/', DivisionsList.as_view(), name='divisions'),
    path('divisions/<slug:div_slug>/', DivisionsDetailList.as_view(), name='division-detail'),
    path('add_division/', AddDivisionView.as_view(), name='add-division'),
    re_path(r'^documents/$', views.documents, name='documents'),
    # path('staff/', views.staff, name='staff'),
    # re_path(r'^divisions/$', views.divisions, name='divisions'),
    # path('divisions/<slug:div_slug>/', views.divisions_detail, name='division-detail'),
    # path('add_division/', views.add_division, name='add-division'),

]