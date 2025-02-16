# Generated by Django 4.2.19 on 2025-02-16 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('humidity', models.FloatField(blank=True, null=True)),
                ('motion_detected', models.BooleanField(blank=True, null=True)),
                ('smoke_detected', models.BooleanField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='sensor_monitor.sensor')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
