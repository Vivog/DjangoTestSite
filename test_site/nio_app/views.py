from itertools import chain

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import FileResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy, resolve
from django.views.generic import ListView, DetailView, View, CreateView
from django.views.generic.list import MultipleObjectMixin

from .forms import ReviewPubForm, ReviewNewsForm, RegisterUserForm, LoginUserForm
from .models import *
# Create your views here.
from .utilits import PortalMixin

CONTEXT = {}
CONTEXT['models'] = [[Divisions._meta.verbose_name_plural, Divisions.objects.all().count()],
                     [Staff._meta.verbose_name_plural, Staff.objects.all().count()],
                     [Documents._meta.verbose_name_plural, Documents.objects.all().count()],
                     [Projects._meta.verbose_name_plural, Projects.objects.all().count()],
                     [Publications._meta.verbose_name_plural, Publications.objects.all().count()],
                     [News._meta.verbose_name_plural, News.objects.all().count()]]
CONTEXT['main'] = Main.objects.all().prefetch_related('divisions')
"""Виключимо з підрозділів НДВ"""
CONTEXT['div'] = Divisions.objects.all().prefetch_related('locs', 'coops', 'theses')[1:]
CONTEXT['pubs'] = Publications.objects.all().select_related('div').prefetch_related('author', 'category')
CONTEXT['pubs_rev'] = ReviewsPubs.objects.all().select_related('parent', 'pub')
CONTEXT['new'] = News.objects.all().prefetch_related('category')
CONTEXT['new_all'] = News.objects.all().prefetch_related('category')
CONTEXT['news_rev'] = ReviewsNews.objects.all().select_related('parent', 'news')
CONTEXT['staff'] = Staff.objects.all().select_related('div')
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
CONTEXT['staff_prof'] = PROFS
CONTEXT['projects'] = Projects.objects.all().select_related('div').prefetch_related('author', 'category')
CONTEXT['cats'] = Categories.objects.all()
CONTEXT['docs_all'] = Documents.objects.all().select_related('div').prefetch_related('author')
CONTEXT['doc'] = (
    ("M", "Методики"), ("P", "Паспорти"), ("KE", "Керівництва з експлуатації"), ("TD", "Техничні довідки"),
    ("ZT", "Технічні звіти"), ("TI", "Технологічні інструкції"), ("I", "Інше"), (None, "Тип"))
CONTEXT['docs_type'] = Documents.objects.values('type').annotate(Count('type'))
CONTEXT['dt'] = []
for i in CONTEXT['doc']:
    for t in CONTEXT['docs_type']:
        if t['type'] in i:
            add = [i[0], i[1], t['type__count']]
            CONTEXT['dt'].append(add)
        else:
            continue
CONTEXT['page'] = ''


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

def cats(request):
    context = {}
    context.update(CONTEXT)
    return render(request, 'nio_app/cats.html', context=context)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'nio_app/include/login.html'
    extra_context = CONTEXT

    #  Достатньо написати тільки це і не переопредиляти метод!!!
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update(CONTEXT)
    #     return context

    def get_success_url(self):
        return reverse_lazy('nio_app:index_portal')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'nio_app/include/registration.html'
    success_url = reverse_lazy('nio_app:index_portal')
    extra_context = CONTEXT

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('nio_app:index_portal')


def logout_user(request):
    logout(request)
    return redirect('nio_app:index_portal')


class SearchMain(ListView):
    template_name = 'nio_app/search.html'
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
    template_name = 'nio_app/search_cat.html'
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




class Index(ListView):
    model = Main
    template_name = 'nio_app/index_portal.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        print('DIV', context['div'])
        return context
        """при використанні DataMixin"""
        # c_def = self.get_user_context()
        # return dict(list(context.items()) + list(c_def.items()))


class DivisionList(DetailView, MultipleObjectMixin):
    model = Divisions
    template_name = 'nio_app/division.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        div = Divisions.objects.get(slug=self.get_object().slug)
        object_list = div.description.split('\n')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(CONTEXT)
        context['div'] = div
        context['page'] = ''
        return context


class StaffSort:

    def get_div(self):
        return Divisions.objects.all()

    def get_prof(self):
        return Staff.objects.values('prof').distinct()


