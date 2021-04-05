from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust


class Person(models.Model):
    CHARGE_CHOICES = (('1', 'Administrador'), ('2', 'Trabajador'), ('3', 'Otro'))
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    document = models.CharField(max_length=15, null=True, blank=True)
    birth_date = models.DateField('Fecha de nacimiento', null=True, blank=True)
    telephone = models.CharField(max_length=9, null=True, blank=True)
    address = models.CharField('Direccion', max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='person/',
                              default='person/employee0.jpg', blank=True)
    photo_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(
        100, 100)], source='photo', format='JPEG', options={'quality': 90})
    charge = models.CharField('Cargo', max_length=1, choices=CHARGE_CHOICES, default='1', )
    create_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.document)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'


class Business(models.Model):
    id = models.AutoField(primary_key=True)
    ruc = models.CharField(max_length=11)
    business_name = models.CharField('Razón social', max_length=45, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=45, null=True, blank=True)
    legal_representative_name = models.CharField(max_length=100, null=True, blank=True)
    legal_representative_dni = models.CharField(max_length=45, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nombre estado', max_length=100, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)
    is_state = models.BooleanField('Estado', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'


class Cultivation(models.Model):
    id = models.AutoField(primary_key=True)
    abbreviation = models.CharField('Abreviatura', max_length=20, null=True, blank=True)
    name = models.CharField('Nombre cultivo', max_length=100, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)
    state = models.ForeignKey('State', verbose_name='Estado', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cultivo'
        verbose_name_plural = 'Cultivos'


class Domain(models.Model):
    id = models.AutoField(primary_key=True)
    abbreviation = models.CharField('Abreviatura', max_length=20, null=True, blank=True)
    name = models.CharField('Nombre fundo', max_length=100, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)
    zone = models.ForeignKey('Zone', verbose_name='Zona', on_delete=models.CASCADE, null=True, blank=True)
    business = models.ForeignKey('Business', verbose_name='Empresa', on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey('State', verbose_name='Estado', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fundo'
        verbose_name_plural = 'Fundos'


class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField('Codigo', max_length=20, null=True, blank=True)
    name = models.CharField('Nombre zona', max_length=100, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'


class Variety(models.Model):
    id = models.AutoField(primary_key=True)
    abbreviation = models.CharField('Abreviatura', max_length=20, null=True, blank=True)
    name = models.CharField('Nombre variedad', max_length=100, null=True, blank=True)
    cultivation = models.ForeignKey('Cultivation', on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey('State', on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Variadad'
        verbose_name_plural = 'Variedades'


class Phenology(models.Model):
    id = models.AutoField(primary_key=True)
    index = models.CharField('Indice', max_length=10, null=True, blank=True)
    name = models.CharField('Nombre fenologia', max_length=100, null=True, blank=True)
    cultivation = models.ForeignKey('Cultivation', on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey('State', on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fenologia'
        verbose_name_plural = 'Fenologias'


class Module(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nombre modulo', max_length=100, null=True, blank=True)
    domain = models.ForeignKey('Domain', verbose_name='Fundo', on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey('State', verbose_name='Estado', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'


class Lot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nombre lote', max_length=100, null=True, blank=True)
    module = models.ForeignKey('Module', verbose_name='Modulo', on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField('Latitud', max_digits=30, decimal_places=6, default=0)
    longitude = models.DecimalField('Longitud', max_digits=30, decimal_places=6, default=0)
    state = models.ForeignKey('State', verbose_name='Estado', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
