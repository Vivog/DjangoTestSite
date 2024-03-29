"""test_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from nio_app.views import pageNotFound
from test_site import settings

urlpatterns = [
    path('admin/', admin.site.urls, name=admin),
    path('grappelli/', include('grappelli.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('nio_app.urls')),
    path('search/', include('search.urls')),
    path('divisions/', include('divisions.urls')),
    path('staff/', include('staff.urls')),
    path('documents/', include('documents.urls')),
    path('projects/', include('projects.urls')),
    path('publics/', include('publics.urls')),
    path('news/', include('news.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    import debug_toolbar.urls
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = pageNotFound
