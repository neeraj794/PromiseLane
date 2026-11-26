from django.contrib import admin

from .models import BlockedUser, Interest, PartnerPreFerences, Report


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("sender__username", "receiver__username")


@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    list_display = ("blocker", "blocked", "created_at")
    list_filter = ("created_at",)
    search_fields = ("blocker__username", "blocked__username")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("reporter", "reported_user", "reason", "status", "created_at")
    list_filter = ("reason", "status", "created_at")
    search_fields = ("reporter__username", "reported_user__username", "description")


@admin.register(PartnerPreFerences)
class PartnerPreFerencesAdmin(admin.ModelAdmin):
    list_display = ("user", "min_age", "max_age", "preferred_gender", "religion", "marital_status", "city")
    list_filter = ("preferred_gender", "religion", "marital_status")
    search_fields = ("user__username", "city")
