from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render

from .models import Divisions, Staff, Documents


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


def divisions(request):
    divisions = Divisions.objects.all()
    num_staff = Staff.objects.all().count()
    num_doc = Documents.objects.all().count()
    context = {
        'divisions': divisions,
        'num_staff': num_staff,
        'num_doc': num_doc}
    return render(request, 'nio_app/divisions_list_render.html', context=context)


def documents(request):
    return HttpResponse('<h1>Уся документація</h1>')


def divisions_detail(request, div_id):
    div_name = Divisions.objects.get(pk=div_id).division_name
    div_description = Divisions.objects.get(pk=div_id).div_description
    num_staff = Staff.objects.filter(division_name__division_name=div_name).count()

    doc_implemented, doc_develop, doc_agreement = 0, 0, 0
    doc_m, doc_ti, doc_tz, doc_td, doc_p, doc_ke, doc_i = 0, 0, 0, 0, 0, 0, 0
    staff = Staff.objects.filter(division_name__division_name=div_name)
    for author in staff:
        doc_implemented = Documents.objects.filter(author__fio=author, doc_status='В').count()
        doc_develop = Documents.objects.filter(author__fio=author, doc_status='Р').count()
        doc_agreement = Documents.objects.filter(author__fio=author, doc_status='У').count()

        doc_m += Documents.objects.filter(author__fio=author, doc_type='М').count()
        doc_ti += Documents.objects.filter(author__fio=author, doc_type='ТІ').count()
        doc_tz += Documents.objects.filter(author__fio=author, doc_type='ЗТ').count()
        doc_td += Documents.objects.filter(author__fio=author, doc_type='ТД').count()
        doc_p += Documents.objects.filter(author__fio=author, doc_type='П').count()
        doc_ke += Documents.objects.filter(author__fio=author, doc_type='КЕ').count()
        doc_i += Documents.objects.filter(author__fio=author, doc_type='І').count()
    # num_doc = Documents.objects.all()[pk].count()
    context = {
        'div_name': div_name,
        'num_staff': num_staff,
        'div_description': div_description,
        'doc_implemented': doc_implemented,
        'doc_develop': doc_develop,
        'doc_agreement': doc_agreement,
        'doc_m': doc_m,
        'doc_ti': doc_ti,
        'doc_tz': doc_tz,
        'doc_td': doc_td,
        'doc_p': doc_p,
        'doc_ke': doc_ke,
        'doc_i': doc_i
    }
    return render(request, 'nio_app/divisions_detail_render.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Друже нажаль такої сторінки не існує.</h1>"
                                "<h2>Перевір адресу запиту</h2>")

# class DivisionsListView(generic.ListView):
#     model = Divisions
#     paginate_by = 10
#
# class StaffListView(generic.ListView):
#     model = Staff
#     paginate_by = 10
#     def get_queryset(self):
#         return Staff.objects.all().order_by('fio')
#
# class Staff_DivListView(generic.ListView):
#     model = Staff
#     paginate_by = 10
#
#     # def get_queryset(self):
#     #     return Staff.objects.filter(division_name__division_name=Staff.division_name)
#
# class DocListView(generic.ListView):
#     model = Documents
#     paginate_by = 10
#
# class DivisionsDetailView(generic.DetailView):
#     model = Divisions
#
# class StaffDetailView(generic.DetailView):
#     model = Staff
#
# class DocDetailView(generic.DetailView):
#     model = Documents
