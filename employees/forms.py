from django import forms
from .models import Employee


class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agar instance.user bo'lsa, full_name initial qiymatini to'ldiramiz
        if self.instance and getattr(self.instance, 'user', None):
            user = self.instance.user
            full_name = ''
            try:
                full_name = user.get_full_name() or ''
            except AttributeError:
                first = (getattr(user, 'first_name', '') or '').strip()
                last = (getattr(user, 'last_name', '') or '').strip()
                full_name = f"{first} {last}".strip()

            self.fields['full_name'].initial = full_name or getattr(user, 'username', '')