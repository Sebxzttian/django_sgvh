from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError

class AdministradorManager(BaseUserManager):
    def create_user(self, correo_institucional, password=None, **extra_fields):
        if not correo_institucional:
            raise ValueError("El correo institucional debe ser proporcionado")
        extra_fields.setdefault('is_staff', True)  # Los administradores deben tener acceso al panel
        extra_fields.setdefault('is_admin', False)  # No todos los usuarios creados son administradores
        user = self.model(correo_institucional=self.normalize_email(correo_institucional), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_institucional, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser debe tener is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(correo_institucional, password, **extra_fields)

class Administrador(AbstractBaseUser, PermissionsMixin):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_cedula = models.CharField(max_length=20, unique=True)
    numero_celular = models.CharField(max_length=20)
    correo_institucional = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)  # Define si tienen acceso al panel de administración
    is_superuser = models.BooleanField(default=False)

    objects = AdministradorManager()

    USERNAME_FIELD = 'correo_institucional'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'numero_cedula', 'numero_celular']

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Instructor(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo_institucional = models.EmailField()
    numero_celular = models.CharField(max_length=15)
    numero_cedula = models.CharField(max_length=15, unique=True)
    competencias_imparte = models.CharField(max_length=50)
    
    class Meta:
        db_table = "Instructor"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ProgramaFormacion(models.Model):
    JORNADAS = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche')
    ]
    codigo_programa = models.CharField(max_length=15)
    nombre_programa = models.CharField(max_length=50)
    jornada = models.CharField(max_length=50, choices=JORNADAS)
    numero_ficha = models.CharField(max_length=10)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    class Meta:
        db_table = "ProgramaFormacion"

    def __str__(self):
        return self.nombre_programa

    def clean(self):
        # Verificar que la fecha_fin sea mayor que la fecha_inicio
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError("La fecha de fin debe ser mayor que la fecha de inicio.")

class Ambiente(models.Model):
    SEDE = [
        ('Principal', 'Principal'),
        ('Alternativa', 'Alternativa'),
        ('Granja', 'Granja')
    ]
    codigo_ambiente = models.CharField(max_length=15)
    nombre_ambiente = models.CharField(max_length=100)
    sede = models.CharField(max_length=100, choices=SEDE)
    
    class Meta:
        db_table = "Ambiente"

    def __str__(self):
        return self.nombre_ambiente

class Competencia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo_norma = models.IntegerField(blank=True, null=True, verbose_name="Código de la norma")
    unidad_competencia = models.CharField(max_length=500)
    duracion_estimada = models.CharField(max_length=50, help_text="Duración estimada para lograr el aprendizaje", verbose_name="Duración estimada (horas)")
    resultado_aprendizaje = models.TextField()
    
    class Meta:
        db_table = "Competencia"
        
    def __str__(self):
        return self.nombre

