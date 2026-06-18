from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone


def _display_user(user):
    if not user:
        return '-'
    return user.get_full_name() or user.username


def _display_value(value):
    return str(value) if value else '-'


def _addressed_to(document):
    parts = [
        document.addressed_to_name,
        document.addressed_to_designation,
    ]
    value = ', '.join(part for part in parts if part)
    return value or '-'


def send_forward_notification(document, request_user=None):
    if not document.notification_required:
        return 'skipped'

    if document.notification_sent:
        return 'already_sent'

    if not document.designated_person or not document.designated_person.email:
        document.notification_sent = False
        document.notification_error = 'Notification was not sent because the designated person or email is missing.'
        document.save(update_fields=['notification_sent', 'notification_error', 'updated_at'])
        return 'missing_recipient'

    recipient_email = document.designated_person.email
    cc_emails = []

    if document.first_boss and document.first_boss.email:
        cc_emails.append(document.first_boss.email)

    subject = f'Document Forwarded: {document.tracking_id} - {document.subject}'
    body = '\n'.join([
        'A physical document has been forwarded for your attention.',
        '',
        f'Tracking ID: {document.tracking_id}',
        f'Reference No: {_display_value(document.reference_no)}',
        f'Subject: {document.subject}',
        f'Addressed To: {_addressed_to(document)}',
        f'Source Division: {_display_value(document.source_division)}',
        f'Source Region: {_display_value(document.source_region)}',
        f'Source Area: {_display_value(document.source_area)}',
        f'Source Branch: {_display_value(document.source_branch)}',
        f'Source Department: {_display_value(document.source_department)}',
        f'Destination Department: {_display_value(document.destination_department)}',
        f'Receiving Department: {_display_value(document.current_department)}',
        f'Status: {document.get_status_display()}',
        f'Priority: {document.get_priority_display()}',
        f'Remarks: {_display_value(document.remarks)}',
        f'Forwarded by: {_display_user(request_user)}',
        '',
        'The physical document is being sent manually. Please coordinate with the receiving/dispatch desk as needed.',
    ])

    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
            cc=cc_emails,
        )
        email.send(fail_silently=False)
    except Exception as exc:
        document.notification_sent = False
        document.notification_error = str(exc)
        document.save(update_fields=['notification_sent', 'notification_error', 'updated_at'])
        return 'failed'

    document.notification_sent = True
    document.notification_sent_at = timezone.now()
    document.notification_error = ''
    document.save(update_fields=[
        'notification_sent',
        'notification_sent_at',
        'notification_error',
        'updated_at',
    ])
    return 'sent'
