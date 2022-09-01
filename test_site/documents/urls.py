from django.urls import path

from documents.views import *

app_name = 'documents'
urlpatterns = [

    path('docs/', DocsList.as_view(), name='docs'),
    path('download_doc/<int:id>/', download_doc, name='download_doc'),
    path('search_docs/', SearchDoc.as_view(), name='search_docs'),
    path('docs/type/<str:type>/', DocsTypeDetail.as_view(), name='docs_type'),
    path('docs/<slug:slug>/', DocDetail.as_view(), name='doc_single'),


]