# Generated by Django 5.1.6 on 2025-02-24 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0004_vendordocument'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='submitted_documents',
        ),
        migrations.AlterField(
            model_name='vendor',
            name='tender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendors', to='tenders.tender'),
        ),
    ]
