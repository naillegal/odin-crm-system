# Generated by Django 5.1.2 on 2024-10-15 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0003_customer_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='note_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Qeyd tarixi'),
        ),
    ]
