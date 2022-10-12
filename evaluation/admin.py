from django.contrib import admin
from .models import *
# Register your models here.


class CompaniesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Stars)
admin.site.register(Companies, CompaniesAdmin)
admin.site.register(CompanySites)
admin.site.register(Sites)
admin.site.register(People)
admin.site.register(PeopleCompany)





