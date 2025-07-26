from django.contrib import admin
from .models import EmailVerificationCode


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'created_at', 'expires_at', 'is_used')
    search_fields = ('email',)
    list_filter = ('is_used', 'created_at')
    readonly_fields = ('created_at',)
