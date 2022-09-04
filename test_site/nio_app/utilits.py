from django.db.models import Count

from documents.models import Documents
from divisions.models import Divisions
from projects.models import Projects

class PortalMixin:
    paginate_by = 2
    def docs_name(self):
        doc = (
            ("M", "Методики"), ("P", "Паспорти"), ("KE", "Керівництва з експлуатації"), ("TD", "Техничні довідки"),
            ("ZT", "Технічні звіти"), ("TI", "Технологічні інструкції"), ("I", "Інше"))
        docs_type = Documents.objects.values('type').annotate(Count('type'))
        dt = []
        for i in doc:
            for t in docs_type:
                if t['type'] in i:
                    add = [i[0], i[1], t['type__count']]
                    dt.append(add)
                else:
                    continue
        return dt

    divisions = Divisions.objects.prefetch_related('locs', 'coops', 'theses')

    def get_user_context(self, **kwargs):
        context = kwargs
        context['divisions'] = self.divisions
        context['dt'] = self.docs_name()
        context['projects'] = Projects.objects.only('name')
        context['page'] = ''
        return context


