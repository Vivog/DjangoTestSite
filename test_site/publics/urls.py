from django.urls import path

from .views import *

app_name = 'publics'
urlpatterns = [

    path('publics/', PubsList.as_view(), name='publics'),
    path('search_pub/', SearchPub.as_view(), name='search_pub'),
    path('publics/category/<slug:slug>/', PubsCatsDetail.as_view(), name='publics_category'),
    path('publics/<slug:slug>/', PubsDetail.as_view(), name='public_single'),
    path('publics/<slug:slug>/review/', AddReviewPub.as_view(), name='add_review_pub'),

]