from django.shortcuts import render

from .models import Divisions, Staff, Documents


# Create your views here.

def home(request):
    num_divisions = Divisions.objects.all().count()
    num_staff = Staff.objects.all().count()
    num_staff_NDL_6 = Staff.objects.filter(division_name__exact=2).count()
    num_doc = Documents.objects.all().count()
    content = {'num_divisions': num_divisions, 'num_staff': num_staff, 'num_staff_NDL_6': num_staff_NDL_6,
               'num_doc': num_doc}
    return render(request, 'nio_app/home.html', context=content)
