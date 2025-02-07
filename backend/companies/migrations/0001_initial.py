# Generated by Django 3.2.8 on 2021-12-29 07:24

import companies.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sectors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolios', '0001_initial'),
        ('markets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ticker', models.CharField(max_length=200)),
                ('alt_tickers', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('color', models.CharField(max_length=200)),
                ('broker', models.CharField(max_length=200)),
                ('country_code', models.CharField(max_length=200)),
                ('is_closed', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('base_currency', models.CharField(max_length=50)),
                ('dividends_currency', models.CharField(max_length=50)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=companies.models.user_directory_path)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='companies', to='markets.market')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='portfolios.portfolio')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='companies', to='sectors.sector')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
