# Generated by Django 5.1.2 on 2024-10-27 10:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0019_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Design3D',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='3D Dizayn Başlıq')),
                ('image', models.ImageField(blank=True, null=True, upload_to='designs/', verbose_name='3D Dizayn şəkil')),
                ('url', models.URLField(blank=True, max_length=500, null=True, verbose_name='3D Dizayn Link')),
            ],
            options={
                'verbose_name': '3D Dizayn',
                'verbose_name_plural': '3D Dizaynlar',
            },
        ),
        migrations.RemoveField(
            model_name='priceofferproduct',
            name='design_3d_url',
        ),
        migrations.AlterField(
            model_name='priceofferproduct',
            name='price_offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.priceoffer', verbose_name='Qiymət Təklifi'),
        ),
        migrations.AddField(
            model_name='priceofferproduct',
            name='design_3d',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CRM.design3d', verbose_name='3D Dizayn'),
        ),
    ]
