# Generated by Django 5.0.8 on 2024-10-03 21:57

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('tier', models.CharField(choices=[('tier 1', 'Cấp độ 1'), ('tier 2', 'Cấp độ 2'), ('tier 3', 'Cấp độ 3')], max_length=50)),
                ('fax', models.IntegerField(blank=True, null=True)),
                ('contact_list', models.JSONField(blank=True, default=dict, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('category', models.CharField(choices=[('Phuy', 'Phuy'), ('Thùng', 'Thùng'), ('Cơ Khí Ô Tô', 'Cơ Khí Ô Tô')], max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('is_urgent', models.BooleanField(default=False)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('Open', 'Mở'), ('Processing', 'Đang xử lý đơn hàng'), ('BuyingMaterial', 'Lên Kế Hoạch Sản Xuất'), ('InProduction', 'Đang Sản Xuất'), ('Delivering', 'Giao Hàng'), ('Completed', 'Hoàn Thành'), ('Cancelled', 'Cancelled')], default='Open', max_length=50)),
                ('note', models.CharField(blank=True, default='', max_length=2000)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='products.customer')),
                ('deliverer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='delivery_orders', to=settings.AUTH_USER_MODEL)),
                ('logistic_staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='logistic_orders', to=settings.AUTH_USER_MODEL)),
                ('sale_staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sale_orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product Order',
                'verbose_name_plural': 'Product Orders',
                'ordering': ['due_date'],
            },
        ),
        migrations.CreateModel(
            name='ProductOrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('product_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.productorder')),
            ],
            options={
                'verbose_name': 'Product Order Product',
                'verbose_name_plural': 'Product Order Products',
            },
        ),
    ]
