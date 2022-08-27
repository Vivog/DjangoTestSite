from django.urls import path

from nio_app.views import *

app_name = 'nio_app'
urlpatterns = [
    path('', Index.as_view(), name='index_portal'),
    path('search/', SearchMain.as_view(), name='search'),
    path('search/<str:cat>/<str:search>/', SearchCat.as_view(), name='search_cat'),
    path('login/', LoginUser.as_view(), name='login'),
    path('reg/', RegisterUser.as_view(), name='registration'),
    path('logout/', logout_user, name='logout'),
    path('#divs/', Index.as_view(), name='divs'),
    path('division/<slug:slug>/', DivisionList.as_view(), name='division'),
    path('staff/', StaffList.as_view(), name='staff'),
    path('staff/<slug:slug>/', StaffSingle.as_view(), name='staff_single'),
    path('search_staff/', SearchStaff.as_view(), name='search_staff'),
    path('staff/filter/', StaffSortList.as_view(), name='filter'),
    path('publics/', PubsList.as_view(), name='publics'),
    path('search_pub/', SearchPub.as_view(), name='search_pub'),
    path('publics/category/<slug:slug>/', PubsCatsDetail.as_view(), name='publics_category'),
    path('publics/<slug:slug>/', PubsDetail.as_view(), name='public_single'),
    path('publics/<slug:slug>/review/', AddReviewPub.as_view(), name='add_review_pub'),
    path('news/', NewsList.as_view(), name='news'),
    path('search_news/', SearchNews.as_view(), name='search_news'),
    path('news/category/<slug:slug>/', NewsCatsDetail.as_view(), name='news_category'),
    path('news/<slug:slug>/', NewsDetail.as_view(), name='news_single'),
    path('news/<slug:slug>/review/', AddReviewNews.as_view(), name='add_review_news'),
    path('docs/', DocsList.as_view(), name='docs'),
    path('download_doc/<int:id>/', download_doc, name='download_doc'),
    path('search_docs/', SearchDoc.as_view(), name='search_docs'),
    path('docs/type/<str:type>/', DocsTypeDetail.as_view(), name='docs_type'),
    path('docs/<slug:slug>/', DocDetail.as_view(), name='doc_single'),
    path('contacts/', contacts, name='contacts'),
    path('cats/', cats, name='cats'),

]

