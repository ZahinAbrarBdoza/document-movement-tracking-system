from django.db.models import Q

from .models import Document


def user_role_flags(request):
    user = request.user

    if not user.is_authenticated:
        return {
            'global_can_edit': False,
            'global_can_view_reports': False,
            'global_can_bulk_forward': False,
            'global_can_bulk_close': False,
            'global_can_view_system_documents': False,
            'global_can_view_delegation_reports': False,
            'global_my_assigned_count': 0,
        }

    assigned_count = Document.objects.filter(
        Q(designated_person=user) |
        Q(delegations__is_active=True, delegations__delegated_recipient=user),
    ).exclude(status='closed').distinct().count()

    if user.is_superuser:
        return {
            'global_can_edit': True,
            'global_can_view_reports': True,
            'global_can_bulk_forward': True,
            'global_can_bulk_close': True,
            'global_can_view_system_documents': True,
            'global_can_view_delegation_reports': True,
            'global_my_assigned_count': assigned_count,
        }

    groups = set(user.groups.values_list('name', flat=True))
    can_view_system_documents = bool(groups.intersection({
        'Admin',
        'Receiving Desk',
        'HR',
        'ADT',
        'OPS',
        'Management',
    }))
    can_view_delegation_reports = bool(groups.intersection({
        'Admin',
        'Receiving Desk',
        'Management',
    }))
    can_bulk_close = (
        bool(groups.intersection({'Admin', 'Receiving Desk'})) or
        'Management' not in groups
    )

    return {
        'global_can_edit': bool(groups.intersection({'Admin', 'Receiving Desk', 'HR', 'ADT', 'OPS'})),
        'global_can_view_reports': bool(groups.intersection({'Admin', 'HR', 'ADT', 'OPS', 'Management'})),
        'global_can_bulk_forward': bool(groups.intersection({'Admin', 'Receiving Desk'})),
        'global_can_bulk_close': can_bulk_close,
        'global_can_view_system_documents': can_view_system_documents,
        'global_can_view_delegation_reports': can_view_delegation_reports,
        'global_my_assigned_count': assigned_count,
    }
