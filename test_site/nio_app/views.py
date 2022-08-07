from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q, OuterRef, Subquery, Case, When
from .forms import ReviewPubForm, ReviewNewsForm
from .models import *
from datetime import date
from datetime import date

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from .models import *

# Create your views here.



CONTEXT = {}
CONTEXT['main'] = Main.objects.all()
CONTEXT['div'] = Divisions.objects.all()
CONTEXT['doc'] = (("М", "Методики"), ("П", "Паспорти"), ("КЕ", "Керівництва з експлуатації"), ("ТД", "Техничні довідки"),
        ("ЗТ", "Технічні звіти"), ("ТІ", "Технологічні інструкції"), ("І", "Інше"), (None, "Тип"))
CONTEXT['projects'] = Projects.objects.all()
CONTEXT['pubs'] = Publications.objects.all()
CONTEXT['pubs_rev'] = ReviewsPubs.objects.all()
CONTEXT['new'] = News.objects.all()
CONTEXT['news_rev'] = ReviewsNews.objects.all()
CONTEXT['staff'] = Staff.objects.all()
STAFF = Staff.objects.all()
# PROF = [('Усі',len(STAFF)), ]
PROF = []
for s in STAFF:
    if s.prof not in PROF:
        # num = len(Staff.objects.filter(prof=s.prof))
        PROF.append(s.prof)
    else:
        continue
PROFS = list(set(PROF))
trans_table = str.maketrans(
    'ABCEHKMOPTXacekmopuxyi',
    'АВСЕНКМОРТХасекморихуі',
)
PROFS.sort(key=lambda s: s[0].translate(trans_table))
CONTEXT['staff_prof'] = PROFS
CONTEXT['cats'] = Categories.objects.all()


def pageNotFound(request, exception):
    context = {}
    context.update(CONTEXT)
    return render(request, 'nio_app/404.html', context=context)

def contacts(request):
    context = {}
    context.update(CONTEXT)
    context['dev'] = Staff.objects.get(tabel='654')
    context['sec'] = Staff.objects.get(tabel='633')
    context['arh'] = Staff.objects.get(tabel='672')
    return render(request, 'nio_app/contacts.html', context=context)

def index_portal(request):

    context = {}
    context.update(CONTEXT)
    return render(request, 'nio_app/index_portal.html', context=context)

class DivisionList(DetailView):
    model = Divisions
    template_name = 'nio_app/division.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        context['div'] = Divisions.objects.get(slug=self.get_object().slug)
        return context



class StaffSort:

    def get_div(self):
        return Divisions.objects.all()

    def get_prof(self):
        return Staff.objects.values('prof').distinct()


class StaffSortList(StaffSort, ListView):
    template_name = 'nio_app/staff.html'
    context_object_name = 'filter'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update(CONTEXT)
        return context

    def get_queryset(self):
        queryset = Staff.objects.order_by('fio')
        sorting = ('fio', 'tabel', 'oklad', 'birthday')
        if self.request.GET.get('divs') == None and self.request.GET.get('prof') == None and self.request.GET.get('sort') != None:
            for s in sorting:
                if self.request.GET.get('sort') == s:
                    queryset = Staff.objects.order_by(s)
        elif self.request.GET.get('divs') == None:
            for s in sorting:
                if self.request.GET.get('sort') == s:
                    queryset = Staff.objects.filter(
                        Q(prof__in=self.request.GET.getlist("prof"))
                    ).order_by(s)
        elif self.request.GET.get('divs') != None and self.request.GET.get('prof') == None:
            for s in sorting:
                if self.request.GET.get('sort') == s:
                    queryset = Staff.objects.filter(
                        Q(div_id__in=self.request.GET.getlist("divs"))
                    ).order_by(s)
        elif self.request.GET.get('divs') != None and self.request.GET.get('prof') != None:
            for s in sorting:
                if self.request.GET.get('sort') == s:
                    queryset = Staff.objects.filter(
                        Q(div_id__in=self.request.GET.getlist("divs")),
                        Q(prof__in=self.request.GET.getlist("prof"))
                    ).order_by(s)
        return queryset

