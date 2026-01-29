from django.contrib import admin

# Apps order list
APP_ORDER = ['accounts', 'employees', 'finance', 'analytics']

# Models order list
MODEL_ORDERS = {
    'accounts': ['User'],
    'employees': ['Employee', 'Balance', 'MonthBalanceStatistics', 'YearlyBalanceStatistics'],
    'finance': ['IncomeExpense', 'IncomeExpenseStatistics'],
    'analytics': ['FinancialPerformanceIndicator']
}

# Save original method
original_get_app_list = admin.AdminSite.get_app_list

def custom_get_app_list(self, request, app_label=None):
    try:
        app_list = original_get_app_list(self, request, app_label)
        
        # Debug: Print current apps
        print("DEBUG: Current apps:", [app['app_label'] for app in app_list])
        
        # Sort apps
        app_list.sort(key=lambda app: APP_ORDER.index(app['app_label'])
                      if app['app_label'] in APP_ORDER
                      else 999)
        
        # Sort models within each app
        for app in app_list:
            app_label = app['app_label']
            if app_label in MODEL_ORDERS and MODEL_ORDERS[app_label]:
                model_order = MODEL_ORDERS[app_label]
                # Debug: Print current models for this app
                print(f"DEBUG: Models in {app_label}:", [model['object_name'] for model in app['models']])
                app['models'].sort(
                    key=lambda model: model_order.index(model['object_name'])
                    if model['object_name'] in model_order
                    else 999
                )
        
        return app_list
    except Exception as e:
        print(f"ERROR in custom_get_app_list: {e}")
        import traceback
        traceback.print_exc()
        # Return default app list if error
        return original_get_app_list(self, request, app_label)

# Override admin site
admin.AdminSite.get_app_list = custom_get_app_list
