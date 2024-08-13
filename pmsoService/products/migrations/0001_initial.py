# Generated by Django 4.2.15 on 2024-08-13 03:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('category', models.CharField(choices=[('Phuy', 'Phuy'), ('Thung', 'Thung'), ('Cơ Khí Ô Tô', 'Cơ Khí Ô Tô')], max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_urgent', models.BooleanField(default=False)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('Open', 'Mở'), ('Planning Production', 'Lên Kế Hoạch Sản Xuất'), ('In Production', 'Đang Sản Xuất'), ('Delivering', 'Giao Hàng'), ('Completed', 'Hoàn Thành')], default='Open', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True, null=True)),
                ('deliverer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='delivery_orders', to=settings.AUTH_USER_MODEL)),
                ('logistic_staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='logistic_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('product_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productorder')),
            ],
        ),
        migrations.AddField(
            model_name='productorder',
            name='products',
            field=models.ManyToManyField(through='products.ProductOrderProduct', to='products.product'),
        ),
        migrations.AddField(
            model_name='productorder',
            name='sale_staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='sale_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
