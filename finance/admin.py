from django.contrib import admin
from .models import IncomeExpense, IncomeExpenseStatistics
from core.admin_mixins import PreserveFiltersAdminMixin


@admin.register(IncomeExpense)
class IncomeExpenseAdmin(PreserveFiltersAdminMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'income_amount',
        'expense_amount',
        'get_net_profit',
        'created_by',
        'created_at'
    )
    list_filter = (
        'date',
        'created_by',
        'created_at'
    )
    search_fields = (
        'description',
        'created_by__username'
    )
    readonly_fields = ('created_at', 'net_profit')
    date_hierarchy = 'date'
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('created_by', 'date')
        }),
        ('Summa ma\'lumotlari', {
            'fields': ('income_amount', 'expense_amount', 'net_profit')
        }),
        ('Qo\'shimcha', {
            'fields': ('description',)
        }),
        ('Vaqt belgilari', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_net_profit(self, obj):
        return obj.net_profit
    get_net_profit.short_description = 'Foyda'


@admin.register(IncomeExpenseStatistics)
class IncomeExpenseStatisticsAdmin(PreserveFiltersAdminMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'year',
        'month',
        'total_income',
        'total_expense',
        'net_profit'
    )
    list_filter = (
        'year',
        'month'
    )
    readonly_fields = ('net_profit',)
    fieldsets = (
        ('Davr', {
            'fields': ('year', 'month')
        }),
        ('Statistika ma\'lumotlari', {
            'fields': ('total_income', 'total_expense', 'net_profit')
        }),
    )
