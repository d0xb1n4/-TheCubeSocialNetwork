from django.contrib import admin
from .models import *


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'token', 'date_of_birth', 'date_of_creation')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Post)