class StaffList(StaffSort, ListView):
    model = Staff
    template_name = 'nio_app/staff.html'
    context_object_name = 'filter'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update(CONTEXT)
        return context


    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=None, **kwargs)
    #     context.update(CONTEXT)
    #     context['staff_all'] = Staff.objects.all().count()
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     if self.request.method == 'POST':
    #         sort = self.sort_by(self.request, divs=self.request.POST.get('divs'), prof=self.request.POST.get('prof'),
    #                             sort=self.request.POST.get('sort'))
    #         CONTEXT['staff'] = sort
    #         return render(request, 'nio_app/staff.html', context=CONTEXT)
    #     else:
    #         sort = self.sort_by(self.request)
    #         CONTEXT['staff'] = sort
    #         return render(request, 'nio_app/staff.html', context=CONTEXT)
    #
    # def sort_by(self, request, divs=None, prof=None, sort=None):
    #     if divs == None and prof == None:
    #         if sort == None:
    #             STAFF = Staff.objects.all()
    #             return STAFF
    #         elif sort != None:
    #             STAFF = Staff.objects.all()
    #             if sort == 'tabel':
    #                 STAFF = STAFF.order_by('tabel')
    #                 return STAFF
    #             elif sort == 'fio':
    #                 STAFF = STAFF.order_by('fio')
    #                 return STAFF
    #             elif sort == 'age':
    #                 STAFF = STAFF.order_by('birthday')
    #                 return STAFF
    #             elif sort == 'oklad':
    #                 STAFF = STAFF.order_by('oklad')
    #                 return STAFF
    #     else:
    #         if prof == None and divs != None:
    #             if sort == None:
    #                 div = Divisions.objects.filter(abr=divs)
    #                 STAFF = Staff.objects.filter(div_id=div[0])
    #                 return STAFF
    #             elif sort != None:
    #                 div = Divisions.objects.filter(abr=divs)
    #                 STAFF = Staff.objects.filter(div_id=div[0])
    #                 if sort == 'tabel':
    #                     STAFF = STAFF.order_by('tabel')
    #                     return STAFF
    #                 elif sort == 'fio':
    #                     STAFF = STAFF.order_by('fio')
    #                     return STAFF
    #                 elif sort == 'age':
    #                     STAFF = STAFF.order_by('birthday')
    #                     return STAFF
    #                 elif sort == 'oklad':
    #                     STAFF = STAFF.order_by('oklad')
    #                     return STAFF
    #         elif divs == None and prof != None:
    #             if sort == None:
    #                 STAFF = Staff.objects.filter(prof=prof)
    #                 return STAFF
    #             elif sort != None:
    #                 STAFF = Staff.objects.filter(prof=prof)
    #                 if sort == 'tabel':
    #                     STAFF = STAFF.order_by('tabel')
    #                     return STAFF
    #                 elif sort == 'fio':
    #                     STAFF = STAFF.order_by('fio')
    #                     return STAFF
    #                 elif sort == 'age':
    #                     STAFF = STAFF.order_by('birthday')
    #                     return STAFF
    #                 elif sort == 'oklad':
    #                     STAFF = STAFF.order_by('oklad')
    #                     return STAFF
    #         elif divs != None and prof != None:
    #             if sort == None:
    #                 div = Divisions.objects.filter(abr=divs)
    #                 STAFF = Staff.objects.filter(div_id=div[0]).filter(prof=prof)
    #                 return STAFF
    #             elif sort != None:
    #                 div = Divisions.objects.filter(abr=divs)
    #                 STAFF = Staff.objects.filter(div_id=div[0]).filter(prof=prof)
    #                 if sort == 'tabel':
    #                     STAFF = STAFF.order_by('tabel')
    #                     return STAFF
    #                 elif sort == 'fio':
    #                     STAFF = STAFF.order_by('fio')
    #                     return STAFF
    #                 elif sort == 'age':
    #                     STAFF = STAFF.order_by('birthday')
    #                     return STAFF
    #                 elif sort == 'oklad':
    #                     STAFF = STAFF.order_by('oklad')
    #                     return STAFF










# class StaffSort(ListView):
#     model = Staff
#     template_name = 'nio_app/staff_sort.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data()
#         context.update(CONTEXT)
#         context['staff'] = Staff.objects.order_by('fio')
#         if 'tabel':
#             context['staff'] = Staff.objects.order_by('tabel')
#         elif 'oklad':
#             context['staff'] = Staff.objects.order_by('oklad')
#         elif 'age':
#             context['staff'] = Staff.objects.order_by('birthday')
#         return context




class PubsList(ListView):
    model = Publications
    template_name = 'nio_app/publics.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        context['last'] = Publications.objects.all().order_by('-pub_date')
        return context

class PubsDetail(DetailView):
    model = Publications
    template_name = 'nio_app/public_single.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        return context

    def get_queryset(self):
        return Publications.objects.filter(slug=self.kwargs['slug'])

class PubsCatsDetail(DetailView):
    model = Categories
    template_name = 'nio_app/publics_category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        return context

    def get_queryset(self):
        return Categories.objects.filter(slug=self.kwargs['slug'])


