from django.contrib import admin
from .models import Department, Zone, UserProfile, Document, DocumentMovement


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'designation', 'phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'designation', 'phone')
    list_filter = ('role', 'department')


class DocumentMovementInline(admin.TabularInline):
    model = DocumentMovement
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'tracking_id',
        'entry_type',
        'subject',
        'source_zone',
        'source_department',
        'destination_department',
        'current_department',
        'status',
        'priority',
        'aging_days',
        'created_at',
    )
    search_fields = (
        'tracking_id',
        'subject',
        'remarks',
    )
    list_filter = (
        'entry_type',
        'status',
        'priority',
        'source_zone',
        'source_department',
        'destination_department',
        'current_department',
        'created_at',
    )
    readonly_fields = (
        'tracking_id',
        'created_at',
        'updated_at',
        'closed_at',
    )
    inlines = [DocumentMovementInline]


@admin.register(DocumentMovement)
class DocumentMovementAdmin(admin.ModelAdmin):
    list_display = (
        'document',
        'action',
        'from_department',
        'to_department',
        'performed_by',
        'created_at',
    )
    search_fields = (
        'document__tracking_id',
        'document__subject',
        'remarks',
    )
    list_filter = (
        'action',
        'from_department',
        'to_department',
        'created_at',
    )