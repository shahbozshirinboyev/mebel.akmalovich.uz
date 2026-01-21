from django.contrib import admin
from django.http import HttpResponseRedirect

class PreserveFiltersAdminMixin:
    """
    Admin mixin that preserves filter states in session storage.
    """
    def changelist_view(self, request, extra_context=None):
        # Create a unique session key for this model's filters
        session_key = f'admin_filters_{request.resolver_match.url_name}'
        
        # If no GET parameters but we have saved filters, restore them
        if not request.GET and session_key in request.session:
            saved_filters = request.session[session_key]
            if saved_filters:
                request.GET = request.GET.copy()
                request.GET.update(saved_filters)
                # Redirect to apply the filters
                return HttpResponseRedirect(request.path + '?' + request.GET.urlencode())
        
        # Save current filters to session if any exist
        if request.GET:
            # Get all filter parameters (including related lookups)
            filter_keys = set()
            for filter_item in self.get_list_filter(request):
                if hasattr(filter_item, 'parameter_name'):
                    filter_keys.add(filter_item.parameter_name)
                else:
                    filter_keys.add(str(filter_item))
            
            # Also include any custom preserved filters
            filter_keys.update(getattr(self, 'preserved_filters', set()))
            
            if filter_keys:
                request.session[session_key] = {
                    k: v for k, v in request.GET.items() 
                    if any(k == fk or k.startswith(f"{fk}__") for fk in filter_keys)
                    or k in ('q',)  # Preserve search
                }
                request.session.modified = True
        
        return super().changelist_view(request, extra_context=extra_context)
