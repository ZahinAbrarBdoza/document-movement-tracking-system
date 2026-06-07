from urllib import request

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

import documents

from .forms import DocumentForm, DocumentMovementForm
from .models import Department, Document, DocumentMovement, Zone


def user_in_groups(user, group_names):
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=group_names).exists()


def can_edit_documents(user):
    return user_in_groups(user, ['Admin', 'HR', 'ADT', 'OPS'])


def can_view_reports(user):
    return user_in_groups(user, ['Admin', 'HR', 'ADT', 'OPS', 'Management'])

def permission_denied_page(request, message='You do not have permission to perform this action.'):
    return render(
        request,
        'documents/permission_denied.html',
        {'message': message},
        status=403
    )

def filter_documents_from_request(request, base_queryset=None):
    if base_queryset is None:
        documents = Document.objects.select_related(
            'source_zone',
            'source_department',
            'destination_department',
            'current_department',
            'created_by',
        ).order_by('-created_at')
    else:
        documents = base_queryset

    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    priority = request.GET.get('priority', '').strip()
    department_id = request.GET.get('department', '').strip()
    zone_id = request.GET.get('zone', '').strip()
    entry_type = request.GET.get('entry_type', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    if query:
        documents = documents.filter(
            Q(tracking_id__icontains=query) |
            Q(subject__icontains=query) |
            Q(document_type__icontains=query) |
            Q(remarks__icontains=query) |
            Q(source_zone__name__icontains=query) |
            Q(source_zone__code__icontains=query) |
            Q(source_department__name__icontains=query) |
            Q(source_department__code__icontains=query) |
            Q(destination_department__name__icontains=query) |
            Q(destination_department__code__icontains=query) |
            Q(current_department__name__icontains=query) |
            Q(current_department__code__icontains=query)
        )

    if status:
        documents = documents.filter(status=status)

    if priority:
        documents = documents.filter(priority=priority)

    if department_id:
        documents = documents.filter(
            Q(source_department_id=department_id) |
            Q(destination_department_id=department_id) |
            Q(current_department_id=department_id)
        )

    if zone_id:
        documents = documents.filter(source_zone_id=zone_id)

    if entry_type:
        documents = documents.filter(entry_type=entry_type)

    if date_from:
        documents = documents.filter(created_at__date__gte=date_from)

    if date_to:
        documents = documents.filter(created_at__date__lte=date_to)

    return documents

@login_required
def dashboard(request):
    total_documents = Document.objects.count()
    pending_documents = Document.objects.exclude(status='closed').count()
    closed_documents = Document.objects.filter(status='closed').count()
    urgent_documents = Document.objects.filter(priority='urgent').exclude(status='closed').count()

    recent_documents = Document.objects.select_related(
        'source_zone',
        'source_department',
        'destination_department',
        'current_department',
    ).order_by('-created_at')[:8]
    user_department = None
    my_department_pending = None

    if hasattr(request.user, 'profile') and request.user.profile.department:
        user_department = request.user.profile.department
        my_department_pending = Document.objects.filter(
            current_department=user_department
        ).exclude(status='closed').count()

    context = {
        'total_documents': total_documents,
        'pending_documents': pending_documents,
        'closed_documents': closed_documents,
        'urgent_documents': urgent_documents,
        'recent_documents': recent_documents,
        'can_edit': can_edit_documents(request.user),
        'user_department': user_department,
        'my_department_pending': my_department_pending,
    }
    return render(request, 'documents/dashboard.html', context)


@login_required
def document_list(request):
    documents = filter_documents_from_request(request)

    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    priority = request.GET.get('priority', '').strip()
    department_id = request.GET.get('department', '').strip()
    zone_id = request.GET.get('zone', '').strip()
    entry_type = request.GET.get('entry_type', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    departments = Department.objects.filter(is_active=True).order_by('name')
    zones = Zone.objects.filter(is_active=True).order_by('name')

    context = {
        'documents': documents,
        'departments': departments,
        'zones': zones,
        'query': query,
        'selected_status': status,
        'selected_priority': priority,
        'selected_department': department_id,
        'selected_zone': zone_id,
        'selected_entry_type': entry_type,
        'selected_date_from': date_from,
        'selected_date_to': date_to,
        'status_choices': Document.STATUS_CHOICES,
        'priority_choices': Document.PRIORITY_CHOICES,
        'entry_type_choices': Document.ENTRY_TYPE_CHOICES,
        'total_found': documents.count(),
        'can_edit': can_edit_documents(request.user),
    }
    return render(request, 'documents/document_list.html', context)

@login_required
def pending_documents(request):
    base_queryset = Document.objects.select_related(
        'source_zone',
        'source_department',
        'destination_department',
        'current_department',
        'created_by',
    ).exclude(status='closed').order_by('created_at')

    documents = filter_documents_from_request(request, base_queryset)

    query = request.GET.get('q', '').strip()
    department_id = request.GET.get('department', '').strip()
    zone_id = request.GET.get('zone', '').strip()
    priority = request.GET.get('priority', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    if query:
        documents = documents.filter(
            Q(tracking_id__icontains=query) |
            Q(subject__icontains=query) |
            Q(document_type__icontains=query) |
            Q(remarks__icontains=query) |
            Q(source_zone__name__icontains=query) |
            Q(source_zone__code__icontains=query) |
            Q(source_department__name__icontains=query) |
            Q(source_department__code__icontains=query) |
            Q(destination_department__name__icontains=query) |
            Q(destination_department__code__icontains=query) |
            Q(current_department__name__icontains=query) |
            Q(current_department__code__icontains=query)
        )

    if department_id:
        documents = documents.filter(
            Q(source_department_id=department_id) |
            Q(destination_department_id=department_id) |
            Q(current_department_id=department_id)
        )

    if zone_id:
        documents = documents.filter(source_zone_id=zone_id)

    if priority:
        documents = documents.filter(priority=priority)

    departments = Department.objects.filter(is_active=True).order_by('name')
    zones = Zone.objects.filter(is_active=True).order_by('name')

    context = {
        'documents': documents,
        'departments': departments,
        'zones': zones,
        'query': query,
        'selected_department': department_id,
        'selected_zone': zone_id,
        'selected_priority': priority,
        'selected_date_from': date_from,
        'selected_date_to': date_to,
        'priority_choices': Document.PRIORITY_CHOICES,
        'total_found': documents.count(),
        'can_edit': can_edit_documents(request.user),
    }
    return render(request, 'documents/pending_documents.html', context)

@login_required
def document_create(request):
    if not can_edit_documents(request.user):
        return permission_denied_page(request, 'You do not have permission to create documents.')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.created_by = request.user
            document.save()

            DocumentMovement.objects.create(
                document=document,
                action='created',
                from_department=None,
                to_department=document.current_department,
                performed_by=request.user,
                remarks='Initial document entry created.'
            )

            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentForm()

    context = {
        'form': form,
    }
    return render(request, 'documents/document_form.html', context)

@login_required
def document_edit(request, pk):
    if not can_edit_documents(request.user):
        return permission_denied_page(request, 'You do not have permission to edit documents.')

    document = get_object_or_404(Document, pk=pk)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)

        if form.is_valid():
            form.save()

            DocumentMovement.objects.create(
                document=document,
                action='status_updated',
                from_department=document.current_department,
                to_department=document.current_department,
                performed_by=request.user,
                remarks='Document information edited.'
            )

            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentForm(instance=document)

    context = {
        'form': form,
        'document': document,
        'is_edit': True,
    }
    return render(request, 'documents/document_form.html', context)


@login_required
def document_detail(request, pk):
    document = get_object_or_404(
        Document.objects.select_related(
            'source_zone',
            'source_department',
            'destination_department',
            'current_department',
            'created_by',
        ),
        pk=pk
    )

    movements = document.movements.select_related(
        'from_department',
        'to_department',
        'performed_by',
    ).all()

    context = {
        'document': document,
        'movements': movements,
        'can_edit': can_edit_documents(request.user),
    }
    return render(request, 'documents/document_detail.html', context)


@login_required
def document_update_movement(request, pk):
    if not can_edit_documents(request.user):
        return permission_denied_page(request, 'You do not have permission to update or forward documents.')

    document = get_object_or_404(
        Document.objects.select_related(
            'current_department',
            'destination_department',
        ),
        pk=pk
    )

    if request.method == 'POST':
        form = DocumentMovementForm(request.POST)

        if form.is_valid():
            movement = form.save(commit=False)
            movement.document = document
            movement.from_department = document.current_department
            movement.performed_by = request.user
            movement.save()

            new_status = form.cleaned_data['new_status']
            to_department = form.cleaned_data.get('to_department')

            document.status = new_status

            if to_department:
                document.current_department = to_department

            if movement.action == 'forwarded' and to_department:
                document.destination_department = to_department

            document.save()

            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentMovementForm(initial={
            'new_status': document.status,
            'to_department': document.current_department,
        })

    context = {
        'document': document,
        'form': form,
    }
    return render(request, 'documents/document_movement_form.html', context)


@login_required
def reports_dashboard(request):
    if not can_view_reports(request.user):
        return permission_denied_page(request, 'You do not have permission to view reports.')

    today = timezone.now().date()

    total_documents = Document.objects.count()
    pending_documents = Document.objects.exclude(status='closed').count()
    closed_documents = Document.objects.filter(status='closed').count()
    urgent_pending = Document.objects.filter(priority='urgent').exclude(status='closed').count()

    received_today = Document.objects.filter(received_date=today).count()
    sent_today = Document.objects.filter(sent_date=today).count()

    department_pending = Department.objects.filter(is_active=True).annotate(
        pending_count=Count(
            'current_documents',
            filter=~Q(current_documents__status='closed')
        )
    ).order_by('-pending_count', 'name')

    zone_documents = Zone.objects.filter(is_active=True).annotate(
        document_count=Count('source_documents')
    ).order_by('-document_count', 'name')

    aging_documents = Document.objects.select_related(
        'source_zone',
        'source_department',
        'destination_department',
        'current_department',
    ).exclude(status='closed').order_by('created_at')[:10]

    recent_closed_documents = Document.objects.select_related(
        'source_zone',
        'source_department',
        'destination_department',
        'current_department',
    ).filter(status='closed').order_by('-closed_at')[:10]

    raw_status_summary = Document.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')

    status_labels = dict(Document.STATUS_CHOICES)

    status_summary = [
        {
            'label': status_labels.get(item['status'], item['status']),
            'count': item['count'],
        }
        for item in raw_status_summary
    ]

    raw_entry_type_summary = Document.objects.values('entry_type').annotate(
        count=Count('id')
    ).order_by('entry_type')

    entry_type_labels = dict(Document.ENTRY_TYPE_CHOICES)

    entry_type_summary = [
        {
            'label': entry_type_labels.get(item['entry_type'], item['entry_type']),
            'count': item['count'],
        }
        for item in raw_entry_type_summary
    ]

    context = {
        'total_documents': total_documents,
        'pending_documents': pending_documents,
        'closed_documents': closed_documents,
        'urgent_pending': urgent_pending,
        'received_today': received_today,
        'sent_today': sent_today,
        'department_pending': department_pending,
        'zone_documents': zone_documents,
        'aging_documents': aging_documents,
        'recent_closed_documents': recent_closed_documents,
        'status_summary': status_summary,
        'entry_type_summary': entry_type_summary,
    }

    return render(request, 'documents/reports_dashboard.html', context)


@login_required
def export_documents_excel(request):
    if not can_view_reports(request.user):
        return permission_denied_page(request, 'You do not have permission to export documents.')

    export_type = request.GET.get('type', '').strip()

    if export_type == 'pending':
        base_queryset = Document.objects.select_related(
            'source_zone',
            'source_department',
            'destination_department',
            'current_department',
            'created_by',
        ).exclude(status='closed').order_by('created_at')

        documents = filter_documents_from_request(request, base_queryset)
    else:
        documents = filter_documents_from_request(request)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Documents'

    headers = [
        'Tracking ID',
        'Entry Type',
        'Document Type',
        'Subject',
        'Source Zone',
        'Source Department',
        'Destination Department',
        'Current Department',
        'Status',
        'Priority',
        'Received Date',
        'Sent Date',
        'Aging Days',
        'Remarks',
        'Created By',
        'Created At',
    ]

    sheet.append(headers)

    header_fill = PatternFill(start_color='0F6B45', end_color='0F6B45', fill_type='solid')
    header_font = Font(color='FFFFFF', bold=True)

    for cell in sheet[1]:
        cell.fill = header_fill
        cell.font = header_font

    for document in documents:
        sheet.append([
            document.tracking_id,
            document.get_entry_type_display(),
            document.document_type,
            document.subject,
            document.source_zone.name if document.source_zone else '',
            document.source_department.name if document.source_department else '',
            document.destination_department.name if document.destination_department else '',
            document.current_department.name if document.current_department else '',
            document.get_status_display(),
            document.get_priority_display(),
            document.received_date.strftime('%Y-%m-%d') if document.received_date else '',
            document.sent_date.strftime('%Y-%m-%d') if document.sent_date else '',
            document.aging_days,
            document.remarks,
            document.created_by.username if document.created_by else '',
            document.created_at.strftime('%Y-%m-%d %I:%M %p'),
        ])

    column_widths = {
        'A': 18,
        'B': 14,
        'C': 18,
        'D': 35,
        'E': 18,
        'F': 20,
        'G': 24,
        'H': 24,
        'I': 25,
        'J': 12,
        'K': 15,
        'L': 15,
        'M': 12,
        'N': 35,
        'O': 15,
        'P': 20,
    }

    for column, width in column_widths.items():
        sheet.column_dimensions[column].width = width

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="document_records.xlsx"'

    workbook.save(response)
    return response