class StaffSortList(StaffSort, ListView):
    template_name = 'nio_app/staff/staff.html'
    context_object_name = 'filter'
    paginate_by = 3

    def get_queryset(self):
        # queryset = Staff.objects.order_by('fio')
        sorting = ('fio', 'tabel', 'oklad', 'birthday')
        if self.request.GET.get('divs') != None and self.request.GET.get('prof') == None and self.request.GET.get(
                'sort') == None:
            queryset = Staff.objects.filter(
                Q(div_id__in=self.request.GET.getlist("divs"))
            ).order_by('fio')
        elif self.request.GET.get('divs') != None and self.request.GET.get('prof') != None and self.request.GET.get(
                'sort') == None:
            queryset = Staff.objects.filter(
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
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update(CONTEXT)
        context['page'] = ''
        if self.request.GET.get('divs'):
            context['page'] += f"divs={self.request.GET.get('divs')}&"
        if self.request.GET.get('prof'):
            context['page'] += f"prof={self.request.GET.get('prof')}&"
        if self.request.GET.get('sort'):
            context['page'] += f"sort={self.request.GET.get('sort')}&"
        return context


class StaffList(StaffSort, ListView):
    model = Staff
    template_name = 'nio_app/staff/staff.html'
    context_object_name = 'filter'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update(CONTEXT)
        context['page'] = ''
        if self.request.GET.get('divs'):
            context['page'] += f"divs={self.request.GET.get('divs')}&"
        if self.request.GET.get('prof'):
            context['page'] += f"prof={self.request.GET.get('prof')}&"
        if self.request.GET.get('sort'):
            context['page'] += f"sort={self.request.GET.get('sort')}&"
        return context

class StaffSingle(DetailView):
    model = Staff
    template_name = 'nio_app/staff/staff_single.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update(CONTEXT)
        context['single'] = Staff.objects.get(slug=self.kwargs['slug'])
        context['page'] = ''
        return context


class SearchStaff(StaffSort, ListView):
    template_name = 'nio_app/staff/staff.html'

    def get_queryset(self):
        search_list = Staff.objects.filter(fio__icontains=self.request.GET.get('search_staff'))
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        context['filter'] = self.get_queryset()
        context['page'] = f"search_staff={self.request.GET.get('search_staff')}&"
        return context


class PubsList(PortalMixin, ListView):
    model = Publications
    template_name = 'nio_app/publics/publics.html'
    queryset = Publications.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        context['pubs'] = self.queryset
        context['page'] = ''
        return context


class PubsDetail(DetailView, MultipleObjectMixin):
    model = Publications
    template_name = 'nio_app/publics/public_single.html'
    paginate_by = 6


    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = Publications.objects.get(slug=self.kwargs['slug']).text.split('\n')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(CONTEXT)
        context['page'] = ''
        return context

    def get_queryset(self):
        return Publications.objects.filter(slug=self.kwargs['slug'])


class PubsCatsDetail(DetailView):
    model = Categories
    template_name = 'nio_app/publics/publics_category.html'

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


class SearchPub(ListView):
    template_name = 'nio_app/publics/publics.html'
    paginate_by = 1

    def get_queryset(self):
        search_list = Publications.objects.filter(name__icontains=self.request.GET.get('search_pub'))
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        context['pubs'] = self.get_queryset()
        context['page'] = f"search_pub={self.request.GET.get('search_pub')}&"
        return context


class NewsList(PortalMixin, ListView):
    model = News
    template_name = 'nio_app/news/news.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        context['last'] = News.objects.all().order_by('-pub_date')
        return context


class NewsDetail(DetailView, MultipleObjectMixin):
    model = News
    template_name = 'nio_app/news/news_single.html'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = News.objects.get(slug=self.kwargs['slug']).text.split('\n')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(CONTEXT)
        context['page'] = ''
        return context

    def get_queryset(self):
        return News.objects.filter(slug=self.kwargs['slug'])


class NewsCatsDetail(DetailView):
    model = Categories
    template_name = 'nio_app/news/news_category.html'

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


class SearchNews(ListView):
    template_name = 'nio_app/news/news.html'
    paginate_by = 1

    def get_queryset(self):
        search_list = News.objects.filter(name__icontains=self.request.GET.get('search_news'))
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        context['new'] = self.get_queryset()
        context['page'] = f"search_news={self.request.GET.get('search_news')}&"
        return context

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


class DocsList(ListView):
    model = Documents
    template_name = 'nio_app/docs/docs.html'
    paginate_by = 4
    extra_context = CONTEXT


class DocDetail(DetailView):
    model = Documents
    template_name = 'nio_app/docs/doc_single.html'
    extra_context = CONTEXT

    def get_queryset(self):
        return Documents.objects.filter(slug=self.kwargs['slug'])


def download_doc(request, id):
    from pathlib import Path
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = str(Documents.objects.get(pk=id).doc)
    filename = Path(BASE_DIR, 'media/', path)
    # if not filename.exists():
    #     filename = Path(BASE_DIR, 'static/site_app/cv', 'Savushkin_CV.pdf')

    return FileResponse(open(filename, 'rb'), as_attachment=True)


class DocsTypeDetail(ListView):

    model = Documents
    template_name = 'nio_app/docs/docs.html'
    paginate_by = 5
    # extra_context = CONTEXT

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        return context

    def get_queryset(self):
        q = Q(type=self.kwargs['type'])
        return Documents.objects.filter(q)


class SearchDoc(ListView):
    template_name = 'nio_app/docs/docs.html'
    paginate_by = 5

    def get_queryset(self):
        search_list = Documents.objects.filter(name__icontains=self.request.GET.get('search_docs'))
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(CONTEXT)
        context['page'] = f"search_docs={self.request.GET.get('search_docs')}&"
        return context



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
