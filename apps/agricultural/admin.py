from django.contrib import admin

from .models import Business, Zone, Fund, Cultivation, State, Person


class BusinessAdmin(admin.ModelAdmin):
    fields = ['ruc', 'business_name', 'address', 'phone',
              'legal_representative_name', 'legal_representative_dni']
    ordering = ('id',)


admin.site.register(Business, BusinessAdmin)

admin.site.register(Zone)

admin.site.register(Fund)

admin.site.register(Cultivation)

admin.site.register(State)

admin.site.register(Person)
