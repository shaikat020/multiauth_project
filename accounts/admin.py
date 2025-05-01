from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'role', 'id_number', 'is_admin')
    list_filter = ('is_admin', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role', 'id_number', 'level', 'term', 'contact_information')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'id_number', 'level', 'term', 
                      'contact_information', 'password1', 'password2', 'is_active'),
        }),
    )
    search_fields = ('email', 'name', 'id_number')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)