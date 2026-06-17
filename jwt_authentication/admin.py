from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmailVerificationToken, User

@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "created_at"]
    readonly_fields = ["token", "created_at"]

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "role", "is_verified", "is_staff",)
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields",
         {
             "fields":(
                 "role",
                 "is_verified",
                 )
                 },
                 ),
)