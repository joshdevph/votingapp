# Generated by Django 2.2.6 on 2020-07-03 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_newstockholder', '0004_auto_20200703_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockholder',
            name='sh_password_status',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]