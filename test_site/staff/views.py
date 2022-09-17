from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin

from .models import *
from nio_app.utilits import PortalMixin

# Create your views here.
class StaffList(ListView, PortalMixin):
    """Персонал"""
    model = Staff
    template_name = 'staff/staff.html'
    paginate_by = 5

    def get_queryset(self):
        return Staff.objects.select_related('div')

    def staff_prof(self):
        PROF = []
        for s in Staff.objects.only('prof'):
            if s.prof not in PROF:
                PROF.append(s.prof)
            else:
                continue
        PROFS = list(set(PROF))
        return PROFS

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['staff_prof'] = self.staff_prof()
        context['page'] = ''
        if self.request.GET.get('divs'):
            context['page'] += f"divs={self.request.GET.get('divs')}&"
        if self.request.GET.get('prof'):
            context['page'] += f"prof={self.request.GET.get('prof')}&"
        if self.request.GET.get('sort'):
            context['page'] += f"sort={self.request.GET.get('sort')}&"
        self.divisions = Divisions.objects.only('abr', 'slug')

        """використання PortalMixin"""
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))


class StaffSortList(ListView, PortalMixin):
    """Сортування персоналу"""
    template_name = 'staff/staff_sort.html'
    paginate_by = 0

    def get_queryset(self):
        sorting = ('fio', 'tabel', 'oklad', 'birthday')
        if self.request.GET.get('divs') != None and self.request.GET.get('prof') == None and self.request.GET.get(
                'sort') == None:
            queryset = Staff.objects.filter(
                Q(div_id__in=self.request.GET.getlist("divs"))
            ).order_by('fio')


        elif self.request.GET.get('divs') != None and self.request.GET.get('prof') != None and self.request.GET.get(
                'sort') == None:
            queryset =  Staff.objects.filter(
                Q(div_id__in=self.request.GET.getlist("divs")),
                Q(prof__in=self.request.GET.getlist("prof"))
            ).order_by('fio')


        elif self.request.GET.get('divs') != None and self.request.GET.get('prof') == None and self.request.GET.get(
                'sort') != None:
            for s in sorting:
                if self.request.GET.get('sort') == s:
                    queryset = Staff.objects.filter(
                        Q(div_id__in=self.request.GET.getlist("divs"))
                    ).order_by(s)


        elif self.request.GET.get('divs') != None and self.request.GET.get('prof') != None and self.request.GET.get(
                'sort') != None:
            for s in sorting:
                if self.request.GET.get('sort') == s:
                    queryset = Staff.objects.filter(
                        Q(div_id__in=self.request.GET.getlist("divs")),
                        Q(prof__in=self.request.GET.getlist("prof"))
                    ).order_by(s)


        elif self.request.GET.get('divs') == None and self.request.GET.get('prof') != None and self.request.GET.get(
                'sort') == None:
            queryset = Staff.objects.filter(
                Q(prof__in=self.request.GET.getlist("prof"))
            ).order_by('fio')


        elif self.request.GET.get('divs') == None and self.request.GET.get('prof') != None and self.request.GET.get(
                'sort') != None:
            for s in sorting:
                if self.request.GET.get('sort') == s:
                    queryset = Staff.objects.filter(
                        Q(prof__in=self.request.GET.getlist("prof"))
                    ).order_by(s)


        elif self.request.GET.get('divs') == None and self.request.GET.get('prof') == None and self.request.GET.get(
                'sort') != None:
            for s in sorting:
                if self.request.GET.get('sort') == s:
                    queryset = Staff.objects.order_by(s)


        elif self.request.GET.get('divs') == None and self.request.GET.get('prof') == None and self.request.GET.get(
                'sort') == None:
            queryset = Staff.objects.order_by('fio')
        print('QUERY', queryset)
        return queryset

    def staff_prof(self):
        PROF = []
        for s in Staff.objects.only('prof'):
            if s.prof not in PROF:
                PROF.append(s.prof)
            else:
                continue
        PROFS = list(set(PROF))
        return PROFS

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        context['staff_prof'] = self.staff_prof()
        context['page'] = ''
        if self.request.GET.get('divs'):
            context['page'] += f"divs={self.request.GET.get('divs')}&"
        if self.request.GET.get('prof'):
            context['page'] += f"prof={self.request.GET.get('prof')}&"
        if self.request.GET.get('sort'):
            context['page'] += f"sort={self.request.GET.get('sort')}&"


        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))


class StaffSingle(DetailView, PortalMixin):
    """Окремий працівник"""
    model = Staff
    template_name = 'staff/staff_single.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['single'] = self.object

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))


class SearchStaff(ListView, PortalMixin):
    """Пошук персоналу"""
    template_name = 'staff/staff.html'

    def get_queryset(self):
        search_stf = self.request.GET.get('search_staff').title()
        search_list = Staff.objects.select_related('div').filter(fio__icontains=search_stf)
        if not search_list.exists():
            search = self.request.GET.get('search_staff')
            search_list = Staff.objects.select_related('div').filter(fio__icontains=search)
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['staff'] = self.get_queryset()
        context['page'] = f"search_staff={self.request.GET.get('search_staff')}&"

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))