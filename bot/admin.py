from django.contrib import admin
from django.utils.html import format_html
from .models import (
    BotUser, BotAdmin, BotSetting, Service, ServicePackage,
    PortfolioItem, WebsiteItem, FAQ, Order
)


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'full_name', 'username', 'phone', 'first_seen', 'last_active', 'is_active')
    list_filter = ('is_active', 'language')
    search_fields = ('first_name', 'username', 'telegram_id')
    readonly_fields = ('telegram_id', 'first_seen', 'last_active')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    full_name.short_description = 'Ism'


@admin.register(BotAdmin)
class BotAdminAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('user__first_name', 'user__username')

    def user_name(self, obj):
        return obj.user.first_name
    user_name.short_description = 'Admin'


@admin.register(BotSetting)
class BotSettingAdmin(admin.ModelAdmin):
    list_display = ('bot_name', 'phone', 'telegram_username', 'is_bot_active')

    def has_add_permission(self, request):
        if BotSetting.objects.exists():
            return False
        return super().has_add_permission(request)


class ServicePackageInline(admin.TabularInline):
    model = ServicePackage
    extra = 1
    fields = ('name', 'price', 'features', 'order')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'price_info', 'is_active', 'order')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    inlines = [ServicePackageInline]


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('service', 'name', 'price', 'order')
    list_editable = ('order',)
    list_filter = ('service',)


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'is_active', 'order')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title',)


@admin.register(WebsiteItem)
class WebsiteItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'url', 'is_active', 'order')
    list_editable = ('order', 'is_active')
    search_fields = ('name',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'status', 'phone', 'budget', 'created_at')
    list_filter = ('status', 'service')
    search_fields = ('name', 'phone', 'service')
    readonly_fields = ('user', 'created_at', 'updated_at')
    fieldsets = (
        ('Mijoz ma\'lumotlari', {
            'fields': ('user', 'name', 'phone', 'business_type')
        }),
        ('Buyurtma', {
            'fields': ('service', 'description', 'budget', 'comment')
        }),
        ('Boshqarish', {
            'fields': ('status', 'assigned_admin', 'internal_note')
        }),
        ('Sana', {
            'fields': ('created_at', 'updated_at')
        }),
    )
