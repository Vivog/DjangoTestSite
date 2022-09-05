from django.urls import path

from .views import *

app_name = 'projects'
urlpatterns = [

    path('projects/', ProjectsList.as_view(), name='projects'),
    path('download_doc/<int:id>/', download_doc, name='download_doc'),
    path('search_project/', SearchProject.as_view(), name='search_project'),
    path('projects/category/<slug:slug>/', ProjectsCatsDetail.as_view(), name='project_category'),
    path('projects/<slug:slug>/', ProjectsDetail.as_view(), name='project_single'),
    path('projects/<slug:slug>/review/', AddReviewProject.as_view(), name='add_review_project'),

]