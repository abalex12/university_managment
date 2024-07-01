from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    model=User
    fieldsets = (
        (None, {'fields': ('user_id', 'email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'address', 'phone', 'gender', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'role'),
        }),
    )
    list_display = ('email', 'username', 'is_active', 'role')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

class TeacherAdmin(admin.ModelAdmin):
    model = Teacher

    def user_email(self, obj):
        return obj.user.email

    def user_username(self, obj):
        return obj.user.username

    list_display = ('user_email', 'user_username','department')

admin.site.register(Teacher, TeacherAdmin)

class StudentAdmin(admin.ModelAdmin):
    model = Student

    def user_email(self, obj):
        return obj.user.email
    
    def user_username(self, obj):
        return obj.user.username

    # def user_image(self,obj):
    #     return obj.user.profile_image

    list_display = ('user_email', 'user_username','section','department')

admin.site.register(Student,StudentAdmin)

class RoleAdmin(admin.ModelAdmin):
    model = Role
    fieldsets = (
        (None, {'fields': ('role_id', 'role_name')}),
    )
    list_display = ('role_id', 'role_name')
    search_fields = ('role_name',)
    ordering = ('role_name',)

admin.site.register(Role, RoleAdmin)