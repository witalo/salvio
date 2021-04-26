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
from apps.agricultural.models import Person, Business, Module, Domain, State, Zone, Lot, Cultivation, Variety, \
    Phenology, ProgramProduction
from apps.user.views import create_user


class Home(TemplateView):
    template_name = 'index.html'


# lista de empleados
def get_employee_list(request):
    if request.method == 'GET':
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        if user_obj.is_staff:
            user_set = User.objects.all()
        else:
            user_set = User.objects.filter(id=int(user_id))
        return render(request, 'agricultural/employee_list.html', {
            'employee_set': user_set,
        })


# abrir el formulario de registro
def get_employee_form(request):
    if request.method == 'GET':
        my_date = datetime.now()
        date_now = my_date.strftime("%Y-%m-%d")
        t = loader.get_template('agricultural/employee_form.html')
        c = ({
            'date_now': date_now,
            'charge': Person._meta.get_field('charge').choices,
        })
        return JsonResponse({
            'form': t.render(c, request),
        })


# # registrar empleado
@csrf_exempt
def save_person(request):
    if request.method == 'POST':
        _document = request.POST.get('id-document', '')
        _last_name = request.POST.get('id-last-name', '')
        _first_name = request.POST.get('id-first-name', '')
        _birth_date = request.POST.get('id-birth-date', '')
        _charge = request.POST.get('id-charge', '')
        _telephone = request.POST.get('id-telephone', '')
        _email = request.POST.get('id-email', '')
        _address = request.POST.get('id-address', '')
        _user = request.POST.get('id-user', '')
        _password = request.POST.get('id-password', '')
        try:
            _photo = request.FILES['customFile']
        except Exception as e:
            _photo = 'person/employee0.jpg'

        person_obj = Person(
            user=create_user(_first_name, _last_name, _email, _user, _password),
            document=_document,
            birth_date=_birth_date,
            telephone=_telephone,
            address=_address,
            charge=_charge,
            photo=_photo,
        )
        person_obj.save()
        return JsonResponse({
            'message': True,
            'resp': 'Se registro exitosamente',
        }, status=HTTPStatus.OK)


