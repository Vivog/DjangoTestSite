from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, resolve
from django.views.generic import ListView, CreateView

from .forms import *
from .models import *
from .utilits import *


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

class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = 'nio_app/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, object_list=None,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Реєстанція користувача'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'nio_app/login.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['title'] = 'Авторизація'
        return context

    def get_success_url(self):
        return reverse_lazy('home')



def logout_user(request):
    logout(request)
    return redirect('home')


class Staff_DivList(ListView):
    model = Staff
    template_name = 'nio_app/staff_list_render.html'
    context_object_name = 'staff'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["divisions"] = Divisions.objects.all()
        return context

    def get_queryset(self):
        return Staff.objects.all()


class StaffDetailList(ListView):
    # paginate_by = 7
    model = Staff
    template_name = 'nio_app/staff_detail_render.html'
    context_object_name = 'staff_detail'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['div'] = context['staff_detail'].division_name
        context['staff'] = context['staff_detail'].staff_set.all()

        return context

    def get_queryset(self):
        # return Divisions.objects.all()
        return Divisions.objects.get(slug=self.kwargs['div_slug'])


class PersonDetailList(ListView):
    model = Staff
    template_name = 'nio_app/person_detail_render.html'
    context_object_name = 'person_detail'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fio'] = context['person_detail'].fio
        context['photo'] = context['person_detail'].photo
        context['staff'] = Staff.objects.filter(slug=self.kwargs['staff_slug'])

        return context

    def get_queryset(self):
        return Staff.objects.get(slug=self.kwargs['staff_slug'])


class DivisionsList(ListView):
    model = Divisions
    template_name = 'nio_app/divisions_list_render.html'
    context_object_name = 'divisions'


class DivisionsDetailList(ListView):
    model = Divisions
    template_name = 'nio_app/divisions_detail_render.html'
    context_object_name = 'divisions'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['div_name'] = context["divisions"].division_name
        context['div_description'] = context["divisions"].div_description
        context['div_slug'] = context["divisions"].slug
        context['num_staff'] = context["divisions"].staff_set.count()
        context['staff'] = context["divisions"].staff_set.all()
        context['doc_implemented'] = context["divisions"].documents_set.filter(doc_status='В').count()
        context['doc_develop'] = context["divisions"].documents_set.filter(doc_status='Р').count()
        context['doc_agreement'] = context["divisions"].documents_set.filter(doc_status='У').count()
        docs = []
        d_type = (
            ("Методики", "М"), ("Паспорти", "П"), ("Керівництва з експлуатації", "КЕ"), ("Техничні довідки", "ТД"),
            ("Техничні звіти", "ТЗ"), ("Технологічні інструкції", "ТІ"), ("Інше", "І"))
        for d in range(0, 7):
            name = d_type[d][0]
            count = context["divisions"].documents_set.filter(doc_type=d_type[d][1]).count()
            docs.append((name, count))
        context['docs'] = docs
        return context

    def get_queryset(self):
        return Divisions.objects.get(slug=self.kwargs['div_slug'])


class AddDivisionView(CreateView):
    form_class = AddDivisionForm
    template_name = 'nio_app/add_division.html'
    success_url = reverse_lazy('divisions')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додати підрозділ'
        return context


class DocList(ListView):
    model = Documents
    template_name = 'nio_app/doc_list_render.html'
    context_object_name = 'docs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["divisions"] = Divisions.objects.all()
        return context

    def get_queryset(self):
        return Documents.objects.all()





def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Друже нажаль такої сторінки не існує.</h1>"
                                "<h2>Перевір адресу запиту</h2>")

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
