from django.contrib import admin
from .models import EmailVerificationToken

@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "created_at"]
    readonly_fields = ["token", "created_at"]
