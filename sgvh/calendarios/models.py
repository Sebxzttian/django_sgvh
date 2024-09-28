from django.db import models
from horarios.models import ProgramaFormacion, Ambiente, Competencia, Instructor

class CalInst(models.Model):
    programa = models.ForeignKey(ProgramaFormacion, on_delete=models.CASCADE)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE)
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "calins"

    def __str__(self):
        return f"{self.programa.nombre_programa} - {self.ambiente.nombre_ambiente} - {self.competencia.nombre}"

    @property
    def codigo_programa(self):
        return self.programa.codigo_programa

    @property
    def nombre_programa(self):
        return self.programa.nombre_programa

    @property
    def codigo_ambiente(self):
        return self.ambiente.codigo_ambiente

    @property
    def nombre_ambiente(self):
        return self.ambiente.nombre_ambiente

    @property
    def norma_competencia(self):
        return self.competencia.codigo_norma

    @property
    def nombre_competencia(self):
        return self.competencia.nombre

class CalPF(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE)
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "calpf"

    def __str__(self):
        return f"{self.instructor.nombres} - {self.ambiente.nombre_ambiente} - {self.competencia.nombre}"

    @property
    def nombres_instructor(self):
        return self.instructor.nombres
    
    @property
    def apellidos_instructor(self):
        return self.instructor.apellidos

    @property
    def codigo_ambiente(self):
        return self.ambiente.codigo_ambiente

    @property
    def nombre_ambiente(self):
        return self.ambiente.nombre_ambiente

    @property
    def norma_competencia(self):
        return self.competencia.codigo_norma

    @property
    def nombre_competencia(self):
        return self.competencia.nombre

class CalAmb(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    programa = models.ForeignKey(ProgramaFormacion, on_delete=models.CASCADE)
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "calamb"

    def __str__(self):
        return f"{self.instructor.nombres} - {self.programa.nombre_programa} - {self.competencia.nombre}"

    @property
    def nombres_instructor(self):
        return self.instructor.nombres
    
    @property
    def apellidos_instructor(self):
        return self.instructor.apellidos

    @property
    def codigo_programa(self):
        return self.programa.codigo_programa

    @property
    def nombre_programa(self):
        return self.programa.nombre_programa

    @property
    def norma_competencia(self):
        return self.competencia.codigo_norma

    @property
    def nombre_competencia(self):
        return self.competencia.nombre