# Generated by Django 4.2.7 on 2023-11-29 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('token_blacklist', '0012_alter_outstandingtoken_user'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='token',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='token_blacklist.outstandingtoken'),
        ),
    ]
