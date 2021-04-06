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
    # domain
    path('domain_list/', login_required(get_domain_list), name='domain_list'),
    path('modal_domain_save/', login_required(modal_domain_save), name='modal_domain_save'),
    path('modal_domain_update/', login_required(modal_domain_update), name='modal_domain_update'),
    path('save_domain/', login_required(save_domain), name='save_domain'),
    path('update_domain/', login_required(update_domain), name='update_domain'),
    # zone
    path('zone_list/', login_required(get_zone_list), name='zone_list'),
    path('modal_zone_save/', login_required(modal_zone_save), name='modal_zone_save'),
    path('modal_zone_update/', login_required(modal_zone_update), name='modal_zone_update'),
    path('save_zone/', login_required(save_zone), name='save_zone'),
    path('update_zone/', login_required(update_zone), name='update_zone'),
    # lot
    path('lot_list/', login_required(get_lot_list), name='lot_list'),
    path('modal_lot_save/', login_required(modal_lot_save), name='modal_lot_save'),
    path('modal_lot_update/', login_required(modal_lot_update), name='modal_lot_update'),
    path('save_lot/', login_required(save_lot), name='save_lot'),
    path('update_lot/', login_required(update_lot), name='update_lot'),
    # cultivation
    path('cultivation_list/', login_required(get_cultivation_list), name='cultivation_list'),
    path('modal_cultivation_save/', login_required(modal_cultivation_save), name='modal_cultivation_save'),
    path('modal_cultivation_update/', login_required(modal_cultivation_update), name='modal_cultivation_update'),
    path('save_cultivation/', login_required(save_cultivation), name='save_cultivation'),
    path('update_cultivation/', login_required(update_cultivation), name='update_cultivation'),
    # variety
    path('variety_list/', login_required(get_variety_list), name='variety_list'),
    path('modal_variety_save/', login_required(modal_variety_save), name='modal_variety_save'),
    path('modal_variety_update/', login_required(modal_variety_update), name='modal_variety_update'),
    path('save_variety/', login_required(save_variety), name='save_variety'),
    path('update_variety/', login_required(update_variety), name='update_variety'),
    # phenology
    path('phenology_list/', login_required(get_phenology_list), name='phenology_list'),
    path('modal_phenology_save/', login_required(modal_phenology_save), name='modal_phenology_save'),
    path('modal_phenology_update/', login_required(modal_phenology_update), name='modal_phenology_update'),
    path('save_phenology/', login_required(save_phenology), name='save_phenology'),
    path('update_phenology/', login_required(update_phenology), name='update_phenology'),
    path('get_module_by_domain/', login_required(get_module_by_domain), name='get_module_by_domain'),
    # program production
    path('program_production/', login_required(get_program_production_list), name='program_production'),
    path('program_production_save/', login_required(modal_program_production_save), name='program_production_save'),
]
