from django.contrib import admin
from api.models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "size", "type", "url")


admin.site.register(Item, ItemAdmin)
