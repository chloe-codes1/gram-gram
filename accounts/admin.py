from django.contrib import admin
from django.contrib.auth import get_user_model
# Register your models here.

User = get_user_model()
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'first_name', 'last_name', 'email', 'is_superuser', 'last_login', 'date_joined',)

admin.site.register(User, UserAdmin)