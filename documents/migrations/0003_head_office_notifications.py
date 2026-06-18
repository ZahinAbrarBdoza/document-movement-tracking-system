# Generated for Head Office receiving and dispatch notification workflow.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def create_receiving_desk_group(apps, schema_editor):
    group = apps.get_model('auth', 'Group')
    group.objects.get_or_create(name='Receiving Desk')


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('documents', '0002_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'Admin'), ('receiving_desk', 'Receiving Desk'), ('hr', 'HR'), ('adt', 'ADT'), ('ops', 'OPS'), ('management', 'Management')], max_length=30),
        ),
        migrations.AddField(
            model_name='document',
            name='addressed_to_designation',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='document',
            name='addressed_to_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='document',
            name='designated_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designated_documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='first_boss',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='notification_error',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='notification_required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='document',
            name='notification_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='notification_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='reference_no',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.RunPython(create_receiving_desk_group, migrations.RunPython.noop),
    ]
