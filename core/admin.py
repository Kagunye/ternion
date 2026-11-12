from django.contrib import admin

from .models import QuoteRequest


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "phone", "service", "origin", "destination", "movement_date", "created_at", "handled")
    list_filter = ("service", "handled")
    list_editable = ("handled",)
    search_fields = ("name", "company", "phone", "email", "origin", "destination", "cargo_type")
