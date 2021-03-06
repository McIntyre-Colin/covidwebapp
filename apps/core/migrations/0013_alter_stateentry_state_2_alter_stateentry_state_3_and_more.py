# Generated by Django 4.0.5 on 2022-06-06 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_plot_id_stateentry_plot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stateentry',
            name='state_2',
            field=models.CharField(blank=True, choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2),
        ),
        migrations.AlterField(
            model_name='stateentry',
            name='state_3',
            field=models.CharField(blank=True, choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2),
        ),
        migrations.AlterField(
            model_name='stateentry',
            name='state_4',
            field=models.CharField(blank=True, choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2),
        ),
        migrations.AlterField(
            model_name='stateentry',
            name='state_5',
            field=models.CharField(blank=True, choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2),
        ),
        migrations.AlterField(
            model_name='stateentry',
            name='state_6',
            field=models.CharField(blank=True, choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2),
        ),
    ]
