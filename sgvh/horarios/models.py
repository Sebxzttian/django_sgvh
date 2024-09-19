from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AdministradorManager(BaseUserManager):
    def create_user(self, correo_personal, password=None, **extra_fields):
        if not correo_personal:
            raise ValueError("El correo personal debe ser proporcionado")
        user = self.model(correo_personal=self.normalize_email(correo_personal), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_personal, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(correo_personal, password, **extra_fields)      

class Administrador(AbstractBaseUser):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_cedula = models.CharField(max_length=20, unique=True)
    numero_celular = models.CharField(max_length=20)
    correo_institucional = models.EmailField()
    correo_personal = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AdministradorManager()

    USERNAME_FIELD = 'correo_personal'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'numero_cedula', 'numero_celular', 'correo_institucional']

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def is_staff(self):
        return self.is_admin

    # Añadir los siguientes métodos requeridos por Django
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

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
    codigo_programa = models.CharField(max_length=15,)
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
    sede = models.CharField(max_length=100, choices=SEDE )
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