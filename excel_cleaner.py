import pandas as pd
import os
import uuid

def generate_unique_id():
    return str(uuid.uuid4().int)[:8]

def process_file(input_file, output_file):
    possible_id_columns = ['id', 'Employee ID', 'WorkDay ID', 'ID', 'Nº Empleado', 'Nº', 'idsapcompleto', 'ID SAP', 'User ID', 'WD ID']
    possible_email_columns = ['email', 'Email', 'Work Email','Email Organizativo', 'correo', 'Email Corporativoº', 'Email Corporativo', 'Direccion de correo', 'Correo', 'SAML Federation ID', 'correo', 'correo electronico', 'Correo electrónico',]
    forbidden_email_words = ['noemail', 'noreal', 'notiene', 'no-email', 'no.correo', 'no-correo']

    try:
        # Cargar el archivo en un DataFrame
        if input_file.lower().endswith('.csv'):
            df = pd.read_csv(input_file, encoding='utf-8-sig', delimiter=';')
        elif input_file.lower().endswith('.xlsx'):
            df = pd.read_excel(input_file)
        else:
            raise ValueError("Formato de archivo no admitido")

        # Procesar el DataFrame
        rows = []
        for i, row in df.iterrows():
            email = next((row[column] for column in possible_email_columns if column in row and pd.notna(row[column])), None)
            id_value = next((row[column] for column in possible_id_columns if column in row and pd.notna(row[column])), None) or f"{generate_unique_id()}-{i}"

            if email and not any(forbidden_word in email for forbidden_word in forbidden_email_words):
                rows.append({'NIF': id_value, 'email': email})

        # Eliminar duplicados en la columna 'email'
        unique_rows = pd.DataFrame(rows).drop_duplicates(subset='email')

        # Guardar el resultado en un nuevo archivo CSV
        unique_rows.to_csv(output_file, index=False, encoding='utf-8-sig', sep=';')
        print('CLEAN!')

    except FileNotFoundError as e:
        print(f"Error: '{input_file}' no encontrado")
    except PermissionError:
        print("Permiso denegado")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == '__main__':
    input_file_path = "listado.xlsx"
    output_file_path = "listado_clean.csv"
    process_file(input_file_path, output_file_path)
