# Generated by Django 4.0.4 on 2022-06-03 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_chart_filter_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='month',
            field=models.CharField(choices=[('01', 'January'), ('02', 'Feburary'), ('03', 'March'), ('04', 'April'), ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=15),
        ),
        migrations.AlterField(
            model_name='chart',
            name='year',
            field=models.CharField(choices=[('2020', '2020'), ('2021', '2021')], max_length=15),
        ),
    ]