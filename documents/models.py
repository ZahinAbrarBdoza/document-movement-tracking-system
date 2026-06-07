from django.conf import settings
from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hr', 'HR'),
        ('adt', 'ADT'),
        ('ops', 'OPS'),
        ('management', 'Management'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_profiles'
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    designation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Document(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('inward', 'Inward'),
        ('outward', 'Outward'),
    ]

    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('created', 'Entry Created'),
        ('physical_received', 'Physical Document Received'),
        ('forwarded', 'Forwarded'),
        ('received_by_department', 'Received by Department'),
        ('in_progress', 'In Progress'),
        ('action_taken', 'Action Taken'),
        ('closed', 'Closed'),
        ('returned', 'Returned'),
        ('on_hold', 'On Hold'),
        ('missing_physical_copy', 'Missing Physical Copy'),
    ]

    tracking_id = models.CharField(max_length=50, unique=True, blank=True)
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES)
    document_type = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=255)

    source_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='source_documents'
    )
    source_zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='source_documents'
    )
    destination_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='destination_documents'
    )
    current_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_documents'
    )

    received_date = models.DateField(null=True, blank=True)
    sent_date = models.DateField(null=True, blank=True)

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    remarks = models.TextField(blank=True)

    attachment = models.FileField(upload_to='documents/', null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            year = timezone.now().year
            last_document = Document.objects.filter(
                tracking_id__startswith=f'DOC-{year}'
            ).order_by('-id').first()

            if last_document:
                last_number = int(last_document.tracking_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.tracking_id = f'DOC-{year}-{new_number:06d}'

        if self.status == 'closed' and not self.closed_at:
            self.closed_at = timezone.now()

        super().save(*args, **kwargs)

    @property
    def aging_days(self):
        if self.status == 'closed' and self.closed_at:
            return (self.closed_at.date() - self.created_at.date()).days
        return (timezone.now().date() - self.created_at.date()).days

    def __str__(self):
        return f'{self.tracking_id} - {self.subject}'


class DocumentMovement(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('physical_received', 'Physical Received'),
        ('forwarded', 'Forwarded'),
        ('received', 'Received'),
        ('status_updated', 'Status Updated'),
        ('closed', 'Closed'),
        ('returned', 'Returned'),
        ('comment_added', 'Comment Added'),
    ]

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='movements'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    from_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movement_from'
    )
    to_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movement_to'
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.document.tracking_id} - {self.action}'