from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import path
from .models import Employee, Salary

User = get_user_model()


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ("full_name", "user", "phone_number", "position", "salary_type", "f_base_salary", "created_at")
	list_filter = ()
	search_fields = ()

	def f_base_salary(self, obj):
		return "{:,}".format(obj.base_salary).replace(',', ' ')
	f_base_salary.short_description = 'Base Salary (uzs)'

	class Media:
		js = ("admin/js/user_autofill.js",)

	def clean_user(self, form_data):
		"""Validate that user is not already assigned to another employee."""
		cleaned_data = form_data
		if 'user' in cleaned_data:
			user = cleaned_data['user']
			if user and Employee.objects.filter(user=user).exclude(id=self.instance.id if self.instance else None).exists():
				raise admin.ValidationError("Bu foydalanuvchi allaqachon xodim sifatida belgilangan.")
		return cleaned_data

	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path('get-user-details/<uuid:user_id>/', self.admin_site.admin_view(self.get_user_details), name='employee_get_user_details'),
		]
		return custom_urls + urls

	def save_model(self, request, obj, form, change):
		"""Validate before saving that this user isn't already assigned."""
		if obj.user and Employee.objects.filter(user=obj.user).exclude(id=obj.id).exists():
			from django.core.exceptions import ValidationError
			raise ValidationError("Bu foydalanuvchi allaqachon xodim sifatida belgilangan.")
		super().save_model(request, obj, form, change)

	def get_user_details(self, request, user_id):
		try:
			user = User.objects.get(pk=user_id)
			full_name = f"{user.first_name} {user.last_name}".strip() or user.username
			phone = getattr(user, 'phone_number', '') or ''
			return JsonResponse({
				'full_name': full_name,
				'phone_number': phone
			})
		except User.DoesNotExist:
			return JsonResponse({'error': 'User not found'}, status=404)

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
	list_display = ("employee", "date", "f_earned_amount", "earned_note", "f_paid_amount", "paid_note", "created_at")
	list_filter = ()
	search_fields = ()

	def f_paid_amount(self, obj):
		return "{:,}".format(obj.paid_amount).replace(',', ' ')
	f_paid_amount.short_description = 'Paid (uzs)'

	def f_earned_amount(self, obj):
		return "{:,}".format(obj.earned_amount).replace(',', ' ')
	f_earned_amount.short_description = 'Earned (uzs)'
