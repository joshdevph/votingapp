# Generated by Django 3.0.8 on 2020-07-09 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_votemaster', '0005_auto_20200708_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nominee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sh_id', models.CharField(max_length=255)),
                ('election_code', models.CharField(max_length=255)),
                ('sh_fullname', models.CharField(max_length=255)),
            ],
        ),
    ]
