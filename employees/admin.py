from django.contrib import admin
from .models import Employee, Balance, BalanceStatistics


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'position',
        'salary_type',
        'base_salary',
        'user',
        'created_at'
    )
    list_filter = (
        'salary_type',
        'position',
        'created_at'
    )
    search_fields = (
        'full_name',
        'position',
        'user__username',
        'user__email'
    )
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('user', 'full_name', 'position')
        }),
        ('Maosh ma\'lumotlari', {
            'fields': ('salary_type', 'base_salary')
        }),
        ('Vaqt belgilari', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'employee',
        'date',
        'earned_amount',
        'paid_amount',
        'net_balance',
        'created_at'
    )
    list_filter = (
        'date',
        'employee',
        'created_at'
    )
    search_fields = (
        'employee__full_name',
        'employee__position',
        'description'
    )
    readonly_fields = ('created_at', 'net_balance')
    date_hierarchy = 'date'
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('employee', 'date')
        }),
        ('Summa ma\'lumotlari', {
            'fields': ('earned_amount', 'paid_amount', 'net_balance')
        }),
        ('Qo\'shimcha', {
            'fields': ('description',)
        }),
        ('Vaqt belgilari', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(BalanceStatistics)
class BalanceStatisticsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'employee',
        'year',
        'month',
        'total_earned',
        'total_paid',
        'net_balance',
        'is_closed'
    )
    list_filter = (
        'year',
        'month',
        'is_closed',
        'employee'
    )
    search_fields = (
        'employee__full_name',
        'employee__position'
    )
    readonly_fields = ('net_balance',)
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('employee', 'year', 'month')
        }),
        ('Statistika ma\'lumotlari', {
            'fields': ('total_earned', 'total_paid', 'net_balance')
        }),
        ('Holat', {
            'fields': ('is_closed',)
        }),
    )
