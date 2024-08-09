# Generated by Django 4.2.15 on 2024-08-09 11:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('dueDate', models.DateField()),
                ('status', models.CharField(choices=[('Open', 'Mở'), ('Planning Production', 'Lên Kế Hoạch Sản Xuất'), ('In Production', 'Đang Sản Xuất'), ('Delivering', 'Giao Hàng'), ('Completed', 'Hoàn Thành')], default='Open', max_length=50)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('lastModified', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('product_orders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productorder')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
