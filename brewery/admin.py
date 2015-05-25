from django.contrib import admin

from brewery.models import BrewSettings
from brewery.models import Temperature
from brewery.models import State

admin.site.register(BrewSettings)
admin.site.register(Temperature)
admin.site.register(State)
