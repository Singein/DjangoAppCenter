# Generated by Django 3.0.2 on 2020-10-06 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('addition', models.TextField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'dac_settings',
            },
        ),
    ]
