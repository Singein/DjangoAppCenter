# Generated by Django 3.0.2 on 2020-10-06 11:27

import DjangoAppCenter.extensions.fields.snowflake.core
import DjangoAppCenter.extensions.fields.snowflake.field
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', DjangoAppCenter.extensions.fields.snowflake.field.SnowFlakeField(default=DjangoAppCenter.extensions.fields.snowflake.core.get_snowflake_id, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='package name')),
                ('app_name', models.CharField(max_length=255, verbose_name='app name')),
                ('repository', models.CharField(default='https://pypi.org/simple', max_length=255, verbose_name='repository')),
                ('enable', models.BooleanField(default=True, verbose_name='enable')),
                ('version', models.CharField(default='0.0.1', max_length=255, verbose_name='version')),
                ('old_version', models.CharField(default='0.0.1', editable=False, max_length=255, verbose_name='old_version')),
                ('is_app', models.BooleanField(default=False, help_text='register the package as an django app')),
                ('installing', models.BooleanField(default=False)),
                ('pip_version', models.CharField(choices=[('pip3', 'pip3'), ('pip', 'pip')], default='pip', max_length=255, verbose_name='pip version')),
            ],
            options={
                'db_table': 'dac_packages',
            },
        ),
    ]
