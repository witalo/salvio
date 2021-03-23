from datetime import datetime
from http import HTTPStatus
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.template import loader

from apps.agricultural.consult import query_api_amigo
from apps.agricultural.models import Person, Business, Module, Domain, State
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
        _name = int(request.POST.get('id-module', ''))
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
