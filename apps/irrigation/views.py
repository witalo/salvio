from django.db import DatabaseError, IntegrityError
from django.shortcuts import render

from apps.agricultural.models import Zone, State, Cultivation, Domain
from apps.irrigation.models import Method, Team, IrrigationGroup, NutritionLaw, Operator, Registration, \
    DetailRegistration, RegisterPulses, DetailRequirement, ConsumptionRequirement
import decimal
from datetime import datetime
from http import HTTPStatus
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.template import loader
from django.core import serializers

from apps.agricultural.consult import query_api_amigo
from apps.user.views import create_user


# Create your views here.

# --------------------method-------------------------------------
def get_method_list(request):
    if request.method == 'GET':
        method_set = Method.objects.all()
        return render(request, 'irrigation/method_list.html', {
            'method_set': method_set
        })


def modal_method_save(request):
    if request.method == 'GET':
        t = loader.get_template('irrigation/method_register.html')
        c = ({})
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_method(request):
    if request.method == 'POST':
        _method = request.POST.get('id-method', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        method_obj = Method(
            name=_method,
            user=user_obj
        )
        method_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_method_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        method_obj = Method.objects.get(id=int(pk))
        t = loader.get_template('irrigation/method_update.html')
        c = ({
            'method_obj': method_obj,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_method(request):
    if request.method == 'POST':
        _id = int(request.POST.get('id-pk', ''))
        method_obj = Method.objects.get(id=int(_id))
        _name = request.POST.get('id-method', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        method_obj.name = _name
        method_obj.user = user_obj
        method_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# --------------------irrigation group-------------------------------------
def get_group_list(request):
    if request.method == 'GET':
        group_set = IrrigationGroup.objects.all()
        return render(request, 'irrigation/group_irrigation_list.html', {
            'group_set': group_set
        })


def modal_group_save(request):
    if request.method == 'GET':
        t = loader.get_template('irrigation/group_irrigation_register.html')
        c = ({})
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_group(request):
    if request.method == 'POST':
        _subgroup = request.POST.get('id-subgroup', '')
        _departure_rc = request.POST.get('id-departure_rc', '')
        _family = request.POST.get('id-family', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        group_obj = IrrigationGroup(
            subgroup=_subgroup,
            departure_rc=_departure_rc,
            family=_family,
            user=user_obj
        )
        group_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_group_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        group_obj = IrrigationGroup.objects.get(id=int(pk))
        t = loader.get_template('irrigation/group_irrigation_update.html')
        c = ({
            'group_obj': group_obj,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_group(request):
    if request.method == 'POST':
        _id = int(request.POST.get('id-pk', ''))
        group_obj = IrrigationGroup.objects.get(id=int(_id))
        _subgroup = request.POST.get('id-subgroup', '')
        _departure_rc = request.POST.get('id-departure_rc', '')
        _family = request.POST.get('id-family', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        group_obj.subgroup = _subgroup
        group_obj.departure_rc = _departure_rc
        group_obj.family = _family
        group_obj.user = user_obj
        group_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# --------------------team----------------------------
def get_team_list(request):
    if request.method == 'GET':
        team_set = Team.objects.all()
        return render(request, 'irrigation/team_list.html', {
            'team_set': team_set
        })


def modal_team_save(request):
    if request.method == 'GET':
        zone_set = Zone.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('irrigation/team_register.html')
        c = ({
            'zone_set': zone_set,
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_team(request):
    if request.method == 'POST':
        zone_id = request.POST.get('id-zone', '')
        zone_obj = Zone.objects.get(id=int(zone_id))
        state_id = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(state_id))
        _name = request.POST.get('id-name', '')
        _description = request.POST.get('id-description', '')
        _reservoir = request.POST.get('id-reservoir', '')
        _correction_factor = request.POST.get('id-correction_factor', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        team_obj = Team(
            zone=zone_obj,
            name=_name,
            description=_description,
            reservoir=_reservoir,
            correction_factor=_correction_factor,
            state=state_obj,
            user=user_obj
        )
        team_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_team_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        team_obj = Team.objects.get(id=int(pk))
        zone_set = Zone.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('irrigation/team_update.html')
        c = ({
            'team_obj': team_obj,
            'zone_set': zone_set,
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_team(request):
    if request.method == 'POST':
        _id = int(request.POST.get('id-pk', ''))
        team_obj = Team.objects.get(id=int(_id))
        zone_id = request.POST.get('id-zone', '')
        zone_obj = Zone.objects.get(id=int(zone_id))
        state_id = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(state_id))
        _name = request.POST.get('id-name', '')
        _description = request.POST.get('id-description', '')
        _reservoir = request.POST.get('id-reservoir', '')
        _correction_factor = request.POST.get('id-correction_factor', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))

        team_obj.zone = zone_obj
        team_obj.name = _name
        team_obj.description = _description
        team_obj.reservoir = _reservoir
        team_obj.correction_factor = _correction_factor
        team_obj.state = state_obj
        team_obj.user = user_obj
        team_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# --------------------NutritionLaw----------------------------
def get_law_list(request):
    if request.method == 'GET':
        law_set = NutritionLaw.objects.all()
        return render(request, 'irrigation/law_list.html', {
            'law_set': law_set
        })


def modal_law_save(request):
    if request.method == 'GET':
        group_set = IrrigationGroup.objects.all()
        t = loader.get_template('irrigation/law_register.html')
        c = ({
            'group_set': group_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_law(request):
    if request.method == 'POST':
        _code = request.POST.get('id-code', '')
        _group = request.POST.get('id-group', '')
        group_obj = IrrigationGroup.objects.get(id=int(_group))
        _name = request.POST.get('id-name', '')
        _um = (request.POST.get('id-um', ''))
        _v1 = (request.POST.get('id-v1', '0'))
        if _v1 == '':
            _v1 = 0
        _v2 = (request.POST.get('id-v2', '0'))
        if _v2 == '':
            _v2 = 0
        _v3 = (request.POST.get('id-v3', '0'))
        if _v3 == '':
            _v3 = 0
        _v4 = (request.POST.get('id-v4', '0'))
        if _v4 == '':
            _v4 = 0
        _v5 = (request.POST.get('id-v5', '0'))
        if _v5 == '':
            _v5 = 0
        _v6 = (request.POST.get('id-v6', '0'))
        if _v6 == '':
            _v6 = 0
        _v7 = (request.POST.get('id-v7', '0'))
        if _v7 == '':
            _v7 = 0
        _v8 = (request.POST.get('id-v8', '0'))
        if _v8 == '':
            _v8 = 0
        _v9 = (request.POST.get('id-v9', '0'))
        if _v9 == '':
            _v9 = 0
        _v10 = (request.POST.get('id-v10', '0'))
        if _v10 == '':
            _v10 = 0
        _v11 = (request.POST.get('id-v11', '0'))
        if _v11 == '':
            _v11 = 0
        _v12 = (request.POST.get('id-v12', '0'))
        if _v12 == '':
            _v12 = 0
        _v13 = (request.POST.get('id-v13', '0'))
        if _v13 == '':
            _v13 = 0
        _v14 = (request.POST.get('id-v14', '0'))
        if _v14 == '':
            _v14 = 0
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        law_obj = NutritionLaw(
            code=_code,
            irrigation_group=group_obj,
            name=_name,
            um=_um,
            n=decimal.Decimal(_v1),
            p2o5=decimal.Decimal(_v2),
            k2o=decimal.Decimal(_v3),
            cao=decimal.Decimal(_v4),
            mgo=decimal.Decimal(_v5),
            s=decimal.Decimal(_v6),
            fe=decimal.Decimal(_v7),
            mn=decimal.Decimal(_v8),
            b=decimal.Decimal(_v9),
            zn=decimal.Decimal(_v10),
            mo=decimal.Decimal(_v11),
            ci=decimal.Decimal(_v12),
            cu=decimal.Decimal(_v13),
            h2o=decimal.Decimal(_v14),
            user=user_obj
        )
        law_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_law_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        law_obj = NutritionLaw.objects.get(id=int(pk))
        group_set = IrrigationGroup.objects.all()
        t = loader.get_template('irrigation/law_update.html')
        c = ({
            'group_set': group_set,
            'law_obj': law_obj,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_law(request):
    if request.method == 'POST':
        _id = int(request.POST.get('id-pk', ''))
        law_obj = NutritionLaw.objects.get(id=int(_id))
        _code = request.POST.get('id-code', '')
        _group = request.POST.get('id-group', '')
        group_obj = IrrigationGroup.objects.get(id=int(_group))
        _name = request.POST.get('id-name', '')
        _um = (request.POST.get('id-um', ''))
        _v1 = (request.POST.get('id-v1', '0'))
        if _v1 == '':
            _v1 = 0
        _v2 = (request.POST.get('id-v2', '0'))
        if _v2 == '':
            _v2 = 0
        _v3 = (request.POST.get('id-v3', '0'))
        if _v3 == '':
            _v3 = 0
        _v4 = (request.POST.get('id-v4', '0'))
        if _v4 == '':
            _v4 = 0
        _v5 = (request.POST.get('id-v5', '0'))
        if _v5 == '':
            _v5 = 0
        _v6 = (request.POST.get('id-v6', '0'))
        if _v6 == '':
            _v6 = 0
        _v7 = (request.POST.get('id-v7', '0'))
        if _v7 == '':
            _v7 = 0
        _v8 = (request.POST.get('id-v8', '0'))
        if _v8 == '':
            _v8 = 0
        _v9 = (request.POST.get('id-v9', '0'))
        if _v9 == '':
            _v9 = 0
        _v10 = (request.POST.get('id-v10', '0'))
        if _v10 == '':
            _v10 = 0
        _v11 = (request.POST.get('id-v11', '0'))
        if _v11 == '':
            _v11 = 0
        _v12 = (request.POST.get('id-v12', '0'))
        if _v12 == '':
            _v12 = 0
        _v13 = (request.POST.get('id-v13', '0'))
        if _v13 == '':
            _v13 = 0
        _v14 = (request.POST.get('id-v14', '0'))
        if _v14 == '':
            _v14 = 0
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        law_obj.code = _code
        law_obj.irrigation_group = group_obj
        law_obj.name = _name
        law_obj.um = _um
        law_obj.n = decimal.Decimal(_v1)
        law_obj.p2o5 = decimal.Decimal(_v2)
        law_obj.k2o = decimal.Decimal(_v3)
        law_obj.cao = decimal.Decimal(_v4)
        law_obj.mgo = decimal.Decimal(_v5)
        law_obj.s = decimal.Decimal(_v6)
        law_obj.fe = decimal.Decimal(_v7)
        law_obj.mn = decimal.Decimal(_v8)
        law_obj.b = decimal.Decimal(_v9)
        law_obj.zn = decimal.Decimal(_v10)
        law_obj.mo = decimal.Decimal(_v11)
        law_obj.ci = decimal.Decimal(_v12)
        law_obj.cu = decimal.Decimal(_v13)
        law_obj.h2o = decimal.Decimal(_v14)
        law_obj.user = user_obj
        law_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# -------------------Operators----------------
def get_operators_list(request):
    if request.method == 'GET':
        operators_set = Operator.objects.all()
        return render(request, 'irrigation/operators_list.html', {
            'operators_set': operators_set
        })


def modal_operators_save(request):
    if request.method == 'GET':
        zone_set = Zone.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('irrigation/operators_register.html')
        c = ({
            'zone_set': zone_set,
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_operators(request):
    if request.method == 'POST':
        _zone = request.POST.get('id-zone', '')
        zone_obj = Zone.objects.get(id=int(_zone))
        _code = request.POST.get('id-code', '')
        _document = request.POST.get('id-document', '')
        _description = request.POST.get('id-description', '')
        _function = request.POST.get('id-function', '')
        _state = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        operator_obj = Operator(
            zone=zone_obj,
            code_sap=_code,
            document=_document,
            description=_description,
            function=_function,
            state=state_obj,
            user=user_obj
        )
        operator_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_operators_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        operator_obj = Operator.objects.get(id=int(pk))
        zone_set = Zone.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('irrigation/operators_update.html')
        c = ({
            'zone_set': zone_set,
            'state_set': state_set,
            'operator_obj': operator_obj,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_operators(request):
    if request.method == 'POST':
        _id = int(request.POST.get('id-pk', ''))
        operator_obj = Operator.objects.get(id=int(_id))
        _zone = request.POST.get('id-zone', '')
        zone_obj = Zone.objects.get(id=int(_zone))
        _code = request.POST.get('id-code', '')
        _document = request.POST.get('id-document', '')
        _description = request.POST.get('id-description', '')
        _function = request.POST.get('id-function', '')
        _state = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))

        operator_obj.zone = zone_obj
        operator_obj.code_sap = _code
        operator_obj.document = _document
        operator_obj.description = _description
        operator_obj.function = _function
        operator_obj.state = state_obj
        operator_obj.user = user_obj
        operator_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# -----------Riego y Fertilizacion---------------------
def get_irrigation_list(request):
    if request.method == 'GET':
        irrigation_set = Registration.objects.all()
        return render(request, 'irrigation/irrigation_list.html', {
            'irrigation_set': irrigation_set
        })


def modal_irrigation_save(request):
    if request.method == 'GET':
        cultivation_set = Cultivation.objects.all()
        zone_set = Zone.objects.all()
        domain_set = Domain.objects.all()
        method_set = Method.objects.all()
        team_set = Team.objects.all()
        year_now = (datetime.now()).strftime("%Y")
        t = loader.get_template('irrigation/irrigation_register.html')
        c = ({
            'cultivation_set': cultivation_set,
            'zone_set': zone_set,
            'domain_set': domain_set,
            'method_set': method_set,
            'team_set': team_set,
            'year_now': year_now,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_irrigation(request):
    if request.method == 'POST':
        _year = request.POST.get('id-year', '')
        _week = request.POST.get('id-week', '')
        _number = request.POST.get('id-number', '')
        _pk1 = request.POST.get('id-cultivation', '')
        cultivation_obj = Cultivation.objects.get(id=int(_pk1))
        _pk2 = request.POST.get('id-zone', '')
        zone_obj = Zone.objects.get(id=int(_pk2))
        _pk3 = request.POST.get('id-domain', '')
        domain_obj = Domain.objects.get(id=int(_pk3))
        _pk4 = request.POST.get('id-method', '')
        method_obj = Method.objects.get(id=int(_pk4))
        _pk5 = request.POST.get('id-team', '')
        team_obj = Team.objects.get(id=int(_pk5))
        _area = request.POST.get('id-area', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        registration_obj = Registration(
            number=_number,
            week=_week,
            year=_year,
            cultivation=cultivation_obj,
            domain=domain_obj,
            zone=zone_obj,
            method=method_obj,
            team=team_obj,
            area=decimal.Decimal(_area),
            user=user_obj
        )
        registration_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_irrigation_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        registration_obj = Registration.objects.get(id=int(pk))
        cultivation_set = Cultivation.objects.all()
        zone_set = Zone.objects.all()
        domain_set = Domain.objects.all()
        method_set = Method.objects.all()
        team_set = Team.objects.all()
        t = loader.get_template('irrigation/irrigation_update.html')
        c = ({
            'registration_obj': registration_obj,
            'cultivation_set': cultivation_set,
            'zone_set': zone_set,
            'domain_set': domain_set,
            'method_set': method_set,
            'team_set': team_set
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_irrigation(request):
    if request.method == 'POST':
        _id = int(request.POST.get('id-pk', ''))
        registration_obj = Registration.objects.get(id=int(_id))
        _year = request.POST.get('id-year', '')
        _week = request.POST.get('id-week', '')
        _number = request.POST.get('id-number', '')
        _pk1 = request.POST.get('id-cultivation', '')
        cultivation_obj = Cultivation.objects.get(id=int(_pk1))
        _pk2 = request.POST.get('id-zone', '')
        zone_obj = Zone.objects.get(id=int(_pk2))
        _pk3 = request.POST.get('id-domain', '')
        domain_obj = Domain.objects.get(id=int(_pk3))
        _pk4 = request.POST.get('id-method', '')
        method_obj = Method.objects.get(id=int(_pk4))
        _pk5 = request.POST.get('id-team', '')
        team_obj = Team.objects.get(id=int(_pk5))
        _area = request.POST.get('id-area', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        registration_obj.number = _number
        registration_obj.week = _week
        registration_obj.year = _year
        registration_obj.cultivation = cultivation_obj
        registration_obj.zone = zone_obj
        registration_obj.domain = domain_obj
        registration_obj.team = team_obj
        registration_obj.method = method_obj
        registration_obj.area = decimal.Decimal(_area)
        registration_obj.user = user_obj
        registration_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# -----------Detalle 1 Riego y Fertilizacion---------------------
def get_detail_irrigation_list(request, pk):
    if request.method == 'GET':
        # _pk = request.GET.get('pk', '')
        irrigation_obj = Registration.objects.get(id=int(pk))
        detail_irrigation_set = DetailRegistration.objects.filter(registration=irrigation_obj)
        return render(request, 'irrigation/detail_irrigation_list.html', {
            'detail_irrigation_set': detail_irrigation_set,
            'irrigation_obj': irrigation_obj
        })


def modal_detail_irrigation_save(request):
    if request.method == 'GET':
        _pk = request.GET.get('pk', '')
        date_now = (datetime.now()).strftime("%Y-%m-%d")
        t = loader.get_template('irrigation/detail_irrigation_register.html')
        c = ({
            'date_now': date_now,
            'pk': _pk,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_detail_irrigation(request):
    if request.method == 'POST':
        _pk = request.POST.get('id-register', '')
        register_obj = Registration.objects.get(id=int(_pk))
        _date = request.POST.get('id-date', '')
        _turn = request.POST.get('id-turn', '')
        _valve = request.POST.get('id-valve', '')
        _eto = request.POST.get('id-eto', '')
        _ha = request.POST.get('id-ha', '')
        _kc = request.POST.get('id-kc', '')
        _m3 = request.POST.get('id-m3', '')
        _proportion = request.POST.get('id-proportion', '')
        _solution = request.POST.get('id-solution', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        detail_registration_obj = DetailRegistration(
            registration=register_obj,
            date=_date,
            turn=_turn,
            associated_valve=_valve,
            eto=_eto,
            ha=_ha,
            kc=_kc,
            M3=_m3,
            proportion=_proportion,
            mother_solution=decimal.Decimal(_solution),
            user=user_obj
        )
        detail_registration_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_detail_irrigation_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        detail_irrigation_obj = DetailRegistration.objects.get(id=int(pk))
        t = loader.get_template('irrigation/detail_irrigation_update.html')
        c = ({
            'detail_irrigation_obj': detail_irrigation_obj
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_detail_irrigation(request):
    if request.method == 'POST':
        _pk = request.POST.get('id-pk', '')
        detail_register_obj = DetailRegistration.objects.get(id=int(_pk))
        _date = request.POST.get('id-date', '')
        _turn = request.POST.get('id-turn', '')
        _valve = request.POST.get('id-valve', '')
        _eto = request.POST.get('id-eto', '')
        _ha = request.POST.get('id-ha', '')
        _kc = request.POST.get('id-kc', '')
        _m3 = request.POST.get('id-m3', '')
        _proportion = request.POST.get('id-proportion', '')
        _solution = request.POST.get('id-solution', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        detail_register_obj.date = _date
        detail_register_obj.turn = _turn
        detail_register_obj.associated_valve = _valve
        detail_register_obj.eto = _eto
        detail_register_obj.ha = _ha
        detail_register_obj.kc = _kc
        detail_register_obj.M3 = _m3
        detail_register_obj.proportion = _proportion
        detail_register_obj.mother_solution = _solution
        detail_register_obj.user = user_obj
        detail_register_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def get_detail_pulses(request):
    if request.method == 'GET':
        id_detail_registration = request.GET.get('pk', '')
        detail_registration_obj = DetailRegistration.objects.get(pk=int(id_detail_registration))
        register_pulses_set = RegisterPulses.objects.filter(detail_registration=detail_registration_obj)
        t = loader.get_template('irrigation/detail_pulses_grid_list.html')
        c = ({
            'register_pulses_set': register_pulses_set,
        })
        return JsonResponse({
            'grid': t.render(c, request),
        }, status=HTTPStatus.OK)


def modal_save_pulses(request):
    if request.method == 'GET':
        _pk = request.GET.get('pk', '')
        t = loader.get_template('irrigation/detail_pulses_register.html')
        c = ({
            'pk': _pk,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_detail_pulses(request):
    if request.method == 'POST':
        _p = request.POST.get('id-dp', '')
        detail_register_obj = DetailRegistration.objects.get(id=int(_p))
        _name = request.POST.get('id-name-pulse', '')
        _pulse = request.POST.get('id-pulse', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        register_pulse_obj = RegisterPulses(
            detail_registration=detail_register_obj,
            name=_name,
            pulse=_pulse,
            user=user_obj
        )
        register_pulse_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_update_pulses(request):
    if request.method == 'GET':
        _pk = request.GET.get('pk', '')
        register_pulses_obj = RegisterPulses.objects.get(id=int(_pk))
        t = loader.get_template('irrigation/detail_pulses_update.html')
        c = ({
            'register_pulses_obj': register_pulses_obj,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_detail_pulses(request):
    if request.method == 'POST':
        _rp = request.POST.get('id-pk', '')
        _name = request.POST.get('id-name-pulse', '')
        _pulse = request.POST.get('id-pulse', '')
        register_pulses_obj = RegisterPulses.objects.get(id=int(_rp))
        register_pulses_obj.name = _name
        register_pulses_obj.pulse = _pulse
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        register_pulses_obj.user = user_obj
        register_pulses_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# -----------Detalle 2 Requerimiento y Fertilizacion---------------------
def request_irrigation_list(request, pk):
    if request.method == 'GET':
        irrigation_obj = Registration.objects.get(id=int(pk))
        request_irrigation_set = DetailRequirement.objects.filter(registration=irrigation_obj)
        return render(request, 'irrigation/request_irrigation_list.html', {
            'request_irrigation_set': request_irrigation_set,
            'irrigation_obj': irrigation_obj
        })


def modal_request_irrigation_save(request):
    if request.method == 'GET':
        _pk = request.GET.get('pk', '')
        nutrition_set = NutritionLaw.objects.all()
        t = loader.get_template('irrigation/request_irrigation_register.html')
        c = ({
            'nutrition_set': nutrition_set,
            'pk': _pk
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_request_irrigation(request):
    if request.method == 'POST':
        _p = request.POST.get('id-dp', '')
        registration_obj = Registration.objects.get(id=int(_p))
        pk = request.POST.get('id-product', '')
        nutrition_obj = NutritionLaw.objects.get(id=int(pk))
        _monday = request.POST.get('id-monday', '')
        _tuesday = request.POST.get('id-tuesday', '')
        _wednesday = request.POST.get('id-wednesday', '')
        _thursday = request.POST.get('id-thursday', '')
        _friday = request.POST.get('id-friday', '')
        _saturday = request.POST.get('id-saturday', '')
        _sunday = request.POST.get('id-sunday', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        request_irrigation_obj = DetailRequirement(
            registration=registration_obj,
            nutrition=nutrition_obj,
            monday=_monday,
            tuesday=_tuesday,
            wednesday=_wednesday,
            thursday=_thursday,
            friday=_friday,
            saturday=_saturday,
            sunday=_sunday,
            user=user_obj
        )
        request_irrigation_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


@csrf_exempt
def set_consumed_requirement(request):
    data = {}
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        try:
            detail_requirement_obj = DetailRequirement.objects.get(id=pk)
        except DetailRequirement.DoesNotExist:
            data['error'] = "Problemas al obtener datos!"
            response = JsonResponse(data)
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response
        date_now = (datetime.now()).strftime("%Y-%m-%d")
        t = loader.get_template('irrigation/request_consumed_list.html')
        c = ({
            'detail_requirement_obj': detail_requirement_obj,
            'date_now': date_now,
        })

        consumption_requirement_set = ConsumptionRequirement.objects.filter(
            detail_requirement=detail_requirement_obj).order_by('id')
        tpl2 = loader.get_template('irrigation/request_consumed_grid_list.html')
        context2 = ({'consumption_requirement_set': consumption_requirement_set, })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
            'grid': tpl2.render(context2)
        }, status=HTTPStatus.OK)
    else:
        if request.method == 'POST':
            _date = request.POST.get('id-dates', '')
            _consumed = request.POST.get('id-consumed', '')
            _pk = request.POST.get('id-pk', '')
            detail_requirement_obj = DetailRequirement.objects.get(id=int(_pk))

            if decimal.Decimal(_consumed) == 0:
                data['error'] = "Ingrese valores validos."
                response = JsonResponse(data)
                response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                return response
            user_id = request.user.id
            user_obj = User.objects.get(id=int(user_id))
            try:
                consumption_requirement_obj = ConsumptionRequirement(
                    detail_requirement=detail_requirement_obj,
                    date=_date,
                    consumption=decimal.Decimal(_consumed),
                    user=user_obj
                )
                consumption_requirement_obj.save()
            except DatabaseError as e:
                data['error'] = str(e)
                response = JsonResponse(data)
                response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                return response
            except IntegrityError as e:
                data['error'] = str(e)
                response = JsonResponse(data)
                response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                return response

            consumption_requirement_set = ConsumptionRequirement.objects.filter(
                detail_requirement=detail_requirement_obj).order_by('id')
            tpl2 = loader.get_template('irrigation/request_consumed_grid_list.html')
            context2 = ({'consumption_requirement_set': consumption_requirement_set, })

            return JsonResponse({
                'message': 'Se registro con exito.',
                'grid': tpl2.render(context2),
            }, status=HTTPStatus.OK)


def get_consumed_detail(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        consumed_requirement_obj = ConsumptionRequirement.objects.filter(id=int(pk))
        serialized_obj = serializers.serialize('json', consumed_requirement_obj)
        return JsonResponse({'obj': serialized_obj}, status=HTTPStatus.OK)
    return JsonResponse({'message': 'Error de peticion.'}, status=HTTPStatus.BAD_REQUEST)


def update_consumed_requirement(request):
    data = dict()
    if request.method == 'POST':
        _pk = request.POST.get('pk_consumed', '')
        consumption_requirement_obj = ConsumptionRequirement.objects.get(id=int(_pk))
        _dates = request.POST.get('id-dates', '')
        _consumed = request.POST.get('id-consumed', '')
        if decimal.Decimal(_consumed) == 0:
            data['error'] = "Ingrese valores validos."
            response = JsonResponse(data)
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response
        consumption_requirement_obj.date = _dates
        consumption_requirement_obj.consumption = _consumed
        consumption_requirement_obj.save()
        consumption_requirement_set = ConsumptionRequirement.objects.filter(
            detail_requirement=consumption_requirement_obj.detail_requirement).order_by('id')
        tpl2 = loader.get_template('irrigation/request_consumed_grid_list.html')
        context2 = ({'consumption_requirement_set': consumption_requirement_set, })
        return JsonResponse({
            'message': 'Informacion actualizada con exito.',
            'grid': tpl2.render(context2),
        }, status=HTTPStatus.OK)
    return JsonResponse({'message': 'Error de peticion.'}, status=HTTPStatus.BAD_REQUEST)
