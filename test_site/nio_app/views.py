from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import *
from .models import *


# Create your views here.

def home(request):
    num_divisions = Divisions.objects.all().count()
    num_staff = Staff.objects.all().count()
    num_doc = Documents.objects.all().count()
    context = {
        'num_divisions': num_divisions,
        'num_staff': num_staff,
        'num_doc': num_doc}
    return render(request, 'nio_app/home.html', context=context)


def staff(request):
    return HttpResponse('Сторінка персоналу')


# def divisions(request):
#     divisions = Divisions.objects.all()
#     context = {
#         'divisions': divisions
#     }
#     return render(request, 'nio_app/divisions_list_render.html', context=context)

class DivisionsList(ListView):
    model = Divisions
    template_name = 'nio_app/divisions_list_render.html'
    context_object_name = 'divisions'


def documents(request):
    return HttpResponse('<h1>Уся документація</h1>')


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


class DivisionsDetailList(ListView):
    model = Divisions
    template_name = 'nio_app/divisions_detail_render.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['div_name'] = self.get_queryset().division_name
        context['div_description'] = self.get_queryset().div_description
        context['num_staff'] = self.get_queryset().staff_set.count()
        context['doc_implemented'] = self.get_queryset().documents_set.filter(doc_status='В').count()
        context['doc_develop'] = self.get_queryset().documents_set.filter(doc_status='Р').count()
        context['doc_agreement'] = self.get_queryset().documents_set.filter(doc_status='У').count()
        context['doc_m'] = self.get_queryset().documents_set.filter(doc_type='М').count()
        context['doc_ti'] = self.get_queryset().documents_set.filter(doc_type='ТІ').count()
        context['doc_tz'] = self.get_queryset().documents_set.filter(doc_type='ЗТ').count()
        context['doc_td'] = self.get_queryset().documents_set.filter(doc_type='ТД').count()
        context['doc_p'] = self.get_queryset().documents_set.filter(doc_type='П').count()
        context['doc_ke'] = self.get_queryset().documents_set.filter(doc_type='КЕ').count()
        context['doc_i'] = self.get_queryset().documents_set.filter(doc_type='І').count()
        return context

    def get_queryset(self):
        return Divisions.objects.get(slug=self.kwargs['div_slug'])


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

class AddDivisionView(CreateView):
    form_class = AddDivisionForm
    template_name = 'nio_app/add_division.html'
    success_url = reverse_lazy('divisions')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додати підрозділ'
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Друже нажаль такої сторінки не існує.</h1>"
                                "<h2>Перевір адресу запиту</h2>")
