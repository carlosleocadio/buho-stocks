# Generated by Django 3.2.8 on 2021-10-30 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sectors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sector',
            name='super_sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sectors', to='sectors.supersector'),
        ),
    ]
