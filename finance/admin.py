from django.contrib import admin
from .models import IncomeExpense, IncomeExpenseStatistics
from core.admin_mixins import PreserveFiltersAdminMixin, LocalizedAmountAdminMixin, format_amount


@admin.register(IncomeExpense)
class IncomeExpenseAdmin(LocalizedAmountAdminMixin, PreserveFiltersAdminMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'formatted_income_amount',
        'formatted_expense_amount',
        'formatted_net_profit',
        'created_by',
        'created_at'
    )

    def formatted_income_amount(self, obj):
        return format_amount(obj.income_amount)
    formatted_income_amount.short_description = 'Kirim summasi'

    def formatted_expense_amount(self, obj):
        return format_amount(obj.expense_amount)
    formatted_expense_amount.short_description = 'Chiqim summasi'

    def formatted_net_profit(self, obj):
        return format_amount(obj.net_profit)
    formatted_net_profit.short_description = 'Foyda'
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
class IncomeExpenseStatisticsAdmin(LocalizedAmountAdminMixin, PreserveFiltersAdminMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'year',
        'month',
        'formatted_total_income',
        'formatted_total_expense',
        'formatted_net_profit'
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

    def formatted_total_income(self, obj):
        return format_amount(obj.total_income)
    formatted_total_income.short_description = 'Jami kirim'

    def formatted_total_expense(self, obj):
        return format_amount(obj.total_expense)
    formatted_total_expense.short_description = 'Jami chiqim'

    def formatted_net_profit(self, obj):
        return format_amount(obj.net_profit)
    formatted_net_profit.short_description = 'Foyda'
