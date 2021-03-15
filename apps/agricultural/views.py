from datetime import datetime
from http import HTTPStatus
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.template import loader
from apps.agricultural.models import Person, Business


class Home(TemplateView):
    template_name = 'index.html'

# lista de empleados
def get_employee_list(request):
    if request.method == 'GET':
        employee_set = Person.objects.all()
        my_date = datetime.now()
        date_now = my_date.strftime("%Y-%m")
        return render(request, 'agricultural/employee_list.html', {
            'date_now': date_now,
            'employee_set': employee_set,
        })


# abrir el formulario de registro
def get_employee_form(request):
    if request.method == 'GET':
        my_date = datetime.now()
        date_now = my_date.strftime("%Y-%m-%d")
        business_set = Business.objects.all()
        t = loader.get_template('agricultural/employee_form.html')
        c = ({
            'date_now': date_now,
            'type': Person._meta.get_field('type').choices,
            'business_set': business_set,
        })
        return JsonResponse({
            'form': t.render(c, request),
        })


#
# # registrar empleado
@csrf_exempt
def save_person(request):
    if request.method == 'POST':
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        _document = request.POST.get('document', '')
        _paternal_last_name = request.POST.get('paternal', '')
        _maternal_last_name = request.POST.get('maternal', '')
        _names = request.POST.get('names', '')
        _birth_date = request.POST.get('birth_date', '')
        _occupation = request.POST.get('occupation', '')
        _telephone = request.POST.get('telephone', '')
        _email = request.POST.get('email', '')
        _address = request.POST.get('address', '')
        _state = bool(request.POST.get('checkbox', ''))
        _business_id = request.POST.get('business', '')
        business_obj = Business.objects.get(id=int(_business_id))
        try:
            _photo = request.FILES['customFile']
        except Exception as e:
            _photo = 'person/employee0.jpg'

        person_obj = Person(
            document=_document,
            paternal_last_name=_paternal_last_name,
            maternal_last_name=_maternal_last_name,
            names=_names,
            birth_date=_birth_date,
            telephone=_telephone,
            email=_email,
            address=_address,
            type=_occupation,
            is_state=_state,
            photo=_photo,
            business=business_obj,
            user=user_obj,
        )
        person_obj.save()
        return JsonResponse({
            'message': True,
            'resp': 'Se registro exitosamente',
        }, status=HTTPStatus.OK)


def get_employee_update_form(request):
    if request.method == 'GET':
        pk = int(request.GET.get('pk', ''))
        person_obj = Person.objects.get(id=pk)
        business_set = Business.objects.all()
        t = loader.get_template('agricultural/employee_update_form.html')
        c = ({
            'person_obj': person_obj,
            'type': Person._meta.get_field('type').choices,
            'business_set': business_set,
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
        person_obj = Person.objects.get(id=_id)
        _document = request.POST.get('document', '')
        _paternal_last_name = request.POST.get('paternal', '')
        _maternal_last_name = request.POST.get('maternal', '')
        _names = request.POST.get('names', '')
        _birth_date = request.POST.get('birth_date', '')
        _occupation = request.POST.get('occupation', '')
        _telephone = request.POST.get('telephone', '')
        _email = request.POST.get('email', '')
        _address = request.POST.get('address', '')
        _business_id = request.POST.get('business', '')
        business_obj = Business.objects.get(id=int(_business_id))
        _photo = request.FILES.get('customFile', False)
        _state = bool(request.POST.get('checkbox', ''))

        person_obj.document = _document
        person_obj.birth_date = _birth_date
        person_obj.paternal_last_name = _paternal_last_name
        person_obj.maternal_last_name = _maternal_last_name
        person_obj.names = _names
        person_obj.type = _occupation
        person_obj.telephone = _telephone
        person_obj.email = _email
        person_obj.address = _address
        person_obj.business = business_obj
        if _photo is not False:
            person_obj.photo = _photo
        person_obj.is_state = _state
        person_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)


