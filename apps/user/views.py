from http import HTTPStatus

from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, JsonResponse
from .forms import FormLogin
from ..agricultural.models import Person


class Login(FormView):
    template_name = 'login.html'
    form_class = FormLogin
    success_url = reverse_lazy('home')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


# creacion de usuario
def create_user(first_name_=None, last_name_=None, email_=None, user_=None, password_=None):
    staff = False
    if user_ != '' and user_ != None:
        try:
            user_obj = User.objects.get(username=user_)
        except User.DoesNotExist:
            user_obj = None

        if user_obj is not None:
            message = 'El usuario ya se encuentra registrado'
            return message
        if password_ == '' or password_ == None:
            message = 'Ingrese una contraseña valida'
            return message
        user_obj = User(
            first_name=first_name_,
            last_name=last_name_,
            username=user_,
            email=email_,
        )
        user_obj.set_password(password_)
        user_obj.is_staff = staff
        user_obj.save()
        return user_obj
    else:
        message = 'Ingrese un usuario valido'
        return message


# creacion de usuario
@csrf_exempt
def update_user(request):
    if request.method == 'POST':
        _id = int(request.POST.get('pk'))
        user_obj = User.objects.get(id=_id)
        _username = request.POST.get('username')
        _password = request.POST.get('password')
        is_staff = False
        if request.POST.get('is_staff') is not None:
            is_staff = bool(request.POST.get('is_staff'))

        if _username != '':
            try:
                _search = User.objects.get(username=_username).id
            except User.DoesNotExist:
                _search = None
        if _search is not None:
            if _search != user_obj.id:
                response = JsonResponse({'error': "Este usuario ya existe."})
                response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                return response

        user_obj.username = _username
        user_obj.set_password(_password)
        user_obj.is_staff = is_staff
        user_obj.save()
        return JsonResponse({
            'success': True,
        }, status=HTTPStatus.OK)
