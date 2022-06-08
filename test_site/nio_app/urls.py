from django.urls import path, re_path

from nio_app import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^divisions/$', views.divisions, name='divisions'),
    re_path(r'^documents/$', views.documents, name='documents'),
    path('divisions/<int:div_id>/', views.divisions_detail, name='division-detail'),
    # re_path(r'^divisions/$', views.DivisionsListView.as_view(), name='divisions'),
    # re_path(r'^divisions/(?P<pk>\d+)$', views.DivisionsDetailView.as_view(), name='division-detail'),
    # re_path(r'^staff/$', views.StaffListView.as_view(), name='staff'),
    # # re_path(r'^divisions/(?P<pk>\d+)$/(?P<apk>\d+)', views.Staff_DivListView.as_view(), name='staff'),
    # re_path(r'^staff/(?P<pk>\d+)$', views.StaffDetailView.as_view(), name='staff-detail'),
]
