from django.conf import settings
from django.core.validators import MinValueValidator
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


class Division(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name='regions'
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('division', 'name')
        ordering = ['division__name', 'name']

    def __str__(self):
        return self.name


class Area(models.Model):
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='areas'
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('region', 'name')
        ordering = ['region__division__name', 'region__name', 'name']

    def __str__(self):
        return self.name


class Branch(models.Model):
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name='branches'
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('area', 'name')
        ordering = ['area__region__division__name', 'area__region__name', 'area__name', 'name']

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('receiving_desk', 'Receiving Desk'),
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

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f'{self.user.username} Profile'


class CourierRate(models.Model):
    description = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    remarks = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['description', 'quantity']
        unique_together = ('description', 'quantity', 'amount')

    def __str__(self):
        return f'{self.description} - {self.quantity} - {self.amount}'

class Document(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('inward', 'Inward'),
        ('outward', 'Outward'),
    ]

    DOCUMENT_TYPE_CHOICES = [
        ('Letter', 'Letter'),
        ('Memo', 'Memo'),
        ('Application', 'Application'),
        ('Report', 'Report'),
        ('Complaint', 'Complaint'),
        ('Other', 'Other'),
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

    SOURCE_TYPE_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
    ]

    EXTERNAL_ORGANIZATION_TYPE_CHOICES = [
        ('pksf', 'PKSF'),
        ('mra', 'MRA'),
        ('bank', 'Bank'),
        ('other', 'Other Organization'),
    ]

    tracking_id = models.CharField(max_length=50, unique=True, blank=True)
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES)
    document_type = models.CharField(max_length=100, choices=DOCUMENT_TYPE_CHOICES, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    reference_no = models.CharField(max_length=100, blank=True)
    addressed_to_name = models.CharField(max_length=150, blank=True)
    addressed_to_designation = models.CharField(max_length=150, blank=True)

    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_TYPE_CHOICES,
        default='internal',
    )
    external_organization_type = models.CharField(
        max_length=30,
        choices=EXTERNAL_ORGANIZATION_TYPE_CHOICES,
        blank=True,
    )
    external_organization_name = models.CharField(max_length=255, blank=True)
    external_branch_name = models.CharField(max_length=255, blank=True)

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
    source_division = models.ForeignKey(
        Division,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='source_documents'
    )
    source_region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='source_documents'
    )
    source_area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='source_documents'
    )
    source_branch = models.ForeignKey(
        Branch,
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
    designated_person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='designated_documents'
    )
    first_boss = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_documents'
    )

    received_date = models.DateField(null=True, blank=True)
    sent_date = models.DateField(null=True, blank=True)

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    remarks = models.TextField(blank=True)
    notification_required = models.BooleanField(default=True)
    notification_sent = models.BooleanField(default=False)
    notification_sent_at = models.DateTimeField(null=True, blank=True)
    notification_error = models.TextField(blank=True)

    attachment = models.FileField(upload_to='documents/', null=True, blank=True)
    courier_rate = models.ForeignKey(
        CourierRate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )
    outward_description = models.CharField(max_length=255, blank=True)
    outward_quantity = models.CharField(max_length=255, blank=True)
    outward_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    outward_is_manual = models.BooleanField(default=False)

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

    @property
    def source_display(self):
        if self.source_type == 'external':
            if self.external_organization_type in {'pksf', 'mra'}:
                return self.get_external_organization_type_display()

            if self.external_organization_type in {'bank', 'other'}:
                if self.external_organization_name and self.external_branch_name:
                    return f'{self.external_organization_name} - {self.external_branch_name}'
                return (
                    self.external_organization_name or
                    self.external_branch_name or
                    self.get_external_organization_type_display() or
                    '-'
                )

            return self.get_external_organization_type_display() or '-'

        return (
            self.source_branch or
            self.source_area or
            self.source_region or
            self.source_division or
            self.source_department or
            '-'
        )

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
