from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin

from documents.models import Documents
from projects.models import Projects
from .models import *
from staff.models import Staff
from nio_app.utilits import PortalMixin

# Create your views here.

class DivisionList(DetailView, MultipleObjectMixin, PortalMixin):
    """Підрозділи"""
    model = Divisions
    template_name = 'divisions/division.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        div = self.object
        object_list = div.description.split('\n')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['div'] = div
        staff = div.staff_set.only('photo', 'div_id', 'fio').filter(div_id=div.pk)
        try:
            context['boss'] = staff.get(prof__icontains='нач')
        except:
            pass
        context['num_staff'] = staff.count()
        docs = div.div.only('div_id').filter(div_id=div.pk)
        context['num_docs'] = docs.count()
        projects = div.projects_set.only('div_id').filter(div_id=div.pk)
        context['num_projects'] = projects.count()

        """використання PortalMixin"""
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))
