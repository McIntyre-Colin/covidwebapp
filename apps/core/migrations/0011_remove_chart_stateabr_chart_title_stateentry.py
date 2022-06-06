# Generated by Django 4.0.5 on 2022-06-06 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_chart_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chart',
            name='stateAbr',
        ),
        migrations.AddField(
            model_name='chart',
            name='title',
            field=models.CharField(default='Informative Title!', max_length=100),
        ),
        migrations.CreateModel(
            name='StateEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_1', models.CharField(choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2)),
                ('state_2', models.CharField(choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2)),
                ('state_3', models.CharField(choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2)),
                ('state_4', models.CharField(choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2)),
                ('state_5', models.CharField(choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2)),
                ('state_6', models.CharField(choices=[('ca', 'CA'), ('pa', 'PA'), ('ak', 'AK')], max_length=2)),
                ('plot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.chart')),
            ],
        ),
    ]
