from django import forms
from .models import Department, Document, DocumentMovement


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'entry_type',
            'document_type',
            'subject',
            'source_department',
            'source_zone',
            'destination_department',
            'current_department',
            'received_date',
            'sent_date',
            'priority',
            'status',
            'remarks',
            'attachment',
        ]

        widgets = {
            'entry_type': forms.Select(attrs={'class': 'form-control'}),
            'document_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Letter, Memo, Application, Report...'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'বিষয় লিখুন / Enter subject'
            }),
            'source_department': forms.Select(attrs={'class': 'form-control'}),
            'source_zone': forms.Select(attrs={'class': 'form-control'}),
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
            'source_department': 'Source Department',
            'source_zone': 'Source Zone',
            'destination_department': 'Destination Department',
            'current_department': 'Current Department',
            'received_date': 'Received Date',
            'sent_date': 'Sent Date',
            'priority': 'Priority',
            'status': 'Status',
            'remarks': 'Remarks / মন্তব্য',
            'attachment': 'Attachment',
        }




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
        label='Forward / Current Department'
    )

    class Meta:
        model = DocumentMovement
        fields = [
            'action',
            'to_department',
            'new_status',
            'remarks',
        ]

        widgets = {
            'action': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'মুভমেন্ট বা স্ট্যাটাস আপডেট সম্পর্কে মন্তব্য লিখুন'
            }),
        }

        labels = {
            'action': 'Action',
            'remarks': 'Remarks / মন্তব্য',
        }