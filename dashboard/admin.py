from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from dashboard.models import User,Course,BookedCourse
admin.site.register(BookedCourse)
admin.site.register(Course)
@admin.register(User)

class UserAdmin(UserAdmin):
    model = User
    # ✅ Columns in the list view
    list_display = ('username', 'email', 'role')
    list_filter = ('role', 'gender')

    # ✅ Add custom fields to the form layout   
    fieldsets = UserAdmin.fieldsets + (
        ('Student Info', {
            'fields': (
                'phone',
                'gender',
                'dob',
                'profile_picture',
                'role',
            )
        }),
    )

    # ✅ Fields shown while creating a new user (superuser too)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Student Info', {
            'fields': (
                'phone',
                'gender',
                'dob',
                'profile_picture',
                'role',
            )
        }),
    )