class AddReviewPub(View):

    def post(self, request, slug):
        form = ReviewPubForm(request.POST)
        pub = Publications.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
                print(form.parent_id)
            form.pub = pub
            form.save()
        return redirect(pub.get_absolute_url())


class NewsList(ListView):
    model = News
    template_name = 'nio_app/news.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        context['last'] = News.objects.all().order_by('-pub_date')
        return context

class NewsDetail(DetailView):
    model = News
    template_name = 'nio_app/news_single.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        return context
    def get_queryset(self):
        return News.objects.filter(slug=self.kwargs['slug'])

class NewsCatsDetail(DetailView):
    model = Categories
    template_name = 'nio_app/news_category.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        return context
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






    # def post(self, request):
    #     div = Divisions.objects.all()
    #     if request.method == '':
    #     for d in div:
    #         print(d)
    #         if divs == d:
    #             print('DIVS ', divs)
    #
    #     return render(request, 'nio_app/staff.html', context=CONTEXT)

    # def post(self, request):
    #     if request.method == 'POST':
    #         form = ChoiseStaffForm(request.POST)
    #         if form.is_valid():
    #             divs = request.POST.get('by_divs')
    #             print('DIVS ', divs)
    #             # context =
    #             div = Divisions.objects.filter(abr=form.by_divs)
    #             CONTEXT['staff'] = Staff.objects.filter(div_id=div.id)
    #             return redirect('nio_app:staff')
    #     else:
    #         form = ChoiseStaffForm
    #     return render(request, 'nio_app/staff.html', {'form': form},)


