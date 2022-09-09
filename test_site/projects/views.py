from django.http import FileResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.list import MultipleObjectMixin

from .forms import ReviewProjectForm
from .models import *
from divisions.models import Divisions
from nio_app.models import Categories

from nio_app.utilits import PortalMixin


# Create your views here.
class ProjectsList(ListView, PortalMixin):
    """Проекти"""
    model = Projects
    template_name = 'projects/projects.html'
    queryset = Projects.objects.prefetch_related('author', 'category', 'reviewsprojects_set')
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=self.object_list, **kwargs)
        context['cats'] = Categories.objects.filter(projects__gte=1).distinct()
        context['projs'] = Projects.objects.only('name', 'slug',)

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))


class ProjectsDetail(DetailView, PortalMixin):
    """Окремий проект"""
    model = Projects
    template_name = 'projects/project_single.html'

    def get_object(self, queryset=None):
        return Projects.objects.prefetch_related('category', 'author', 'reviewsprojects_set').get(
            slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['cats'] = Categories.objects.filter(projects__gte=1).distinct()
        context['projs'] = Projects.objects.only('name', 'slug',)
        context['pic'] = ProjectsPics.objects.get(project_id=self.object.pk).pic

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))

def download_doc(request, id):
    from pathlib import Path
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = str(ProjectsDocs.objects.get(project_id=id).doc)
    filename = Path(BASE_DIR, 'media/', path)
    return FileResponse(open(filename, 'rb'), as_attachment=True)


class ProjectsCatsDetail(DetailView, PortalMixin):
    """Категорії проектів"""
    model = Categories
    template_name = 'projects/project_category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = Projects.objects.prefetch_related('category', 'author', )
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['cats'] = Categories.objects.filter(projects__gte=1).distinct()
        context['projs'] = Projects.objects.only('name', 'slug', )

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()
        return dict(list(context.items()) + list(mixin_context.items()))


class AddReviewProject(View):
    """Відгук на проект"""
    def post(self, request, slug):
        form = ReviewProjectForm(request.POST)
        project = Projects.objects.prefetch_related('category', 'author',).get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.project = project
            form.save()
        return redirect(project.get_absolute_url())


class SearchProject(ListView, PortalMixin):
    """Пошук проектів"""
    template_name = 'projects/projects.html'

    def get_queryset(self):
        search_list = Projects.objects.select_related('div').filter(
            name__icontains=self.request.GET.get('search_project'))
        return search_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['cats'] = Categories.objects.filter(projects__gte=1).distinct()
        context['projs'] = Projects.objects.only('name', 'slug', )
        context['page'] = f"search_project={self.request.GET.get('search_project')}&"

        """використання PortalMixin"""
        self.divisions = Divisions.objects.only('abr', 'slug')
        mixin_context = self.get_user_context()

        return dict(list(context.items()) + list(mixin_context.items()))



