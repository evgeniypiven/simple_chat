"""
Authentication admin
"""

# Standard library imports.

# Related third party imports.
from django.contrib import admin

# Local application/library specific imports.
from .models import User


class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'username', 'email', 'is_staff', 'is_active'
            )
        }),
    )


admin.site.register(User, UserAdmin)
