# Generated by Django 5.1.2 on 2024-10-20 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0008_alter_feedbacknote_feedback_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='feedback_checked',
            field=models.BooleanField(default=False, verbose_name='Geri dönüş yoxlanılması'),
        ),
        migrations.AddField(
            model_name='customer',
            name='feedback_date',
            field=models.DateField(blank=True, null=True, verbose_name='Geri dönüş tarixi'),
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
        migrations.DeleteModel(
            name='FeedbackNote',
        ),
    ]
