# Generated by Django 5.1.2 on 2024-10-14 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Adı, Soyadı')),
                ('contact_number', models.CharField(max_length=20, verbose_name='Əlaqə nömrəsi')),
                ('initial_price_offer', models.CharField(blank=True, max_length=50, null=True, verbose_name='İlkin qiymət təklifi')),
                ('inquiry_method', models.CharField(blank=True, max_length=255, null=True, verbose_name='Müraciət vasitəsi')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Ünvan')),
                ('feedback_note', models.TextField(blank=True, null=True, verbose_name='Geri dönüş qeydi')),
                ('feedback_date', models.DateField(blank=True, null=True, verbose_name='Geri dönüş tarixi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma tarixi')),
                ('customer_code', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Müştəri Kodu')),
            ],
            options={
                'verbose_name': 'Müştəri',
                'verbose_name_plural': 'Müştərilər',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Xüsusiyyətin adı')),
            ],
            options={
                'verbose_name': 'Xüsusiyyət',
                'verbose_name_plural': 'Xüsusiyyətlər',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Məhsulun adı')),
            ],
            options={
                'verbose_name': 'Məhsul',
                'verbose_name_plural': 'Məhsullar',
            },
        ),
        migrations.CreateModel(
            name='PriceOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma tarixi')),
                ('views_count', models.IntegerField(default=0, verbose_name='Baxış sayı')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_offers', to='CRM.customer', verbose_name='Müştəri')),
            ],
            options={
                'verbose_name': 'Qiymət Təklifi',
                'verbose_name_plural': 'Qiymət Təklifləri',
            },
        ),
        migrations.CreateModel(
            name='PriceOfferProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Məhsulun ölçüsü')),
                ('price', models.CharField(blank=True, max_length=30, null=True, verbose_name='Məhsulun qiyməti')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Sayı')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Məhsulun açıqlaması')),
                ('design_3d_url', models.URLField(blank=True, max_length=500, null=True, verbose_name='3D dizayn linki')),
                ('price_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.priceoffer', verbose_name='Qiymət təklifi')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.product', verbose_name='Məhsul')),
            ],
            options={
                'verbose_name': 'Müştəri Məhsulu',
                'verbose_name_plural': 'Müştəri Məhsulları',
            },
        ),
        migrations.CreateModel(
            name='CustomerProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Məhsulun ölçüsü')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.customer', verbose_name='Müştəri')),
                ('features', models.ManyToManyField(blank=True, to='CRM.feature', verbose_name='Xüsusiyyətlər')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.product', verbose_name='Məhsul')),
            ],
            options={
                'verbose_name': 'Müştəri Məhsulu',
                'verbose_name_plural': 'Müştəri Məhsulları',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='products',
            field=models.ManyToManyField(through='CRM.CustomerProduct', to='CRM.product', verbose_name='Maraqlandığı məhsullar'),
        ),
        migrations.CreateModel(
            name='SalesContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Sistem adı')),
                ('glass_thickness', models.CharField(blank=True, max_length=100, null=True, verbose_name='Şüşənin qalınlığı')),
                ('profile_color', models.CharField(blank=True, max_length=100, null=True, verbose_name='Profil rəngi')),
                ('sales_price', models.CharField(max_length=50, verbose_name='Satış qiyməti')),
                ('payment_type', models.CharField(choices=[('Nağd', 'Nağd'), ('Taksit', 'Taksit')], max_length=50, verbose_name='Ödəniş növü')),
                ('total_size', models.CharField(max_length=100, verbose_name='Toplam m²')),
                ('is_single_glass', models.BooleanField(default=False, verbose_name='Şüşə 8mm tək qat şüşə olacaqdır.')),
                ('is_double_glass', models.BooleanField(default=False, verbose_name='Şüşə paket şüşə olacaqdır.')),
                ('is_stainless_colored_glass', models.BooleanField(default=False, verbose_name='Şüşə paslanmayan və rəngli olacaqdır.')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma tarixi')),
                ('views_count', models.IntegerField(default=0, verbose_name='Baxış sayı')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_contracts', to='CRM.customer', verbose_name='Müştəri')),
            ],
            options={
                'verbose_name': 'Satış Sözləşməsi',
                'verbose_name_plural': 'Satış Sözləşmələri',
            },
        ),
    ]
