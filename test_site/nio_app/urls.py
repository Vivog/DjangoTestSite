from django.urls import path, re_path

from nio_app import views
from nio_app.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('staff/', views.staff, name='staff'),
    # re_path(r'^divisions/$', views.divisions, name='divisions'),
    path('divisions/', DivisionsList.as_view(), name='divisions'),
    re_path(r'^documents/$', views.documents, name='documents'),
    # path('divisions/<slug:div_slug>/', views.divisions_detail, name='division-detail'),
    path('divisions/<slug:div_slug>/', DivisionsDetailList.as_view(), name='division-detail'),
    # path('add_division/', views.add_division, name='add-division'),
    path('add_division/', AddDivisionView.as_view(), name='add-division'),

]
