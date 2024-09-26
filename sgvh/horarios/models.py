from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class AdministradorManager(BaseUserManager):
    def create_user(self, correo_personal, password=None, **extra_fields):
        if not correo_personal:
            raise ValueError("El correo personal debe ser proporcionado")
        extra_fields.setdefault('is_staff', True)  # Los administradores deben tener acceso al panel
        extra_fields.setdefault('is_admin', False)  # No todos los usuarios creados son administradores
        user = self.model(correo_personal=self.normalize_email(correo_personal), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_personal, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser debe tener is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(correo_personal, password, **extra_fields)

class Administrador(AbstractBaseUser, PermissionsMixin):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_cedula = models.CharField(max_length=20, unique=True)
    numero_celular = models.CharField(max_length=20)
    correo_institucional = models.EmailField()
    correo_personal = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)  # Solo ciertos usuarios son administradores
    is_staff = models.BooleanField(default=True)  # Define si tienen acceso al panel de administración
    is_superuser = models.BooleanField(default=False)

    objects = AdministradorManager()

    USERNAME_FIELD = 'correo_personal'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'numero_cedula', 'numero_celular', 'correo_institucional']

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Instructor(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo_personal = models.EmailField()
    correo_institucional = models.EmailField()
    numero_celular = models.CharField(max_length=15)
    numero_cedula = models.CharField(max_length=15, unique=True)
    competencias_imparte = models.CharField(max_length=50)

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
    instructores = models.ManyToManyField(Instructor)

    def __str__(self):
        return self.nombre_programa

class Ambiente(models.Model):
    SEDE = [
        ('Principal', 'Principal'),
        ('Alternativa', 'Alternativa'),
        ('Granja', 'Granja')
    ]
    nombre_ambiente = models.CharField(max_length=100)
    sede = models.CharField(max_length=100, choices=SEDE)
    programa_formacion = models.ForeignKey(ProgramaFormacion, on_delete=models.CASCADE)
    instructores = models.ManyToManyField(Instructor)

    def __str__(self):
        return self.nombre_ambiente

class Competencia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo_norma = models.CharField(max_length=50, blank=True, null=True)
    unidad_competencia = models.CharField(max_length=500)
    duracion_estimada = models.CharField(max_length=50, help_text="Duración estimada para lograr el aprendizaje")
    resultado_aprendizaje = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    programa_formacion = models.ForeignKey(ProgramaFormacion, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
