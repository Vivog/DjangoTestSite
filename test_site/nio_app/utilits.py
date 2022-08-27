from django.db.models import Count

from .models import *

class PortalMixin():
    paginate_by = 2

class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['main'] = Main.objects.all().prefetch_related('divisions')
        context['div'] = Divisions.objects.all().prefetch_related('locs', 'coops', 'theses')
        context['pubs'] = Publications.objects.all().select_related('div').prefetch_related('author', 'category')
        context['pubs_rev'] = ReviewsPubs.objects.all().select_related('parent', 'pub')
        context['new'] = News.objects.all().prefetch_related('category')
        context['new_all'] = News.objects.all().prefetch_related('category')
        context['news_rev'] = ReviewsNews.objects.all().select_related('parent', 'news')
        context['staff'] = Staff.objects.all().select_related('div')
        STAFF = Staff.objects.all()
        PROF = []
        for s in STAFF:
            if s.prof not in PROF:
                PROF.append(s.prof)
            else:
                continue
        PROFS = list(set(PROF))
        trans_table = str.maketrans(
            'ABCEHKMOPTXacekmopuxyi',
            'АВСЕНКМОРТХасекморихуі',
        )
        PROFS.sort(key=lambda s: s[0].translate(trans_table))
        context['staff_prof'] = PROFS
        context['projects'] = Projects.objects.all().select_related('div').prefetch_related('author', 'category')
        context['cats'] = Categories.objects.all()
        context['docs_all'] = Documents.objects.all().select_related('div').prefetch_related('author')
        context['doc'] = (
            ("M", "Методики"), ("P", "Паспорти"), ("KE", "Керівництва з експлуатації"), ("TD", "Техничні довідки"),
            ("ZT", "Технічні звіти"), ("TI", "Технологічні інструкції"), ("I", "Інше"), (None, "Тип"))
        context['docs_type'] = Documents.objects.values('type').annotate(Count('type'))
        context['dt'] = []
        for i in context['doc']:
            for t in context['docs_type']:
                if t['type'] in i:
                    add = [i[0], i[1], t['type__count']]
                    context['dt'].append(add)
                else:
                    continue
        context['page'] = ''
        return context