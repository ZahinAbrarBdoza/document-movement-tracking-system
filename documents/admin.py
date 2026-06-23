from django.contrib import admin
from .models import (
    Area,
    Branch,
    CourierRate,
    Department,
    Division,
    Document,
    DocumentDelegation,
    DocumentMovement,
    Region,
    UserDelegationRule,
    UserProfile,
    Zone,
)


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


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'division', 'code', 'is_active')
    search_fields = ('name', 'code', 'division__name', 'division__code')
    list_filter = ('is_active', 'division')


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'division_name', 'code', 'is_active')
    search_fields = (
        'name',
        'code',
        'region__name',
        'region__code',
        'region__division__name',
    )
    list_filter = ('is_active', 'region__division', 'region')

    @admin.display(description='Division')
    def division_name(self, obj):
        return obj.region.division


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'region_name', 'division_name', 'code', 'is_active')
    search_fields = (
        'name',
        'code',
        'area__name',
        'area__region__name',
        'area__region__division__name',
    )
    list_filter = ('is_active', 'area__region__division', 'area__region', 'area')

    @admin.display(description='Region')
    def region_name(self, obj):
        return obj.area.region

    @admin.display(description='Division')
    def division_name(self, obj):
        return obj.area.region.division

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'role', 'department', 'designation', 'phone')
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'designation',
        'phone',
    )
    list_filter = ('role', 'department')

    @admin.display(description='Email')
    def user_email(self, obj):
        return obj.user.email


@admin.register(CourierRate)
class CourierRateAdmin(admin.ModelAdmin):
    list_display = ('description', 'quantity', 'amount', 'is_active')
    search_fields = ('description', 'quantity', 'remarks')
    list_filter = ('is_active',)


class DocumentMovementInline(admin.TabularInline):
    model = DocumentMovement
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'tracking_id',
        'reference_no',
        'entry_type',
        'subject',
        'courier_rate',
        'outward_amount',
        'designated_person',
        'first_boss',
        'source_zone',
        'source_division',
        'source_region',
        'source_area',
        'source_branch',
        'source_department',
        'destination_department',
        'current_department',
        'status',
        'priority',
        'notification_required',
        'notification_sent',
        'aging_days',
        'created_at',
    )
    search_fields = (
        'tracking_id',
        'reference_no',
        'subject',
        'addressed_to_name',
        'addressed_to_designation',
        'designated_person__username',
        'designated_person__email',
        'first_boss__username',
        'first_boss__email',
        'source_type',
        'external_organization_type',
        'external_organization_name',
        'external_branch_name',
        'source_division__name',
        'source_division__code',
        'source_region__name',
        'source_region__code',
        'source_area__name',
        'source_area__code',
        'source_branch__name',
        'source_branch__code',
        'outward_description',
        'outward_quantity',
        'courier_rate__description',
        'courier_rate__quantity',
        'remarks',
    )
    list_filter = (
        'entry_type',
        'status',
        'priority',
        'courier_rate',
        'outward_is_manual',
        'source_type',
        'external_organization_type',
        'notification_required',
        'notification_sent',
        'designated_person',
        'first_boss',
        'source_zone',
        'source_division',
        'source_region',
        'source_area',
        'source_branch',
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
        'notification_sent_at',
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


@admin.register(DocumentDelegation)
class DocumentDelegationAdmin(admin.ModelAdmin):
    list_display = (
        'document',
        'original_recipient',
        'delegated_recipient',
        'delegated_by',
        'delegated_at',
        'is_active',
    )
    search_fields = (
        'document__tracking_id',
        'document__subject',
        'original_recipient__username',
        'delegated_recipient__username',
        'reason',
    )
    list_filter = ('is_active', 'delegated_at')
    readonly_fields = ('delegated_at',)


@admin.register(UserDelegationRule)
class UserDelegationRuleAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'backup_receiver',
        'start_date',
        'end_date',
        'created_by',
        'is_active',
    )
    search_fields = (
        'user__username',
        'backup_receiver__username',
        'reason',
    )
    list_filter = ('is_active', 'start_date', 'end_date')
    readonly_fields = ('created_at',)