# def home(request):
#     num_divisions = Divisions.objects.all().count()
#     num_staff = Staff.objects.all().count()
#     num_doc = Documents.objects.all().count()
#     divisions = 'divisions/'
#     staff = 'staff/'
#     docs = 'documents/'
#     context = {
#         'divisions': divisions,
#         'staff': staff,
#         'docs': docs,
#         'num_divisions': num_divisions,
#         'num_staff': num_staff,
#         'num_doc': num_doc}
#     return render(request, 'nio_app/home.html', context=context)
#
#
# class RegisterUser(CreateView):
#     form_class = RegisterForm
#     template_name = 'nio_app/register.html'
#     success_url = reverse_lazy('login')
#
#     def get_context_data(self, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title_head'] = 'Портал НДВ - Реєстрація користувача'
#         context['title'] = 'Реєстанція користувача'
#         return context
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('home')
#
#
# class LoginUser(LoginView):
#     form_class = LoginForm
#     template_name = 'nio_app/login.html'
#
#     def get_context_data(self, object_list=None, **kwargs):
#         context = super(LoginUser, self).get_context_data(**kwargs)
#         context['title_head'] = 'Портал НДВ - Авторизація'
#         context['title'] = 'Авторизація'
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('home')
#
#
# def logout_user(request):
#     logout(request)
#     return redirect('home')
#
#
# class Staff_DivList(ListView):
#     model = Staff
#     template_name = 'nio_app/staff_list_render.html'
#     context_object_name = 'staff'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title_head'] = 'Портал НДВ - Персонал'
#         context["divisions"] = Divisions.objects.all()
#         return context
#
#     def get_queryset(self):
#         return Staff.objects.all()
#
#
# class StaffDetailList(DetailView):
#     paginate_by = 2
#     model = Staff
#     template_name = 'nio_app/staff_detail_render.html'
#     context_object_name = 'staff_detail'
#     # если применяемый slug в urls.py не слово slug а что то другое, например div_slug, то обязательно!!!
#     slug_url_kwarg = 'div_slug'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['div'] = context['staff_detail'].division_name
#         context['title_head'] = f"Портал НДВ - {context['div']}"
#         context['staff'] = context['staff_detail'].staff_set.all()
#         context['slug'] = context['staff_detail'].slug
#         return context
#
#     def get_queryset(self):
#         # get() не применимо потому что нужно именно quertyset а не один елемент модели
#         return Divisions.objects.filter(slug=self.kwargs['div_slug'])
#
#
# class AddPersonView(CreateView):
#     form_class = AddPersonForm
#     template_name = 'nio_app/add_person.html'
#     slug_url_kwarg = 'div_slug'
#     success_url = reverse_lazy('home')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title_head'] = 'Портал НДВ - Додати співробітника'
#         context['title'] = 'Додати співробітника'
#         context['slug'] = Divisions.objects.filter(slug=self.kwargs['div_slug']).values('slug')[0]['slug']
#         return context
#
#     def form_valid(self, form):
#         # Если нужно ссылка на поле ForeignKey то нужно передавать не имя поля а его айди с учетом нужной фильтрации
#         div = Divisions.objects.filter(slug=self.kwargs['div_slug']).values('pk')[0]['pk']
#         instance = form.save(commit=False)  # приостанавливаем запись данных в форму
#         instance.division_name_id = div
#         instance.slug = slugify(form.cleaned_data['fio'])
#         instance.save()
#         return redirect('div_staff-detail',
#                         Divisions.objects.filter(slug=self.kwargs['div_slug']).values('slug')[0]['slug'])
#
#     def get_queryset(self):
#         return Divisions.objects.filter(slug=self.kwargs['div_slug'])
#
#
# class PersonDetailList(DetailView):
#     model = Staff
#     template_name = 'nio_app/person_detail_render.html'
#     context_object_name = 'person_detail'
#     slug_url_kwarg = 'staff_slug'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title_head'] = 'Портал НДВ - Інфо користувача'
#         context['fio'] = context['person_detail'].fio
#         context['photo'] = context['person_detail'].photo
#         context['staff'] = Staff.objects.filter(slug=self.kwargs['staff_slug'])
#         context['slug'] = context['person_detail'].slug
#         context['div_name'] = context['person_detail'].division_name
#         # Способ как все таки взять значение атрибута из quertyset
#         # values('имя атрибута') получаем словарь {'имя атрибута': 'значение'}
#         # потом указиваем ключ к словарю и получаем значение
#         context['div_slug'] = Divisions.objects.filter(division_name=context['div_name']).values('slug')[0]['slug']
#
#         return context
#
#     def get_queryset(self):
#         return Staff.objects.filter(slug=self.kwargs['staff_slug'])
#
#
# class EditInfoPersonView(UpdateView):
#     form_class = EditInfoPersonForm
#     template_name = 'nio_app/edit_info_person.html'
#     success_url = reverse_lazy('divisions')
#     slug_url_kwarg = 'staff_slug'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title_head'] = 'Портал НДВ - Корегування інфо користувача'
#         context['title'] = 'Корегування інформації про користувача'
#         context['slug'] = context['staff'].slug
#         return context
#
#     def form_valid(self, form):
#         # Если нужно ссылка на поле ForeignKey то нужно передавать не имя поля а его айди с учетом нужной фильтрации
#         # div = Divisions.objects.filter(slug=self.kwargs['div_slug']).values('pk')[0]['pk']
#         instance = form.save(commit=False)  # приостанавливаем запись данных в форму
#         instance.division_name = form.clean_division_name()
#         instance.save()
#         return redirect('staff')
#
#     def get_queryset(self):
#         return Staff.objects.filter(slug=self.kwargs['staff_slug'])
#
#
# class DivisionsList(ListView):
#     model = Divisions
#     template_name = 'nio_app/divisions_list_render.html'
#     context_object_name = 'divisions'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title_head'] = 'Портал НДВ - Підрозділи'
#         return context
#
#
# class DivisionsDetailList(ListView):
#     model = Divisions
#     template_name = 'nio_app/divisions_detail_render.html'
#     context_object_name = 'divisions'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['div_name'] = context["divisions"].division_name
#         context['title_head'] = f"Портал НДВ - {context['div_name']}"
#         context['div_description'] = context["divisions"].div_description
#         context['div_slug'] = context["divisions"].slug
#         context['num_staff'] = context["divisions"].staff_set.count()
#         context['staff'] = context["divisions"].staff_set.all()
#         context['doc_implemented'] = context["divisions"].documents_set.filter(doc_status='В').count()
#         context['doc_develop'] = context["divisions"].documents_set.filter(doc_status='Р').count()
#         context['doc_agreement'] = context["divisions"].documents_set.filter(doc_status='У').count()
#         docs = []
#         d_type = (
#             ("Методики", "М"), ("Паспорти", "П"), ("Керівництва з експлуатації", "КЕ"), ("Техничні довідки", "ТД"),
#             ("Техничні звіти", "ТЗ"), ("Технологічні інструкції", "ТІ"), ("Інше", "І"))
#         for d in range(0, 7):
#             name = d_type[d][0]
#             count = context["divisions"].documents_set.filter(doc_type=d_type[d][1]).count()
#             docs.append((name, count))
#         context['docs'] = docs
#         return context
#
#     def get_queryset(self):
#         return Divisions.objects.get(slug=self.kwargs['div_slug'])
#
#
# class AddDivisionView(CreateView):
#     form_class = AddDivisionForm
#     template_name = 'nio_app/add_division.html'
#     success_url = reverse_lazy('divisions')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title_head'] = 'Портал НДВ - Додати підрозділ'
#         context['title'] = 'Додати підрозділ'
#         return context
#
#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.slug = slugify(form.cleaned_data['div_abr'])
#         instance.save()
#         return redirect('divisions')
#
#
# class DocList(ListView):
#     model = Documents
#     template_name = 'nio_app/doc_list_render.html'
#     context_object_name = 'docs'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title_head'] = 'Портал НДВ - Документація'
#         context['doc_list'] = []
#         for d in context['docs']:
#             if d.division_name not in context['doc_list']:
#                 context['doc_list'].append(d.division_name)
#             else:
#                 continue
#         # context['div'] = context['docs'].filter(division_name=context['docs']).values('slug')[0]['slug']
#         context['slug'] = Divisions.objects.first().documents_set.all()
#         return context
#
#     def get_queryset(self):
#         return Documents.objects.all()
#
#
# class DocDetailList(DetailView):
#     paginate_by = 2
#     model = Documents
#     template_name = 'nio_app/doc_detail_render.html'
#     context_object_name = 'doc_detail'
#     # если применяемый slug в urls.py не слово slug а что то другое, например div_slug, то обязательно!!!
#     slug_url_kwarg = 'div_slug'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title_head'] = 'Портал НДВ - Документація'
#         context['div'] = context['doc_detail'].division_name
#         context['docs'] = context['doc_detail'].documents_set.all()
#         return context
#
#     def get_queryset(self):
#         # get() не применимо потому что нужно именно quertyset а не один елемент модели
#         return Divisions.objects.filter(slug=self.kwargs['div_slug'])




