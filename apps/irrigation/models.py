from django.contrib.auth.models import User
from django.db import models
from apps.agricultural.models import Cultivation, Zone, Domain, State


# Create your models here.
class Method(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nombre metodo', max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuario registro', on_delete=models.SET_NULL, null=True,
                             blank=True)
    create_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Metodo'
        verbose_name_plural = 'Metodos'


class IrrigationGroup(models.Model):
    id = models.AutoField(primary_key=True)
    subgroup = models.CharField('Subgrupo', max_length=200, null=True, blank=True)
    departure_rc = models.CharField('Partida RC', max_length=200, null=True, blank=True)
    family = models.CharField('Nombre familia', max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.subgroup)

    class Meta:
        verbose_name = 'Metodo'
        verbose_name_plural = 'Metodos'


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    zone = models.ForeignKey(Zone, verbose_name='Zona', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Nombre equipo', max_length=200, null=True, blank=True)
    description = models.CharField('Descripcion', max_length=200, null=True, blank=True)
    reservoir = models.CharField('Reservorio', max_length=200, null=True, blank=True)
    correction_factor = models.IntegerField('Factor Correccion', null=True, blank=True)
    state = models.ForeignKey(State, verbose_name='Estado', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'


class NutritionLaw(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField('Codigo', max_length=20, null=True, blank=True)
    irrigation_group = models.ForeignKey('IrrigationGroup', verbose_name='Grupo riego', on_delete=models.CASCADE,
                                         null=True, blank=True)
    name = models.CharField('Nombre', max_length=200, null=True, blank=True)
    um = models.CharField('UM', max_length=200, null=True, blank=True)
    n = models.DecimalField('N', max_digits=20, decimal_places=2, default=0)
    p2o5 = models.DecimalField('P2O5', max_digits=20, decimal_places=2, default=0)
    k2o = models.DecimalField('K2O', max_digits=20, decimal_places=2, default=0)
    cao = models.DecimalField('CAO', max_digits=20, decimal_places=2, default=0)
    mgo = models.DecimalField('MGO', max_digits=20, decimal_places=2, default=0)
    s = models.DecimalField('S', max_digits=20, decimal_places=2, default=0)
    fe = models.DecimalField('FE', max_digits=20, decimal_places=2, default=0)
    mn = models.DecimalField('MN', max_digits=20, decimal_places=2, default=0)
    b = models.DecimalField('B', max_digits=20, decimal_places=2, default=0)
    zn = models.DecimalField('ZN', max_digits=20, decimal_places=2, default=0)
    mo = models.DecimalField('MO', max_digits=20, decimal_places=2, default=0)
    ci = models.DecimalField('CI', max_digits=20, decimal_places=2, default=0)
    cu = models.DecimalField('CU', max_digits=20, decimal_places=2, default=0)
    h2o = models.DecimalField('H2O', max_digits=20, decimal_places=2, default=0)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Ley nutricion riego'
        verbose_name_plural = 'Ley nutricion riegos'


class Operator(models.Model):
    id = models.AutoField(primary_key=True)
    zone = models.ForeignKey(Zone, verbose_name='Zona', on_delete=models.CASCADE, null=True, blank=True)
    code_sap = models.CharField('Codigo SAP', max_length=20, null=True, blank=True)
    document = models.CharField('Documento', max_length=15, null=True, blank=True)
    description = models.CharField('Descripcion', max_length=200, null=True, blank=True)
    function = models.CharField('Funcion', max_length=100, null=True, blank=True)
    state = models.ForeignKey(State, verbose_name='Estado', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.description)

    class Meta:
        verbose_name = 'Operador'
        verbose_name_plural = 'Operadores'


class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField('Numero reserva', max_length=20, null=True, blank=True)
    date = models.DateField('Fecha', null=True, blank=True)
    cultivation = models.ForeignKey(Cultivation, on_delete=models.CASCADE, null=True, blank=True)
    domain = models.ForeignKey(Domain, verbose_name='Fundo', on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(Zone, verbose_name='Zona', on_delete=models.CASCADE, null=True, blank=True)
    method = models.ForeignKey('Method', verbose_name='Metodo', on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey('Team', verbose_name='Equipo', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Regisros'
