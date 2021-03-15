from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('employee_list/', login_required(get_employee_list), name='employee_list'),
    path('get_employee_form/', login_required(get_employee_form), name='get_employee_form'),
    path('get_employee_update_form/', login_required(get_employee_update_form), name='get_employee_update_form'),
    path('save_person/', login_required(save_person), name='save_person'),
    path('update_person/', login_required(update_person), name='update_person'),
]