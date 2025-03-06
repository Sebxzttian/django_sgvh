import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font
from django.conf import settings
from .models import Instructor
import os

def create_instructor_template():
    try:
        # Obtener todos los instructores de la base de datos
        instructores = Instructor.objects.all()
        
        # Crear lista de datos
        data = []
        for instructor in instructores:
            data.append({
                'nombres': instructor.nombres,
                'apellidos': instructor.apellidos,
                'correo_institucional': instructor.correo_institucional,
                'numero_celular': instructor.numero_celular,
                'numero_cedula': instructor.numero_cedula
            })
        
        # Crear DataFrame con los datos de los instructores
        df = pd.DataFrame(data)
        
        # Si no hay instructores, crear una plantilla vacía con las columnas
        if df.empty:
            df = pd.DataFrame(columns=[
                'nombres',
                'apellidos',
                'correo_institucional',
                'numero_celular',
                'numero_cedula'
            ])
            # Añadir una fila de ejemplo
            df.loc[0] = [
                'Juan Carlos',
                'Pérez González',
                'jperez@sena.edu.co',
                '3001234567',
                '1234567890'
            ]

        # Asegurarse de que el directorio existe
        template_dir = os.path.join(settings.STATIC_ROOT, 'templates')
        os.makedirs(template_dir, exist_ok=True)

        # Guardar la plantilla
        template_path = os.path.join(template_dir, 'plantilla_instructores.xlsx')
        
        # Configurar el writer para dar formato al Excel
        writer = pd.ExcelWriter(template_path, engine='openpyxl')
        
        # Escribir el DataFrame al Excel con formato
        df.to_excel(writer, index=False, sheet_name='Instructores')
        
        # Obtener la hoja activa
        worksheet = writer.sheets['Instructores']
        
        # Ajustar el ancho de las columnas
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            ) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length
        
        # Dar formato al encabezado
        for cell in worksheet[1]:
            cell.style = 'Headline 3'
            cell.fill = openpyxl.styles.PatternFill(
                start_color='E2EFDA',
                end_color='E2EFDA',
                fill_type='solid'
            )
        
        # Guardar el archivo con el formato
        writer.close()
        
        return template_path
        
    except Exception as e:
        print(f"Error creando la plantilla: {str(e)}")
        raise e 