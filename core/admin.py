from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ScrapCategory, PickupRequest

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'name', 'phone', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('name', 'phone', 'role', 'address')}),
    )

@admin.register(ScrapCategory)
class ScrapCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate_per_kg')
    search_fields = ('name',)

@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'scheduled_date', 'estimated_weight', 'total_amount', 'agent')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('customer__username', 'customer__phone', 'address')
    list_editable = ('status', 'agent')
    autocomplete_fields = ['agent']

    def save_model(self, request, obj, form, change):
        # Auto-update status when agent is assigned
        if obj.agent and obj.status == PickupRequest.Status.PENDING:
            obj.status = PickupRequest.Status.ASSIGNED
        super().save_model(request, obj, form, change)
