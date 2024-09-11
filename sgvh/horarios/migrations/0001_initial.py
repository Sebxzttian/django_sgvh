# Generated by Django 5.1.1 on 2024-09-10 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('numero_cedula', models.CharField(max_length=20, unique=True)),
                ('numero_celular', models.CharField(max_length=20)),
                ('correo_institucional', models.EmailField(max_length=254)),
                ('correo_personal', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('correo_personal', models.EmailField(max_length=254)),
                ('correo_institucional', models.EmailField(max_length=254)),
                ('numero_celular', models.CharField(max_length=20)),
                ('numero_cedula', models.CharField(max_length=20, unique=True)),
                ('competencias_imparte', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProgramaFormacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_programa', models.CharField(max_length=200)),
                ('jornada', models.CharField(max_length=50)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('instructores', models.ManyToManyField(to='horarios.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Competencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('unidad_competencia', models.CharField(max_length=200)),
                ('duracion_estimada', models.IntegerField(help_text='Duración estimada en horas')),
                ('resultado_aprendizaje', models.TextField()),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horarios.instructor')),
                ('programa_formacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horarios.programaformacion')),
            ],
        ),
        migrations.CreateModel(
            name='Ambiente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ambiente', models.CharField(max_length=100)),
                ('sede', models.CharField(max_length=100)),
                ('instructores', models.ManyToManyField(to='horarios.instructor')),
                ('programa_formacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horarios.programaformacion')),
            ],
        ),
    ]
