# Generated by Django 5.1.2 on 2024-10-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0005_alter_customer_note_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='feedback_checked',
            field=models.BooleanField(default=False, verbose_name='Geri dönüş yoxlanılması'),
        ),
    ]
