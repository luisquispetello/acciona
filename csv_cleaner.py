import csv
import uuid

def generate_unique_id():
    return str(uuid.uuid4().int)[:8]


def process_csv(input_file, output_file):

    rows = []

    # Nombres posibles de las columnas 'id' y 'email'
    possible_id_columns = ['id', 'Employee ID', 'ID', 'Nº Empleado', 'Nº', 'idsapcompleto', 'ID SAP', 'User ID', 'WD ID']
    possible_email_columns = ['email', 'Email', 'Work Email', 'Email Organizativo', 'correo', 'Email Corporativoº', 'Email Corporativo', 'Direccion de correo', 'Correo', 'SAML Federation ID', 'correo', 'correo electronico', 'Correo electrónico']
    forbidden_email_words = ['noemail', 'noreal', 'notiene', 'no-email', 'no.correo', 'no-correo']

    try:
        # Leer el archivo CSV y realizar las operaciones
        with open(input_file, "r", encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')

            for i, row in enumerate(csv_reader, start=1):
                # Verificar y manejar celdas vacías en la columna 'email'
                email = next((row[column] for column in possible_email_columns if column in row and row[column]), None)
                
                # Verificar y manejar celdas vacías en la columna 'ID'
                id_value = next((row[column] for column in possible_id_columns if column in row), None)
                id_value = id_value if id_value else f"{generate_unique_id()}-{i}"

                # Verificar si el correo electrónico contiene palabras prohibidas
                if email and not any(forbidden_word in email for forbidden_word in forbidden_email_words):
                    # Construir una nueva fila con solo 'id' y 'email'
                    new_row = {'ID': id_value, 'email': email}
                    rows.append(new_row)

        # Eliminar duplicados en la columna 'email'
        unique_rows = {row["email"]: row for row in rows}.values()

        # Guardar el resultado en un nuevo archivo CSV
        with open(output_file, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["ID", "email"]  # Ajustar según tus columnas
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')

            # Escribir el encabezado
            writer.writeheader()

            # Escribir filas únicas
            writer.writerows(unique_rows)

    except FileNotFoundError:
        print(f"Error: '{input_file}' no encontrado ")
    except PermissionError:
        print("Permiso denegado")


if __name__ == '__main__':
    input_file_path = "listado.csv"
    output_file_path = "listado_clean.csv"
    process_csv(input_file_path, output_file_path)
