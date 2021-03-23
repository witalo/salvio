from django.contrib import admin

from .models import Business, Zone, Cultivation, State, Person, Variety, Phenology, Domain, Module, Lot

admin.site.register(Business)

admin.site.register(State)

admin.site.register(Person)

admin.site.register(Zone)

admin.site.register(Domain)

admin.site.register(Cultivation)

admin.site.register(Variety)

admin.site.register(Phenology)

admin.site.register(Module)

admin.site.register(Lot)
