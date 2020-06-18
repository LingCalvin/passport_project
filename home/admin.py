from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Person, Address

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Address)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'first_name', 'last_name', 'cell_phone', 'email')


admin.site.register(Person, PersonAdmin)
