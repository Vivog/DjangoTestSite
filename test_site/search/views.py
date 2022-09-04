from django.views.generic import ListView

from documents.models import Documents
from news.models import News
from projects.models import Projects
from publics.models import Publications
from staff.models import Staff
from divisions.models import Divisions

from nio_app.utilits import PortalMixin

# Create your views here.
CONTEXT = {}
CONTEXT['models'] = [
    [Divisions._meta.verbose_name_plural, Divisions.objects.all().count()],
                     [Staff._meta.verbose_name_plural, Staff.objects.all().count()],
                     [Documents._meta.verbose_name_plural, Documents.objects.all().count()],
                     [Projects._meta.verbose_name_plural, Projects.objects.all().count()],
                     [Publications._meta.verbose_name_plural, Publications.objects.all().count()],
                     [News._meta.verbose_name_plural, News.objects.all().count()]]

class SearchMain(ListView):
    """Пошук загальний"""
    template_name = 'search/search.html'
    paginate_by = 5

    def get_queryset(self):
        search_list = []
        search_list.append(Divisions.objects.filter(name__icontains=self.request.GET.get('search')))
        search_list.append(Divisions.objects.filter(abr__icontains=self.request.GET.get('search')))
        search_list.append(Staff.objects.filter(fio__icontains=self.request.GET.get('search')))
        search_list.append(Documents.objects.filter(name__icontains=self.request.GET.get('search')))
        # search_list.append(Documents.objects.filter(description__icontains=self.request.GET.get('search')))
        search_list.append(Projects.objects.filter(name__icontains=self.request.GET.get('search')))
        search_list.append(Publications.objects.filter(name__icontains=self.request.GET.get('search')))
        # search_list.append(Publications.objects.filter(description__icontains=self.request.GET.get('search')))
        search_list.append(News.objects.filter(name__icontains=self.request.GET.get('search')))
        # search_list.append(News.objects.filter(description__icontains=self.request.GET.get('search')))
        print('SEARCH', search_list)
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        search_all = []
        for s_c in self.get_queryset():
            for s in s_c:
                if s:
                    print('S_C', s)
                    search_all.append((s._meta.verbose_name_plural, s, s.slug))
                else:
                    continue
        object_list = search_all
        print('SEARCHING ALL', object_list)
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(CONTEXT)
        # context['searching'] = object_list
        # for s_c in self.get_queryset():
        #     for s in s_c:
        #         if s:
        #             print('S_C', s)
        #             context['searching'].append((s._meta.verbose_name_plural, s, s.slug))
        #         else:
        #             continue
        # print('SEARCHING ALL', context['searching'])
        context['search_text'] = self.request.GET.get('search')
        context['models'] = CONTEXT['models']
        for m in context['models']:
            m.append(context['search_text'])
        context['page'] = f"search={self.request.GET.get('search')}&"
        return context


class SearchCat(ListView):
    """Пошук за категорією"""
    template_name = 'search/search_cat.html'
    paginate_by = 5

    def get_queryset(self):
        if self.kwargs['cat'] == 'підрозділи':
            return Divisions.objects.filter(name__icontains=self.kwargs['search'])
        elif self.kwargs['cat'] == 'персонал':
            return Staff.objects.filter(fio__icontains=self.kwargs['search'])
        elif self.kwargs['cat'] == 'документація':
            return Documents.objects.filter(name__icontains=self.kwargs['search'])
        elif self.kwargs['cat'] == 'проекти':
            return Projects.objects.filter(name__icontains=self.kwargs['search'])
        elif self.kwargs['cat'] == 'публікації':
            return Publications.objects.filter(name__icontains=self.kwargs['search'])
        elif self.kwargs['cat'] == 'новини':
            return News.objects.filter(name__icontains=self.kwargs['search'])

    def get_context_data(self, *, object_list=None, **kwargs):
        search_all = []
        for s in self.get_queryset():
            if s:
                print('S_C', s)
                search_all.append((s._meta.verbose_name_plural, s, s.slug))
            else:
                continue
        object_list = search_all
        print('SEARCHING ALL', object_list)
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(CONTEXT)
        context['search_text'] = self.request.GET.get('search')
        context['cat'] = self.kwargs['cat']
        context['s_text'] = self.kwargs['search']
        context['page'] = f"search={self.request.GET.get('search')}&"
        return context