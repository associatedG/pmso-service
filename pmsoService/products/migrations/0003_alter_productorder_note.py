# Generated by Django 5.0.7 on 2024-09-29 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_productorder_note"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productorder",
            name="note",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
