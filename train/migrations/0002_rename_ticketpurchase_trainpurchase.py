# Generated by Django 4.2.7 on 2024-03-08 08:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('train', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TicketPurchase',
            new_name='TrainPurchase',
        ),
    ]