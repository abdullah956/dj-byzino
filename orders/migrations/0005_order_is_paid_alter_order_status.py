# Generated by Django 5.1 on 2024-08-22 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('placed', 'Placed'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], max_length=50),
        ),
    ]
