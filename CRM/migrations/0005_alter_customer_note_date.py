# Generated by Django 5.1.2 on 2024-10-16 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0004_alter_customer_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='note_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Qeyd tarixi'),
        ),
    ]
