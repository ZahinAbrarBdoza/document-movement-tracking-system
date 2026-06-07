def user_role_flags(request):
    user = request.user

    if not user.is_authenticated:
        return {
            'global_can_edit': False,
            'global_can_view_reports': False,
        }

    if user.is_superuser:
        return {
            'global_can_edit': True,
            'global_can_view_reports': True,
        }

    groups = user.groups.values_list('name', flat=True)

    return {
        'global_can_edit': any(group in groups for group in ['Admin', 'HR', 'ADT', 'OPS']),
        'global_can_view_reports': any(group in groups for group in ['Admin', 'HR', 'ADT', 'OPS', 'Management']),
    }