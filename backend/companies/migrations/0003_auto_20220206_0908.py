# Generated by Django 3.2.8 on 2022-02-06 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_alter_company_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='alt_tickers',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
