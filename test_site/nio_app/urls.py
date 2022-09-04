from django.urls import path

from nio_app.views import *

app_name = 'nio_app'
urlpatterns = [

    path('', Index.as_view(), name='index_portal'),

    path('login/', LoginUser.as_view(), name='login'),
    path('reg/', RegisterUser.as_view(), name='registration'),
    path('logout/', logout_user, name='logout'),

    path('contacts/', contacts, name='contacts'),
    path('cats/', cats, name='cats'),

]

