from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import User


def get_user_full_name(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'full_name': ''})
    try:
        user = User.objects.get(pk=user_id)
        full_name = ''
        try:
            full_name = user.get_full_name() or ''
        except AttributeError:
            first = (getattr(user, 'first_name', '') or '').strip()
            last = (getattr(user, 'last_name', '') or '').strip()
            full_name = f"{first} {last}".strip()
        return JsonResponse({'full_name': full_name or user.username})
    except User.DoesNotExist:
        return JsonResponse({'full_name': ''})
