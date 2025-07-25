# Generated by Django 4.2.23 on 2025-07-26 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_alter_region_options_region_code_region_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='job_posts', to='jobs.region', verbose_name='地区'),
        ),
    ]
