# Generated by Django 3.0.2 on 2021-03-25 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='addition',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='备注说明'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='设置名称'),
        ),
    ]
