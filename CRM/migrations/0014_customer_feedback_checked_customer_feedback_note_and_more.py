# Generated by Django 5.1.2 on 2024-10-21 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0013_remove_customer_products_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='feedback_checked',
            field=models.BooleanField(default=False, verbose_name='Geri dönüş yoxlanılması'),
        ),
        migrations.AddField(
            model_name='customer',
            name='feedback_note',
            field=models.TextField(blank=True, null=True, verbose_name='Geri dönüş qeydi'),
        ),
        migrations.AddField(
            model_name='customer',
            name='note_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Qeyd tarixi'),
        ),
        migrations.AddField(
            model_name='customer',
            name='products',
            field=models.ManyToManyField(through='CRM.CustomerProduct', to='CRM.product', verbose_name='Maraqlandığı məhsullar'),
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]