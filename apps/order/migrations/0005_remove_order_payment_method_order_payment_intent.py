# Generated by Django 4.2.7 on 2023-12-29 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_intent',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]