from django.contrib import admin
from contact.models import Category
from contact.models import Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    ordering = ('id',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'email',
        'phone',
        'category',
        'created_at',
    )

    list_filter = (
        'category',
        'created_at',
    )

    list_per_page = 25

    ordering = ('-created_at',)

    search_fields = (
        'id',
        'first_name',
        'email',
        'phone',
    )
