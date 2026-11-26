from django.contrib import admin

from .models import MatrimonialProfile


@admin.register(MatrimonialProfile)
class MatrimonialProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "religion", "marital_status", "city", "state", "is_active")
    list_filter = ("religion", "marital_status", "is_active")
    search_fields = ("user__username", "user__first_name", "user__last_name", "city", "occupation")
