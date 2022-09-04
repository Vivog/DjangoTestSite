from django.urls import path

from .views import *

app_name = 'news'
urlpatterns = [
    path('news/', NewsList.as_view(), name='news'),
    path('search_news/', SearchNews.as_view(), name='search_news'),
    path('news/category/<slug:slug>/', NewsCatsDetail.as_view(), name='news_category'),
    path('news/<slug:slug>/', NewsDetail.as_view(), name='news_single'),
    path('news/<slug:slug>/review/', AddReviewNews.as_view(), name='add_review_news'),
]