def get_employee_update_form(request):
    if request.method == 'GET':
        pk = int(request.GET.get('pk', ''))
        user_obj = User.objects.get(id=pk)
        t = loader.get_template('agricultural/employee_update_form.html')
        c = ({
            'user_obj': user_obj,
            'charge': Person._meta.get_field('charge').choices,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


# Actualizacion persona
@csrf_exempt
def update_person(request):
    if request.method == 'POST':
        _id = int(request.POST.get('pk', ''))
        user_obj = User.objects.get(id=_id)
        _document = request.POST.get('id-document', '')
        _last_name = request.POST.get('id-last-name', '')
        _first_name = request.POST.get('id-first-name', '')
        _birth_date = request.POST.get('id-birth-date', '')
        _charge = request.POST.get('id-charge', '')
        _telephone = request.POST.get('id-telephone', '')
        _email = request.POST.get('id-email', '')
        _address = request.POST.get('id-address', '')
        _user = request.POST.get('id-user', '')
        _password = request.POST.get('id-password', '')
        _photo = request.FILES.get('customFile', False)

        if _user != '':
            try:
                _search = User.objects.get(username=_user).id
            except User.DoesNotExist:
                _search = None
            if _search is not None:
                if _search != user_obj.id:
                    response = JsonResponse({'error': "Este usuario ya existe."})
                    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                    return response

            user_obj.email = _email
            user_obj.first_name = _first_name
            user_obj.last_name = _last_name
            user_obj.username = _user
            user_obj.set_password(_password)
            user_obj.save()

            person_obj = Person.objects.get(user=user_obj)
            person_obj.document = _document
            person_obj.birth_date = _birth_date
            person_obj.charge = _charge
            person_obj.telephone = _telephone
            person_obj.address = _address
            if _photo is not False:
                person_obj.photo = _photo
            person_obj.save()
            return JsonResponse({
                'success': True,
            }, status=HTTPStatus.OK)


def get_business_list(request):
    if request.method == 'GET':
        business_set = Business.objects.all()
        return render(request, 'agricultural/business_list.html', {
            'business_set': business_set,
        })


def get_business_by_document(request):
    data = {}
    if request.method == 'GET':
        number_document = request.GET.get('number_document', '')
        type_document = request.GET.get('type_document', '')
        if type_document == '06':
            type_name = 'RUC'
            r = query_api_amigo(number_document, type_name)
            if r.get('ruc') == number_document:
                name_business = (r.get('business_name')).strip()
                address_business = (r.get('address')).strip()
                return JsonResponse({
                    'names': name_business,
                    'address': address_business},
                    status=HTTPStatus.OK)
            else:
                data = {'error': 'No hay resultados con este numero de RUC'}
                response = JsonResponse(data)
                response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                return response


@csrf_exempt
def save_business(request):
    if request.method == 'POST':
        _ruc = request.POST.get('id-ruc', '')
        _business = request.POST.get('id-business', '')
        _telephone = request.POST.get('id-telephone', '')
        _address = request.POST.get('id-address', '')
        _document = request.POST.get('id-document', '')
        _representative = request.POST.get('id-legal_representative', '')
        business_obj = Business(
            ruc=_ruc,
            business_name=_business,
            phone=_telephone,
            address=_address,
            legal_representative_name=_representative,
            legal_representative_dni=_document
        )
        business_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def get_business_form(request):
    if request.method == 'GET':
        t = loader.get_template('agricultural/register_business.html')
        c = ({})
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


def modal_update_business(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        business_obj = Business.objects.get(id=int(pk))
        t = loader.get_template('agricultural/update_business.html')
        c = ({'business_obj': business_obj})
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_business(request):
    if request.method == 'POST':
        _id = int(request.POST.get('pk', ''))
        business_obj = Business.objects.get(id=_id)
        _ruc = request.POST.get('id-ruc', '')
        _business_name = request.POST.get('id-business', '')
        _phone = request.POST.get('id-telephone', '')
        _address = request.POST.get('id-address', '')
        _document = request.POST.get('id-document', '')
        _representative = request.POST.get('id-legal_representative', '')

        business_obj.ruc = _ruc
        business_obj.business_name = _business_name
        business_obj.phone = _phone
        business_obj.address = _address
        business_obj.legal_representative_dni = _document
        business_obj.legal_representative_name = _representative
        business_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# --------------------module-------------------------------------
def get_module_list(request):
    if request.method == 'GET':
        module_set = Module.objects.all()
        return render(request, 'agricultural/module_list.html', {
            'module_set': module_set,
        })


def modal_module_save(request):
    if request.method == 'GET':
        domain_set = Domain.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('agricultural/register_module.html')
        c = ({
            'domain_set': domain_set,
            'state_set': state_set
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_modulo(request):
    if request.method == 'POST':
        _pk = request.POST.get('id-domain', '')
        domain_obj = Domain.objects.get(id=int(_pk))
        _name = request.POST.get('id-module', '')
        _state = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        module_obj = Module(
            domain=domain_obj,
            name=_name,
            state=state_obj,
            user=user_obj
        )
        module_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_module_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        module_obj = Module.objects.get(id=int(pk))
        domain_set = Domain.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('agricultural/update_module.html')
        c = ({
            'module_obj': module_obj,
            'domain_set': domain_set,
            'state_set': state_set
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_modulo(request):
    if request.method == 'POST':
        _id = int(request.POST.get('id-pk', ''))
        _name = request.POST.get('id-module', '')
        module_obj = Module.objects.get(id=_id)
        _domain = request.POST.get('id-domain', '')
        domain_obj = Domain.objects.get(id=int(_domain))
        _state = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))

        module_obj.name = _name
        module_obj.domain = domain_obj
        module_obj.state = state_obj
        module_obj.user = user_obj
        module_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# --------------------domain-------------------------------------
def get_domain_list(request):
    if request.method == 'GET':
        domain_set = Domain.objects.all()
        return render(request, 'agricultural/domain_list.html', {
            'domain_set': domain_set,
        })


def modal_domain_save(request):
    if request.method == 'GET':
        business_set = Business.objects.all()
        zone_set = Zone.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('agricultural/domain_register.html')
        c = ({
            'business_set': business_set,
            'zone_set': zone_set,
            'state_set': state_set
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_domain(request):
    if request.method == 'POST':
        _abbreviation = request.POST.get('id-abbreviation', '')
        _name = request.POST.get('id-domain', '')
        _zone_pk = request.POST.get('id-zone', '')
        zone_obj = Zone.objects.get(id=int(_zone_pk))
        _business_pk = request.POST.get('id-business', '')
        business_obj = Business.objects.get(id=int(_business_pk))
        _state_pk = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state_pk))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        domain_obj = Domain(
            abbreviation=_abbreviation,
            name=_name,
            zone=zone_obj,
            business=business_obj,
            state=state_obj,
            user=user_obj
        )
        domain_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_domain_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        domain_obj = Domain.objects.get(id=int(pk))
        zone_set = Zone.objects.all()
        business_set = Business.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('agricultural/domain_update.html')
        c = ({
            'domain_obj': domain_obj,
            'zone_set': zone_set,
            'business_set': business_set,
            'state_set': state_set
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_domain(request):
    if request.method == 'POST':
        _pk = request.POST.get('id-pk', '')
        domain_obj = Domain.objects.get(id=int(_pk))
        _abbreviation = request.POST.get('id-abbreviation', '')
        _name = request.POST.get('id-domain', '')
        _zone_pk = request.POST.get('id-zone', '')
        zone_obj = Zone.objects.get(id=int(_zone_pk))
        _business_pk = request.POST.get('id-business', '')
        business_obj = Business.objects.get(id=int(_business_pk))
        _state_pk = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state_pk))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))

        domain_obj.abbreviation = _abbreviation
        domain_obj.name = _name
        domain_obj.zone = zone_obj
        domain_obj.business = business_obj
        domain_obj.state = state_obj
        domain_obj.user = user_obj
        domain_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# --------------------zone-------------------------------------
def get_zone_list(request):
    if request.method == 'GET':
        zone_set = Zone.objects.all()
        return render(request, 'agricultural/zone_list.html', {
            'zone_set': zone_set,
        })


def modal_zone_save(request):
    if request.method == 'GET':
        t = loader.get_template('agricultural/zone_register.html')
        c = ({
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_zone(request):
    if request.method == 'POST':
        _code = request.POST.get('id-code', '')
        _name = request.POST.get('id-zone', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        zone_obj = Zone(
            code=_code,
            name=_name,
            user=user_obj
        )
        zone_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_zone_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        zone_obj = Zone.objects.get(id=int(pk))
        t = loader.get_template('agricultural/zone_update.html')
        c = ({
            'zone_obj': zone_obj,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_zone(request):
    if request.method == 'POST':
        _pk = request.POST.get('id-pk', '')
        zone_obj = Zone.objects.get(id=int(_pk))
        _code = request.POST.get('id-code', '')
        _name = request.POST.get('id-zone', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))

        zone_obj.code = _code
        zone_obj.name = _name
        zone_obj.user = user_obj
        zone_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# --------------------lot-------------------------------------
def get_lot_list(request):
    if request.method == 'GET':
        lot_set = Lot.objects.all()
        return render(request, 'agricultural/lot_list.html', {
            'lot_set': lot_set
        })


def modal_lot_save(request):
    if request.method == 'GET':
        domain_set = Domain.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('agricultural/lot_register.html')
        c = ({
            'domain_set': domain_set,
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_lot(request):
    if request.method == 'POST':
        _name = request.POST.get('id-lot', '')
        _module_pk = request.POST.get('id-module', '')
        module_obj = Module.objects.get(id=int(_module_pk))
        _state_pk = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state_pk))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        lot_obj = Lot(
            name=_name,
            module=module_obj,
            state=state_obj,
            user=user_obj
        )
        lot_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_lot_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        lot_obj = Lot.objects.get(id=int(pk))
        domain_set = Domain.objects.all()
        module_set = Module.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('agricultural/lot_update.html')
        c = ({
            'lot_obj': lot_obj,
            'domain_set': domain_set,
            'module_set': module_set,
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_lot(request):
    if request.method == 'POST':
        _pk = request.POST.get('id-pk', '')
        lot_obj = Lot.objects.get(id=int(_pk))
        _name = request.POST.get('id-lot', '')
        _module_pk = request.POST.get('id-module', '')
        module_obj = Module.objects.get(id=int(_module_pk))
        _code1 = request.POST.get('id-code1', '')
        _code2 = request.POST.get('id-code2', '')
        _state_pk = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state_pk))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))

        lot_obj.name = _name
        lot_obj.module = module_obj
        lot_obj.code_alternate1 = _code1
        lot_obj.code_alternate2 = _code2
        lot_obj.state = state_obj
        lot_obj.user = user_obj
        lot_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# --------------------cultivation-------------------------------------
def get_cultivation_list(request):
    if request.method == 'GET':
        cultivation_set = Cultivation.objects.all()
        return render(request, 'agricultural/cultivation_list.html', {
            'cultivation_set': cultivation_set
        })


def modal_cultivation_save(request):
    if request.method == 'GET':
        state_set = State.objects.all()
        t = loader.get_template('agricultural/cultivation_register.html')
        c = ({
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_cultivation(request):
    if request.method == 'POST':
        _abbreviation = request.POST.get('id-abbreviation', '')
        _name = request.POST.get('id-cultivation', '')
        _state_pk = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state_pk))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        cultivation_obj = Cultivation(
            abbreviation=_abbreviation,
            name=_name,
            state=state_obj,
            user=user_obj
        )
        cultivation_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_cultivation_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        state_set = State.objects.all()
        cultivation_obj = Cultivation.objects.get(id=int(pk))
        t = loader.get_template('agricultural/cultivation_update.html')
        c = ({
            'cultivation_obj': cultivation_obj,
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_cultivation(request):
    if request.method == 'POST':
        _pk = request.POST.get('id-pk', '')
        cultivation_obj = Cultivation.objects.get(id=int(_pk))
        _abbreviation = request.POST.get('id-abbreviation', '')
        _name = request.POST.get('id-cultivation', '')
        _state_pk = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state_pk))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))

        cultivation_obj.abbreviation = _abbreviation
        cultivation_obj.name = _name
        cultivation_obj.state = state_obj
        cultivation_obj.user = user_obj
        cultivation_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# --------------------variety-------------------------------------
def get_variety_list(request):
    if request.method == 'GET':
        variety_set = Variety.objects.all()
        return render(request, 'agricultural/variety_list.html', {
            'variety_set': variety_set
        })


def modal_variety_save(request):
    if request.method == 'GET':
        cultivation_set = Cultivation.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('agricultural/variety_register.html')
        c = ({
            'cultivation_set': cultivation_set,
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_variety(request):
    if request.method == 'POST':
        _abbreviation = request.POST.get('id-abbreviation', '')
        _name = request.POST.get('id-variety', '')
        _cultivation_pk = request.POST.get('id-cultivation', '')
        cultivation_obj = Cultivation.objects.get(id=int(_cultivation_pk))
        _state_pk = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state_pk))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        variety_obj = Variety(
            abbreviation=_abbreviation,
            name=_name,
            cultivation=cultivation_obj,
            state=state_obj,
            user=user_obj
        )
        variety_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_variety_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        variety_obj = Variety.objects.get(id=int(pk))
        cultivation_set = Cultivation.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('agricultural/variety_update.html')
        c = ({
            'variety_obj': variety_obj,
            'cultivation_set': cultivation_set,
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_variety(request):
    if request.method == 'POST':
        _pk = request.POST.get('id-pk', '')
        variety_obj = Variety.objects.get(id=int(_pk))
        _abbreviation = request.POST.get('id-abbreviation', '')
        _name = request.POST.get('id-variety', '')
        _cultivation_pk = request.POST.get('id-cultivation', '')
        cultivation_obj = Cultivation.objects.get(id=int(_cultivation_pk))
        _state_pk = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state_pk))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        variety_obj.abbreviation = _abbreviation
        variety_obj.name = _name
        variety_obj.cultivation = cultivation_obj
        variety_obj.state = state_obj
        variety_obj.user = user_obj
        variety_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


# --------------------phenology-------------------------------------
def get_phenology_list(request):
    if request.method == 'GET':
        phenology_set = Phenology.objects.all()
        return render(request, 'agricultural/phenology_list.html', {
            'phenology_set': phenology_set
        })


def modal_phenology_save(request):
    if request.method == 'GET':
        cultivation_set = Cultivation.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('agricultural/phenology_register.html')
        c = ({
            'cultivation_set': cultivation_set,
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def save_phenology(request):
    if request.method == 'POST':
        _index = request.POST.get('id-index', '')
        _name = request.POST.get('id-phenology', '')
        _cultivation_pk = request.POST.get('id-cultivation', '')
        cultivation_obj = Cultivation.objects.get(id=int(_cultivation_pk))
        _state_pk = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state_pk))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        phenology_obj = Phenology(
            index=_index,
            name=_name,
            cultivation=cultivation_obj,
            state=state_obj,
            user=user_obj
        )
        phenology_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def modal_phenology_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        phenology_obj = Phenology.objects.get(id=int(pk))
        cultivation_set = Cultivation.objects.all()
        state_set = State.objects.all()
        t = loader.get_template('agricultural/phenology_update.html')
        c = ({
            'phenology_obj': phenology_obj,
            'cultivation_set': cultivation_set,
            'state_set': state_set,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def update_phenology(request):
    if request.method == 'POST':
        _pk = request.POST.get('id-pk', '')
        phenology_obj = Phenology.objects.get(id=int(_pk))
        _index = request.POST.get('id-index', '')
        _name = request.POST.get('id-phenology', '')
        _cultivation_pk = request.POST.get('id-cultivation', '')
        cultivation_obj = Cultivation.objects.get(id=int(_cultivation_pk))
        _state_pk = request.POST.get('id-state', '')
        state_obj = State.objects.get(id=int(_state_pk))
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        phenology_obj.index = _index
        phenology_obj.name = _name
        phenology_obj.cultivation = cultivation_obj
        phenology_obj.state = state_obj
        phenology_obj.user = user_obj
        phenology_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


def get_module_by_domain(request):
    if request.method == 'GET':
        pk = request.GET.get('ip', '')
        domain_obj = Domain.objects.get(pk=int(pk))
        module_set = Module.objects.filter(domain=domain_obj)
        module_serialized_obj = serializers.serialize('json', module_set)

        return JsonResponse({
            'module': module_serialized_obj
        }, status=HTTPStatus.OK)


# --------------------program of production-------------------------------------
def get_program_production_list(request):
    if request.method == 'GET':
        program_production_set = ProgramProduction.objects.all()
        return render(request, 'agricultural/production_program_list.html', {
            'program_production_set': program_production_set
        })


def modal_program_production_save(request):
    if request.method == 'GET':
        domain_set = Domain.objects.all()
        cultivation_set = Cultivation.objects.all()
        t = loader.get_template('agricultural/production_program_register.html')
        c = ({
            'domain_set': domain_set,
            'cultivation_set': cultivation_set,
            'sowing_set': ProgramProduction._meta.get_field('sowing').choices,
            'state_set': ProgramProduction._meta.get_field('status').choices,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


def modal_update_form(request):
    if request.method == 'GET':
        program_id = request.GET.get('pk', '')
        program_obj = ProgramProduction.objects.get(id=int(program_id))
        domain_set = Domain.objects.all()
        module_set = Module.objects.all()
        lot_set = Lot.objects.all()
        cultivation_set = Cultivation.objects.all()
        variety_set = Variety.objects.all()
        t = loader.get_template('agricultural/production_program_update.html')
        c = ({
            'program_obj': program_obj,
            'domain_set': domain_set,
            'module_set': module_set,
            'lot_set': lot_set,
            'cultivation_set': cultivation_set,
            'variety_set': variety_set,
            'sowing_set': ProgramProduction._meta.get_field('sowing').choices,
            'state_set': ProgramProduction._meta.get_field('status').choices,
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


def get_module_by_domain(request):
    if request.method == 'GET':
        domain_id = request.GET.get('_pk', '')
        domain_obj = Domain.objects.get(id=int(domain_id))
        module_set = Module.objects.filter(domain=domain_obj)
        module_serialized_obj = serializers.serialize('json', module_set)
        return JsonResponse({
            'modules_set': module_serialized_obj,
        }, status=HTTPStatus.OK)


def get_lot_by_module(request):
    if request.method == 'GET':
        module_id = request.GET.get('_pk', '')
        module_obj = Module.objects.get(id=int(module_id))
        lot_set = Lot.objects.filter(module=module_obj)
        lot_serialized_obj = serializers.serialize('json', lot_set)
        return JsonResponse({
            'lot_set': lot_serialized_obj,
        }, status=HTTPStatus.OK)


def get_variety_by_cultivation(request):
    if request.method == 'GET':
        cultivation_id = request.GET.get('_pk', '')
        cultivation_obj = Cultivation.objects.get(id=int(cultivation_id))
        variety_set = Variety.objects.filter(cultivation=cultivation_obj)
        variety_set_serialized_obj = serializers.serialize('json', variety_set)
        return JsonResponse({
            'variety_set': variety_set_serialized_obj,
        }, status=HTTPStatus.OK)


@csrf_exempt
def save_program(request):
    if request.method == 'POST':
        id_lot = request.POST.get('id_lot', '')
        lot_obj = Lot.objects.get(id=int(id_lot))
        number_campaign = request.POST.get('number_campaign', '')
        year_campaign = request.POST.get('year_campaign', '')
        id_variety = request.POST.get('id_variety', '')
        variety_obj = Variety.objects.get(id=int(id_variety))
        id_area = decimal.Decimal(request.POST.get('id_area', ''))
        date_campaign = request.POST.get('date_campaign', '')
        id_density = request.POST.get('density', '')
        id_sowing = request.POST.get('id_sowing', '')
        id_state = request.POST.get('id_state', '')
        id_responsible = request.POST.get('id_responsible', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        program_production_obj = ProgramProduction(
            lot=lot_obj,
            campaign_number=number_campaign,
            campaign_year=year_campaign,
            variety=variety_obj,
            area=id_area,
            campaign_closure=date_campaign,
            density=id_density,
            sowing=id_sowing,
            responsible=id_responsible,
            status=id_state,
            user=user_obj
        )
        program_production_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


@csrf_exempt
def update_program(request):
    if request.method == 'POST':
        pk = request.POST.get('id-pk', '')
        program_obj = ProgramProduction.objects.get(id=int(pk))
        id_lot = request.POST.get('id_lot', '')
        lot_obj = Lot.objects.get(id=int(id_lot))
        number_campaign = request.POST.get('number_campaign', '')
        year_campaign = request.POST.get('year_campaign', '')
        id_variety = request.POST.get('id_variety', '')
        variety_obj = Variety.objects.get(id=int(id_variety))
        id_area = decimal.Decimal(request.POST.get('id_area', ''))
        date_campaign = request.POST.get('date_campaign', '')
        id_density = request.POST.get('density', '')
        id_sowing = request.POST.get('id_sowing', '')
        id_state = request.POST.get('id_state', '')
        id_responsible = request.POST.get('id_responsible', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        program_obj.lot = lot_obj
        program_obj.variety = variety_obj
        program_obj.campaign_number = number_campaign
        program_obj.campaign_year = year_campaign
        program_obj.area = id_area
        program_obj.campaign_closure = date_campaign
        program_obj.density = id_density
        program_obj.sowing = id_sowing
        program_obj.status = id_state
        program_obj.responsible = id_responsible
        program_obj.user = user_obj
        program_obj.save()

        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)
