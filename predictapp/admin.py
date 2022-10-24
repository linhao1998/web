from django.contrib import admin

# Register your models here.
from predictapp import models
admin.site.register(models.Sequence)
admin.site.register(models.Information)