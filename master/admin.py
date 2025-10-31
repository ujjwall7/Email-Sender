from django.contrib import admin
from . models import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'title', 'company']
    list_display_links = ['id', 'name', 'email', 'title', 'company']

admin.site.register(Credentials)