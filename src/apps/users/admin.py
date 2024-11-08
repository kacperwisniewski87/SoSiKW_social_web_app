from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import SignUpMainForm, CustomUserChangeForm
from .models import CustomUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    verbose_name = 'User Profile Data'


class CustomUserAdmin(UserAdmin):
    add_form = SignUpMainForm
    form = CustomUserChangeForm
    model = CustomUser
    inlines = [UserProfileInline]
    list_display = ("email", "site_url", "first_name", "last_name", "gender", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'site_url')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', "is_superuser", 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", 'is_active',
                "is_staff", "is_superuser", "groups", "user_permissions"
            )
        }),
    )
    search_fields = ("email",)
    ordering = ("id",)

    def gender(self, obj):
        return obj.data.gender


admin.site.register(CustomUser, CustomUserAdmin)
