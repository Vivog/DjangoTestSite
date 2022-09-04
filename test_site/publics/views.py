from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.list import MultipleObjectMixin

from .forms import ReviewPubForm
from .models import *
from divisions.models import Divisions
from nio_app.models import Categories

from nio_app.utilits import PortalMixin

# Create your views here.
class PubsList(ListView, PortalMixin):
    """Публікації"""
    model = Publications
    template_name = 'publics/publics.html'
    queryset = Publications.objects.prefetch_related('author', 'category')
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=self.object_list, **kwargs)
        context['cats'] = Categories.objects.filter(publications__gte=1).distinct()
        context['pubs'] = Publications.objects.only('name', 'slug', 'photo_1')

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))


class PubsDetail(DetailView, MultipleObjectMixin, PortalMixin):
    """Окрема публікація"""
    model = Publications
    template_name = 'publics/public_single.html'
    paginate_by = 6

    def get_object(self, queryset=None):
        return Publications.objects.prefetch_related('category', 'author', 'reviewspubs_set').get(slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.object.text.split('\n')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['cats'] = Categories.objects.filter(publications__gte=1).distinct()
        context['pubs'] = Publications.objects.only('name', 'slug', 'photo_1')

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))


class PubsCatsDetail(DetailView, PortalMixin):
    model = Categories
    template_name = 'publics/publics_category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = Publications.objects.prefetch_related('category', 'author')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['cats'] = Categories.objects.filter(publications__gte=1).distinct()
        context['pubs'] = Publications.objects.only('name', 'slug', 'photo_1')

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))


class AddReviewPub(View):

    def post(self, request, slug):
        form = ReviewPubForm(request.POST)
        pub = Publications.objects.prefetch_related('category', 'author').get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
                print(form.parent_id)
            form.pub = pub
            form.save()
        return redirect(pub.get_absolute_url())


class SearchPub(ListView, PortalMixin):
    template_name = 'publics/publics.html'

    def get_queryset(self):
        search_list = Publications.objects.select_related('div').filter(name__icontains=self.request.GET.get('search_pub'))
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['cats'] = Categories.objects.filter(publications__gte=1).distinct()
        context['pubs'] = Publications.objects.only('name', 'slug', 'photo_1')
        context['page'] = f"search_pub={self.request.GET.get('search_pub')}&"

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))