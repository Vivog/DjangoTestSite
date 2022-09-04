from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.list import MultipleObjectMixin

from divisions.models import Divisions
from nio_app.models import Categories
from nio_app.utilits import PortalMixin
from .forms import ReviewNewsForm
from .models import *


# Create your views here.
class NewsList(ListView, PortalMixin):
    model = News
    template_name = 'news/news.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['cats'] = Categories.objects.filter(news__gte=1).distinct()
        context['news'] = News.objects.only('name', 'slug', 'photo_1')

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))


class NewsDetail(DetailView, MultipleObjectMixin, PortalMixin):
    model = News
    template_name = 'news/news_single.html'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.object.text.split('\n')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['cats'] = Categories.objects.filter(news__gte=1).distinct()
        context['news'] = News.objects.only('name', 'slug', 'photo_1')

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))


class NewsCatsDetail(DetailView, PortalMixin):
    model = Categories
    template_name = 'news/news_category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['cats'] = Categories.objects.filter(news__gte=1).distinct()
        context['news'] = News.objects.only('name', 'slug', 'photo_1')

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_queryset(self):
        return Categories.objects.filter(slug=self.kwargs['slug'])


class AddReviewNews(View):
    def post(self, request, slug):
        form = ReviewNewsForm(request.POST)
        news = News.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.news = news
            form.save()
        return redirect(news.get_absolute_url())


class SearchNews(ListView, PortalMixin):
    template_name = 'news/news.html'
    paginate_by = 1

    def get_queryset(self):
        search_list = News.objects.filter(name__icontains=self.request.GET.get('search_news'))
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['new'] = self.get_queryset()
        context['page'] = f"search_news={self.request.GET.get('search_news')}&"

        context['cats'] = Categories.objects.filter(news__gte=1).distinct()
        context['news'] = News.objects.only('name', 'slug', 'photo_1')

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))
