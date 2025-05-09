# Generated by Django 4.2.1 on 2023-07-12 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ForecastModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("turbine_id", models.CharField(max_length=20)),
                ("model_type", models.CharField(max_length=20)),
                ("model_data", models.CharField(max_length=60)),
                ("model_size", models.CharField(max_length=20)),
                ("model_path", models.CharField(max_length=80)),
                ("model_status", models.CharField(max_length=20)),
                ("model_comment", models.CharField(max_length=80)),
                ("model_trainTime", models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name="Turbine",
            fields=[
                (
                    "turbine_id",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("turbine_name", models.CharField(max_length=20)),
                ("turbine_comment", models.CharField(max_length=80)),
                ("turbine_status", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="TurbineData",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("turbine_id", models.CharField(max_length=20)),
                ("data_name", models.CharField(max_length=20)),
                ("data_type", models.CharField(max_length=20)),
                ("data_size", models.CharField(max_length=20)),
                ("data_path", models.CharField(max_length=80, unique=True)),
                ("data_comment", models.CharField(max_length=40)),
                ("data_uploadTime", models.CharField(max_length=40)),
                ("data_startTime", models.CharField(max_length=40)),
                ("data_endTime", models.CharField(max_length=40)),
            ],
        ),
    ]
