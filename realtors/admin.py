from django.contrib import admin
from .models import Realtor
# Register your models here.

class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id','is_mpv', 'name', 'email', 'hire_date' )
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    list_editable = ('is_mpv', )
    list_per_page = 10

admin.site.register(Realtor, RealtorAdmin)