from django.db.models import Q
from django.http import FileResponse
from django.views.generic import ListView, DetailView

from nio_app.utilits import PortalMixin
from .models import *


# Create your views here.
class DocsList(ListView, PortalMixin):
    model = Documents
    template_name = 'documents/docs.html'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['docs_all'] = Documents.objects.only('year', 'slug', 'number')

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))


class DocDetail(DetailView, PortalMixin):
    model = Documents
    template_name = 'documents/doc_single.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['docs_all'] = Documents.objects.only('year', 'slug', 'number')

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))


def download_doc(request, id):
    from pathlib import Path
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = str(Documents.objects.get(pk=id).doc)
    filename = Path(BASE_DIR, 'media/', path)
    # if not filename.exists():
    #     filename = Path(BASE_DIR, 'static/site_app/cv', 'Savushkin_CV.pdf')
    return FileResponse(open(filename, 'rb'), as_attachment=True)


class DocsTypeDetail(ListView, PortalMixin):
    model = Documents
    template_name = 'documents/docs.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['docs_all'] = Documents.objects.only('year', 'slug', 'number')

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_queryset(self):
        q = Q(type=self.kwargs['type'])
        return Documents.objects.filter(q)


class SearchDoc(ListView, PortalMixin):
    template_name = 'documents/docs.html'
    paginate_by = 5

    def get_queryset(self):
        search_list = Documents.objects.filter(name__icontains=self.request.GET.get('search_docs'))
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['docs_all'] = Documents.objects.only('year', 'slug', 'number')
        context['page'] = f"search_docs={self.request.GET.get('search_docs')}&"

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))
