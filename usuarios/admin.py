from django.contrib import admin
from .models import User
from django.contrib.auth import admin as admin_auth
from .forms import UserCreateForm, UserChangeForm

@admin.register(User)
class UserAdmin(admin_auth.UserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm
    model = User

    fieldsets = admin_auth.UserAdmin.fieldsets + (
        ( 'Tipo', {"fields": ('tipo', )}),
    )
    


