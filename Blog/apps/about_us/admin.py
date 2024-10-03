from django.contrib import admin

from apps.about_us.models import Nosotros

# Register your models here.
class NosotrosAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'edad']

admin.site.register(Nosotros, NosotrosAdmin)