from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('method_list/', login_required(get_method_list), name='method_list'),
    path('modal_method_save/', login_required(modal_method_save), name='modal_method_save'),
    path('modal_method_update/', login_required(modal_method_update), name='modal_method_update'),
    path('save_method/', login_required(save_method), name='save_method'),
    path('update_method/', login_required(update_method), name='update_method'),

    path('group_list/', login_required(get_group_list), name='group_list'),
    path('modal_group_save/', login_required(modal_group_save), name='modal_group_save'),
    path('modal_group_update/', login_required(modal_group_update), name='modal_group_update'),
    path('save_group/', login_required(save_group), name='save_group'),
    path('update_group/', login_required(update_group), name='update_group'),

    path('team_list/', login_required(get_team_list), name='team_list'),
    path('modal_team_save/', login_required(modal_team_save), name='modal_team_save'),
    path('modal_team_update/', login_required(modal_team_update), name='modal_team_update'),
    path('save_team/', login_required(save_team), name='save_team'),
    path('update_team/', login_required(update_team), name='update_team'),

    path('law_list/', login_required(get_law_list), name='law_list'),
    path('modal_law_save/', login_required(modal_law_save), name='modal_law_save'),
    path('modal_law_update/', login_required(modal_law_update), name='modal_law_update'),
    path('save_law/', login_required(save_law), name='save_law'),
    path('update_law/', login_required(update_law), name='update_law'),

    path('operators_list/', login_required(get_operators_list), name='operators_list'),
    path('modal_operators_save/', login_required(modal_operators_save), name='modal_operators_save'),
    path('modal_operators_update/', login_required(modal_operators_update), name='modal_operators_update'),
    path('save_operators/', login_required(save_operators), name='save_operators'),
    path('update_operators/', login_required(update_operators), name='update_operators'),

    path('irrigation_list/', login_required(get_irrigation_list), name='irrigation_list'),
    path('modal_irrigation_save/', login_required(modal_irrigation_save), name='modal_irrigation_save'),
    path('save_irrigation/', login_required(save_irrigation), name='save_irrigation'),
    path('modal_irrigation_update/', login_required(modal_irrigation_update), name='modal_irrigation_update'),
    path('update_irrigation/', login_required(update_irrigation), name='update_irrigation'),

    path('detail_irrigation_list/<int:pk>/', login_required(get_detail_irrigation_list), name='detail_irrigation_list'),
    path('modal_detail_irrigation_save/', login_required(modal_detail_irrigation_save),
         name='modal_detail_irrigation_save'),
    path('save_detail_irrigation/', login_required(save_detail_irrigation), name='save_detail_irrigation'),
    path('modal_detail_irrigation_update/', login_required(modal_detail_irrigation_update),
         name='modal_detail_irrigation_update'),
    path('update_detail_irrigation/', login_required(update_detail_irrigation), name='update_detail_irrigation'),
    path('detail_pulses/', login_required(get_detail_pulses), name='detail_pulses'),
    path('modal_save_pulses/', login_required(modal_save_pulses), name='modal_save_pulses'),
    path('save_detail_pulses/', login_required(save_detail_pulses), name='save_detail_pulses'),
    path('modal_update_pulses/', login_required(modal_update_pulses), name='modal_update_pulses'),
    path('update_detail_pulses/', login_required(update_detail_pulses), name='update_detail_pulses'),

    path('request_irrigation_list/<int:pk>/', login_required(request_irrigation_list), name='request_irrigation_list'),
    path('modal_request_irrigation_save/', login_required(modal_request_irrigation_save),
         name='modal_request_irrigation_save'),
    path('save_request_irrigation/', login_required(save_request_irrigation),
         name='save_request_irrigation'),
    path('set_consumed_requirement/', login_required(set_consumed_requirement),
         name='set_consumed_requirement'),
    path('get_consumed_detail/', login_required(get_consumed_detail),
         name='get_consumed_detail'),
    path('update_consumed_requirement/', login_required(update_consumed_requirement),
         name='update_consumed_requirement'),
]
