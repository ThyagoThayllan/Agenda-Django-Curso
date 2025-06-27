from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)

    list_display = ('id', 'first_name', 'email', 'phone', 'created_at',)

    ordering = ('-created_at',)

    search_fields = ('id', 'first_name', 'email', 'phone',)

    list_per_page = 25
