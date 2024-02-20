# Generated by Django 4.2.8 on 2024-02-20 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_type_alter_marker_type'),
        ('sticker_instructions', '0003_remove_sticker_html_code_htmlcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='htmlcode',
            name='sample_board',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.sampleboard'),
        ),
    ]
