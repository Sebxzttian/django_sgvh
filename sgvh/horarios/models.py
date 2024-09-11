from django.db import models

class Administrador(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_cedula = models.CharField(max_length=20, unique=True)
    numero_celular = models.CharField(max_length=20)
    correo_institucional = models.EmailField()
    correo_personal = models.EmailField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Instructor(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo_personal = models.EmailField()
    correo_institucional = models.EmailField()
    numero_celular = models.CharField(max_length=20)
    numero_cedula = models.CharField(max_length=20, unique=True)
    competencias_imparte = models.TextField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ProgramaFormacion(models.Model):
    nombre_programa = models.CharField(max_length=200)
    jornada = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    instructores = models.ManyToManyField(Instructor)

    def __str__(self):
        return self.nombre_programa

class Ambiente(models.Model):
    nombre_ambiente = models.CharField(max_length=100)
    sede = models.CharField(max_length=100)
    programa_formacion = models.ForeignKey(ProgramaFormacion, on_delete=models.CASCADE)
    instructores = models.ManyToManyField(Instructor)

    def __str__(self):
        return self.nombre_ambiente

class Competencia(models.Model):
    nombre = models.CharField(max_length=200)
    unidad_competencia = models.CharField(max_length=200)
    duracion_estimada = models.IntegerField(help_text="Duración estimada en horas")
    resultado_aprendizaje = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    programa_formacion = models.ForeignKey(ProgramaFormacion, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre