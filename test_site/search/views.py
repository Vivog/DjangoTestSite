from django.views.generic import ListView

from documents.models import Documents
from news.models import News
from projects.models import Projects
from publics.models import Publications
from staff.models import Staff
from divisions.models import Divisions

from nio_app.utilits import PortalMixin

# Create your views here.

class SearchMain(ListView, PortalMixin):
    """Пошук загальний"""
    template_name = 'search/search.html'
    paginate_by = 5

    def get_queryset(self):
        search_stf = self.request.GET.get('search').title()
        search_list = []
        search_list.append(Divisions.objects.only('name').filter(name__icontains=search_stf))
        search_list.append(Divisions.objects.only('abr').filter(abr__icontains=search_stf))
        search_list.append(Staff.objects.only('fio').filter(fio__icontains=search_stf))
        search_list.append(Documents.objects.only('name').filter(name__icontains=search_stf))
        search_list.append(Projects.objects.only('name').filter(name__icontains=search_stf))
        search_list.append(Publications.objects.only('name').filter(name__icontains=search_stf))
        search_list.append(News.objects.only('name').filter(name__icontains=search_stf))
        search = self.request.GET.get('search')
        search_list.append(Divisions.objects.only('name').filter(name__icontains=search))
        search_list.append(Divisions.objects.only('abr').filter(abr__icontains=search))
        search_list.append(Staff.objects.only('fio').filter(fio__icontains=search))
        search_list.append(Documents.objects.only('name').filter(name__icontains=search))
        search_list.append(Projects.objects.only('name').filter(name__icontains=search))
        search_list.append(Publications.objects.only('name').filter(name__icontains=search))
        search_list.append(News.objects.only('name').filter(name__icontains=search))
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        search_all = []
        for s_c in self.get_queryset():
            for s in s_c:
                if s:
                    search_all.append((s._meta.verbose_name_plural, s, s.slug))
                else:
                    continue
        print('SE_ALL', search_all)
        object_list = search_all
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_text'] = self.request.GET.get('search')
        context['models'] = [[Divisions._meta.verbose_name_plural, Divisions.objects.all().count()],
                     [Staff._meta.verbose_name_plural, Staff.objects.all().count()],
                     [Documents._meta.verbose_name_plural, Documents.objects.all().count()],
                     [Projects._meta.verbose_name_plural, Projects.objects.all().count()],
                     [Publications._meta.verbose_name_plural, Publications.objects.all().count()],
                     [News._meta.verbose_name_plural, News.objects.all().count()]]
        for m in context['models']:
            m.append(context['search_text'])
        context['page'] = f"search={self.request.GET.get('search')}&"

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))


class SearchCat(ListView, PortalMixin):
    """Пошук за категорією"""
    template_name = 'search/search_cat.html'
    paginate_by = 5

    def get_queryset(self):
        search_stf = self.kwargs['search'].title()
        search_list = []
        if self.kwargs['cat'] == 'підрозділи':
            search_list.append(Divisions.objects.only('name').filter(name__icontains=search_stf))
            search_list.append(Divisions.objects.only('abr').filter(abr__icontains=search_stf))
            search = self.kwargs['search']
            search_list.append(Divisions.objects.only('name').filter(name__icontains=search))
            search_list.append(Divisions.objects.only('abr').filter(abr__icontains=search))
        elif self.kwargs['cat'] == 'персонал':
            search_list.append(Staff.objects.only('fio').filter(fio__icontains=search_stf))
            search = self.kwargs['search']
            search_list.append(Staff.objects.only('fio').filter(fio__icontains=search))
        elif self.kwargs['cat'] == 'документація':
            search_list.append(Documents.objects.only('name').filter(name__icontains=search_stf))
            search = self.kwargs['search']
            search_list.append(Documents.objects.only('name').filter(name__icontains=search))
        elif self.kwargs['cat'] == 'проекти':
            search_list.append(Projects.objects.only('name').filter(name__icontains=search_stf))
            search = self.kwargs['search']
            search_list.append(Projects.objects.only('name').filter(name__icontains=search))
        elif self.kwargs['cat'] == 'публікації':
            search_list.append(Publications.objects.only('name').filter(name__icontains=search_stf))
            search = self.kwargs['search']
            search_list.append(Publications.objects.only('name').filter(name__icontains=search))
        elif self.kwargs['cat'] == 'новини':
            search_list.append(News.objects.only('name').filter(name__icontains=search_stf))
            search = self.kwargs['search']
            search_list.append(News.objects.only('name').filter(name__icontains=search))

        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        search_all = []
        print('SEARCH', self.get_queryset())
        for s_c in self.get_queryset():
            for s in s_c:
                if s:
                    search_all.append((s._meta.verbose_name_plural, s, s.slug))
                else:
                    continue
        if self.get_queryset():
            object_list = search_all
            context = super().get_context_data(object_list=object_list, **kwargs)
            context['models'] = []
            if self.kwargs['cat'] == 'підрозділи':
                context['models'].append([Divisions._meta.verbose_name_plural, Divisions.objects.all().count()])
            elif self.kwargs['cat'] == 'персонал':
                context['models'].append([Staff._meta.verbose_name_plural, Staff.objects.all().count()])
            elif self.kwargs['cat'] == 'документація':
                context['models'].append([Documents._meta.verbose_name_plural, Documents.objects.all().count()])
            elif self.kwargs['cat'] == 'проекти':
                context['models'].append([Projects._meta.verbose_name_plural, Projects.objects.all().count()])
            elif self.kwargs['cat'] == 'публікації':
                context['models'].append([Publications._meta.verbose_name_plural, Publications.objects.all().count()])
            elif self.kwargs['cat'] == 'новини':
                context['models'].append([News._meta.verbose_name_plural, News.objects.all().count()])
        else:
            context = super().get_context_data(object_list=None, **kwargs)
        context['search_text'] = self.request.GET.get('search')
        context['cat'] = self.kwargs['cat']
        context['s_text'] = self.kwargs['search']
        context['page'] = f"search={self.request.GET.get('search')}&"

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))