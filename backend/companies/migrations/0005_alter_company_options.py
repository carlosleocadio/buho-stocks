# Generated by Django 3.2.13 on 2022-08-10 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_company_isin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name_plural': 'Companies'},
        ),
    ]