# def divisions(request):
#     divisions = Divisions.objects.all()
#     context = {
#         'divisions': divisions
#     }
#     return render(request, 'nio_app/divisions_list_render.html', context=context)

# def divisions_detail(request, div_slug):
#     div_name = Divisions.objects.get(slug=div_slug).division_name
#     div_description = Divisions.objects.get(slug=div_slug).div_description
#     num_staff = Staff.objects.filter(division_name__division_name=div_name).count()
#
#     doc_implemented, doc_develop, doc_agreement = 0, 0, 0
#     doc_m, doc_ti, doc_tz, doc_td, doc_p, doc_ke, doc_i = 0, 0, 0, 0, 0, 0, 0
#     staff = Staff.objects.filter(division_name__division_name=div_name)
#     for author in staff:
#         doc_implemented = Documents.objects.filter(author__fio=author, doc_status='В').count()
#         doc_develop = Documents.objects.filter(author__fio=author, doc_status='Р').count()
#         doc_agreement = Documents.objects.filter(author__fio=author, doc_status='У').count()
#
#         doc_m += Documents.objects.filter(author__fio=author, doc_type='М').count()
#         doc_ti += Documents.objects.filter(author__fio=author, doc_type='ТІ').count()
#         doc_tz += Documents.objects.filter(author__fio=author, doc_type='ЗТ').count()
#         doc_td += Documents.objects.filter(author__fio=author, doc_type='ТД').count()
#         doc_p += Documents.objects.filter(author__fio=author, doc_type='П').count()
#         doc_ke += Documents.objects.filter(author__fio=author, doc_type='КЕ').count()
#         doc_i += Documents.objects.filter(author__fio=author, doc_type='І').count()
#     # num_doc = Documents.objects.all()[pk].count()
#     context = {
#         'div_name': div_name,
#         'num_staff': num_staff,
#         'div_description': div_description,
#         'doc_implemented': doc_implemented,
#         'doc_develop': doc_develop,
#         'doc_agreement': doc_agreement,
#         'doc_m': doc_m,
#         'doc_ti': doc_ti,
#         'doc_tz': doc_tz,
#         'doc_td': doc_td,
#         'doc_p': doc_p,
#         'doc_ke': doc_ke,
#         'doc_i': doc_i
#     }
#     return render(request, 'nio_app/divisions_detail_render.html', context=context)

# def add_division(request):
#     if request.method == "POST":
#         form = AddDivisionForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data) відображення введених даних у консолі в вигляді словника
#             try:
#                 # При використанні форму з спадкуванням від класу form.Form
#                 # Divisions.objects.create(**form.cleaned_data)
#                 # при викорисанні класу form.ModelForm
#                 form.save()
#                 return redirect('divisions')
#             except:
#                 form.add_error(None, "Помилка додавання підрозділу в БД")
#     else:
#         form = AddDivisionForm()
#     return render(request, 'nio_app/add_division.html', context={'form': form, 'title': 'Додати підрозділ'})
