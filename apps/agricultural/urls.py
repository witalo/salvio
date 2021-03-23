from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('employee_list/', login_required(get_employee_list), name='employee_list'),
    path('get_employee_form/', login_required(get_employee_form), name='get_employee_form'),
    path('get_employee_update_form/', login_required(get_employee_update_form), name='get_employee_update_form'),
    path('save_person/', login_required(save_person), name='save_person'),
    path('update_person/', login_required(update_person), name='update_person'),
    # business
    path('business_list/', login_required(get_business_list), name='business_list'),
    path('get_business_form/', login_required(get_business_form), name='get_business_form'),
    path('save_business/', login_required(save_business), name='save_business'),
    path('get_business_by_document/', login_required(get_business_by_document), name='get_business_by_document'),
    path('update_business/', login_required(update_business), name='update_business'),
    path('modal_update_business/', login_required(modal_update_business), name='modal_update_business'),
    # module
    path('module_list/', login_required(get_module_list), name='module_list'),
    path('modal_module_save/', login_required(modal_module_save), name='modal_module_save'),
    path('modal_module_update/', login_required(modal_module_update), name='modal_module_update'),
    path('save_modulo/', login_required(save_modulo), name='save_modulo'),
    path('update_modulo/', login_required(update_modulo), name='update_modulo'),
]