from django.contrib import admin

from .models import UserInventory, UserSubCollection, InventoryItem, GradingDetails


class UserInventoryAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)


class UserSubCollectionAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)


class InventoryItemAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)


class GradingDetailsAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)


admin.site.register(UserInventory, UserInventoryAdmin)
admin.site.register(UserSubCollection, UserSubCollectionAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(GradingDetails, GradingDetailsAdmin)
