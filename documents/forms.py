from django import forms
from django.contrib.auth import get_user_model

from .models import (
    Area,
    Branch,
    CourierRate,
    Department,
    Division,
    Document,
    DocumentMovement,
    Region,
)


class ActiveUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        label = obj.get_full_name() or obj.username
        if obj.email:
            return f'{label} ({obj.email})'
        return label


class DocumentForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('created', 'Entry Created'),
        ('physical_received', 'Physical Document Received'),
        ('forwarded', 'Forwarded'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
        ('missing_physical_copy', 'Missing Physical Copy'),
    ]

    designated_person = ActiveUserChoiceField(
        queryset=get_user_model().objects.none(),
        required=False,
        empty_label='Select designated person',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'data-searchable-select': 'true',
            'data-search-placeholder': 'Search or select designated person',
        }),
        label='Designated Person'
    )
    first_boss = ActiveUserChoiceField(
        queryset=get_user_model().objects.none(),
        required=False,
        empty_label='Select first boss',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'data-searchable-select': 'true',
            'data-search-placeholder': 'Search or select first boss',
        }),
        label='First Boss'
    )

    class Meta:
        model = Document
        fields = [
            'entry_type',
            'document_type',
            'subject',
            'reference_no',
            'addressed_to_name',
            'addressed_to_designation',
            'designated_person',
            'first_boss',
            'notification_required',
            'source_type',
            'external_organization_type',
            'external_organization_name',
            'external_branch_name',
            'source_division',
            'source_region',
            'source_area',
            'source_branch',
            'source_department',
            'destination_department',
            'current_department',
            'received_date',
            'sent_date',
            'courier_rate',
            'outward_description',
            'outward_quantity',
            'outward_amount',
            'outward_is_manual',
            'priority',
            'status',
            'remarks',
            'attachment',
        ]

        widgets = {
            'entry_type': forms.Select(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={
                'class': 'form-control',
                'data-searchable-select': 'true',
                'data-search-placeholder': 'Search or select document type',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'বিষয় লিখুন / Enter subject'
            }),
            'reference_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Reference / memo number'
            }),
            'addressed_to_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name written on the document'
            }),
            'addressed_to_designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Designation written on the document'
            }),
            'notification_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'source_type': forms.Select(attrs={'class': 'form-control'}),
            'external_organization_type': forms.Select(attrs={'class': 'form-control'}),
            'external_organization_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization name'
            }),
            'external_branch_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Branch'
            }),
            'source_division': forms.Select(attrs={'class': 'form-control'}),
            'source_region': forms.Select(attrs={'class': 'form-control'}),
            'source_area': forms.Select(attrs={'class': 'form-control'}),
            'source_branch': forms.Select(attrs={'class': 'form-control'}),
            'source_department': forms.Select(attrs={'class': 'form-control'}),
            'destination_department': forms.Select(attrs={'class': 'form-control'}),
            'current_department': forms.Select(attrs={'class': 'form-control'}),
            'received_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'sent_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'courier_rate': forms.Select(attrs={'class': 'form-control'}),
            'outward_description': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }),
            'outward_quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }),
            'outward_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'outward_is_manual': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'মন্তব্য লিখুন / Enter remarks'
            }),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'entry_type': 'Entry Type',
            'document_type': 'Document Type',
            'subject': 'Subject / বিষয়',
            'reference_no': 'Reference No / স্মারক নং',
            'addressed_to_name': 'Addressed To Name / যার নামে এসেছে',
            'addressed_to_designation': 'Addressed To Designation / পদবি',
            'designated_person': 'Designated Person',
            'first_boss': 'First Boss',
            'notification_required': 'Notification Required',
            'source_type': 'Source Type',
            'external_organization_type': 'Organization Type',
            'external_organization_name': 'Organization Name',
            'external_branch_name': 'Branch',
            'source_division': 'Source Division',
            'source_region': 'Source Region',
            'source_area': 'Source Area',
            'source_branch': 'Source Branch',
            'source_department': 'Internal Source Department',
            'destination_department': 'Destination Department',
            'current_department': 'Current / Receiving Department',
            'received_date': 'Received Date',
            'sent_date': 'Sent Date',
            'courier_rate': 'বিস্তৃত বিবরণ - পরিমাণ',
            'outward_description': 'বিস্তৃত বিবরণ',
            'outward_quantity': 'পরিমাণ',
            'outward_amount': 'টাকার পরিমাণ',
            'outward_is_manual': 'Manual / Other item',
            'priority': 'Priority',
            'status': 'Status',
            'remarks': 'Remarks / মন্তব্য',
            'attachment': 'Attachment',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_queryset = get_user_model().objects.filter(is_active=True).order_by(
            'first_name',
            'last_name',
            'username',
        )
        self.fields['designated_person'].queryset = user_queryset
        self.fields['first_boss'].queryset = user_queryset
        self.fields['status'].choices = self.STATUS_CHOICES
        self.fields['courier_rate'].queryset = CourierRate.objects.filter(
            is_active=True
        ).order_by('description', 'quantity')
        self.fields['courier_rate'].empty_label = 'Select courier/service rate'
        self.fields['subject'].required = False
        self.fields['source_type'].required = False
        self.fields['external_organization_type'].required = False
        self.fields['external_organization_name'].required = False
        self.fields['external_branch_name'].required = False
        self.fields['received_date'].required = False
        self.fields['sent_date'].required = False

        for field_name in [
            'courier_rate',
            'outward_description',
            'outward_quantity',
            'outward_amount',
            'outward_is_manual',
        ]:
            self.fields[field_name].required = False

        self.fields['source_division'].queryset = Division.objects.filter(
            is_active=True
        ).order_by('name')
        self.fields['source_region'].queryset = Region.objects.none()
        self.fields['source_area'].queryset = Area.objects.none()
        self.fields['source_branch'].queryset = Branch.objects.none()

        division_id = self._selected_source_id('source_division')
        region_id = self._selected_source_id('source_region')
        area_id = self._selected_source_id('source_area')

        if division_id:
            self.fields['source_region'].queryset = Region.objects.filter(
                division_id=division_id,
                is_active=True,
            ).order_by('name')

        if region_id:
            self.fields['source_area'].queryset = Area.objects.filter(
                region_id=region_id,
                is_active=True,
            ).order_by('name')

        if area_id:
            self.fields['source_branch'].queryset = Branch.objects.filter(
                area_id=area_id,
                is_active=True,
            ).order_by('name')

    def _selected_source_id(self, field_name):
        if self.is_bound:
            value = self.data.get(self.add_prefix(field_name))
        else:
            value = getattr(self.instance, f'{field_name}_id', None)

        if value and str(value).isdigit():
            return value

        return None

    def clean(self):
        cleaned_data = super().clean()
        entry_type = cleaned_data.get('entry_type')
        source_type = cleaned_data.get('source_type') or 'internal'
        external_organization_type = cleaned_data.get('external_organization_type')
        external_organization_name = (cleaned_data.get('external_organization_name') or '').strip()
        external_branch_name = (cleaned_data.get('external_branch_name') or '').strip()
        received_date = cleaned_data.get('received_date')
        sent_date = cleaned_data.get('sent_date')
        courier_rate = cleaned_data.get('courier_rate')
        outward_is_manual = cleaned_data.get('outward_is_manual')
        outward_amount = cleaned_data.get('outward_amount')

        if entry_type == 'inward':
            if not received_date:
                self.add_error('received_date', 'Received Date is required for inward documents.')
            cleaned_data['sent_date'] = None
        elif entry_type == 'outward':
            if not sent_date:
                self.add_error('sent_date', 'Sent Date is required for outward documents.')
            cleaned_data['received_date'] = None

        cleaned_data['source_type'] = source_type

        if source_type == 'external':
            cleaned_data['source_division'] = None
            cleaned_data['source_region'] = None
            cleaned_data['source_area'] = None
            cleaned_data['source_branch'] = None
            cleaned_data['source_department'] = None

            if not external_organization_type:
                self.add_error('external_organization_type', 'Select an organization type.')
            elif external_organization_type in {'bank', 'other'}:
                if not external_organization_name:
                    self.add_error('external_organization_name', 'Enter the organization name.')
                if not external_branch_name:
                    self.add_error('external_branch_name', 'Enter the branch.')
            else:
                cleaned_data['external_organization_name'] = ''
                cleaned_data['external_branch_name'] = ''
        else:
            cleaned_data['source_type'] = 'internal'
            cleaned_data['external_organization_type'] = ''
            cleaned_data['external_organization_name'] = ''
            cleaned_data['external_branch_name'] = ''

        if outward_amount is not None and outward_amount < 0:
            self.add_error('outward_amount', 'টাকার পরিমাণ শূন্য বা তার বেশি হতে হবে।')

        if outward_is_manual:
            cleaned_data['courier_rate'] = None
        elif courier_rate:
            cleaned_data['outward_description'] = courier_rate.description
            cleaned_data['outward_quantity'] = courier_rate.quantity
            if outward_amount is None:
                cleaned_data['outward_amount'] = courier_rate.amount

        return cleaned_data




class DocumentMovementForm(forms.ModelForm):
    new_status = forms.ChoiceField(
        choices=Document.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='New Status'
    )

    to_department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Forward / Receiving Department'
    )

    def __init__(self, *args, **kwargs):
        status_choices = kwargs.pop('status_choices', None)
        allow_department_change = kwargs.pop('allow_department_change', True)
        super().__init__(*args, **kwargs)

        if status_choices is not None:
            self.fields['new_status'].choices = status_choices

        if not allow_department_change:
            self.fields['to_department'].required = False
            self.fields['to_department'].widget = forms.HiddenInput()

    class Meta:
        model = DocumentMovement
        fields = [
            'to_department',
            'new_status',
            'remarks',
        ]

        widgets = {
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'মুভমেন্ট বা স্ট্যাটাস আপডেট সম্পর্কে মন্তব্য লিখুন'
            }),
        }

        labels = {
            'remarks': 'Remarks / মন্তব্য',
        }
