# Generated by Django 4.2.7 on 2023-11-03 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_options_verificationtoken_session'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VerificationToken',
        ),
    ]