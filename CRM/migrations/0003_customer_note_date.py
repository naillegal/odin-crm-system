# Generated by Django 5.1.2 on 2024-10-15 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0002_alter_priceofferproduct_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='note_date',
            field=models.DateField(blank=True, null=True, verbose_name='Qeyd tarixi'),
        ),
    ]
