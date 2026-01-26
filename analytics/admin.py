from django.contrib import admin
from .models import FinancialPerformanceIndicator
from core.admin_mixins import PreserveFiltersAdminMixin, LocalizedAmountAdminMixin, format_amount


@admin.register(FinancialPerformanceIndicator)
class FinancialPerformanceIndicatorAdmin(LocalizedAmountAdminMixin, PreserveFiltersAdminMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'year',
        'month',
        'formatted_total_expenses',
        'formatted_rent',
        'formatted_electricity',
        'formatted_salaries'
    )
    list_filter = (
        'year',
        'month'
    )
    readonly_fields = ('total_expenses',)
    fieldsets = (
        ('Davr', {
            'fields': ('year', 'month')
        }),
        ('Xarajatlar', {
            'fields': (
                'rent',
                'electricity',
                'gas',
                'water',
                'salaries',
                'machine_equipment',
                'tools_equipment',
                'staff_food',
                'total_expenses'
            )
        }),
    )

    def formatted_total_expenses(self, obj):
        return format_amount(obj.total_expenses)
    formatted_total_expenses.short_description = 'Jami xarajatlar'

    def formatted_rent(self, obj):
        return format_amount(obj.rent)
    formatted_rent.short_description = 'Ijara'

    def formatted_electricity(self, obj):
        return format_amount(obj.electricity)
    formatted_electricity.short_description = 'Elektroenergiya'

    def formatted_salaries(self, obj):
        return format_amount(obj.salaries)
    formatted_salaries.short_description = 'Maoshlar'
