from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from divisions.models import Divisions
from documents.models import Documents
from staff.models import Staff
from .forms import RegisterUserForm, LoginUserForm
from .models import *
from .utilits import PortalMixin


# Create your views here.


def pageNotFound(request, exception):
    """Сторінка 404"""
    context = {}

    """використання PortalMixin"""
    mixin = PortalMixin()
    mixin.divisions = Divisions.objects.only('abr', 'slug')
    mixin_context = mixin.get_user_context()
    context = dict(list(context.items()) + list(mixin_context.items()))
    return render(request, 'nio_app/404.html', context=context)


class Index(PortalMixin, ListView):
    """Головна сторінка"""
    model = Main
    template_name = 'nio_app/index_portal.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['divisions'] = Divisions.objects.prefetch_related('locs', 'coops').values('name', 'abr', 'slug', 'locs', 'coops')
        context['staff_count'] = Staff.objects.values('div').annotate(number=Count('div'))
        context['doc_count'] = Documents.objects.values('div').annotate(number=Count('div'))
        context['boss'] = Staff.objects.only('fio', 'slug', 'div_id').filter(prof__icontains='нач')

        """використання PortalMixin"""
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))



class LoginUser(LoginView, PortalMixin):
    """Авторизація"""
    form_class = LoginUserForm
    template_name = 'nio_app/include/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        """використання PortalMixin"""
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))

    def get_success_url(self):
        return reverse_lazy('nio_app:index_portal')


class RegisterUser(CreateView, PortalMixin):
    """Реєстрація"""
    form_class = RegisterUserForm
    template_name = 'nio_app/include/registration.html'
    success_url = reverse_lazy('nio_app:index_portal')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        """використання PortalMixin"""
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))


    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('nio_app:index_portal')


def logout_user(request):
    """Вихід користувача"""
    logout(request)
    return redirect('nio_app:index_portal')



def contacts(request):
    """Контакти"""
    context = {}
    contact = Staff.objects.only('phone')
    try:
        context['dev'] = contact.get(tabel='654')
        context['sec'] = contact.get(tabel='633')
        context['arh'] = contact.get(tabel='672')
    except:
        context['dev'] = contact.first()
        context['sec'] = contact.first()
        context['arh'] = contact.last()

    """використання PortalMixin"""
    mixin = PortalMixin()
    mixin.divisions = Divisions.objects.only('abr', 'slug')
    mixin_context = mixin.get_user_context()
    context = dict(list(context.items()) + list(mixin_context.items()))
    return render(request, 'nio_app/contacts.html', context=context)


def cats(request):
    """Категорії"""
    context = {}
    """використання PortalMixin"""
    mixin = PortalMixin()
    mixin.divisions = Divisions.objects.only('abr', 'slug')
    mixin_context = mixin.get_user_context()
    context = dict(list(context.items()) + list(mixin_context.items()))
    return render(request, 'nio_app/cats.html', context=context)


