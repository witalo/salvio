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
]
