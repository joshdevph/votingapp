# Generated by Django 3.0.8 on 2020-07-08 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_votemaster', '0004_attendance_at_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='sh_email',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='sh_shares',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
