# Generated by Django 3.2.25 on 2024-06-10 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20240605_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='quote',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
