"""Taller evaluable presencial - Limpieza de texto y generación de n-gramas"""

import pandas as pd  # type: ignore


def load_data(input_file):
    """Lea el archivo usando pandas y devuelva un DataFrame
    
    Args:
        input_file: Ruta al archivo de entrada
        
    Returns:
        DataFrame con los datos cargados desde el archivo
    """

    #
    # Esta parte es igual al taller anterior
    #
    # Leemos el archivo CSV y lo guardamos en un DataFrame
    df = pd.read_csv(input_file)
    return df


def create_key(df, n):
    """Cree una nueva columna en el DataFrame que contenga el key de la
    columna 'text'
    
    Args:
        df: DataFrame con los datos
        n: Tamaño de los n-gramas
        
    Returns:
        DataFrame con la columna 'key' añadida
    """

    # Creamos una copia del DataFrame para no modificar el original
    df = df.copy()
    # Asignamos el texto original a la columna 'key'
    df["key"] = df["raw_text"]
    # Eliminamos espacios en blanco al inicio y al final
    df["key"] = df["key"].str.strip()
    # Convertimos todo el texto a minúsculas
    df["key"] = df["key"].str.lower()
    # Eliminamos los guiones
    df["key"] = df["key"].str.replace("-", "")
    # Eliminamos todos los signos de puntuación
    df["key"] = df["key"].str.translate(
        str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    )
    # Convertimos el texto en una lista de palabras
    df["key"] = df["key"].str.split()    # ------------------------------------------------------
    # Esta es la parte especifica del algoritmo de n-gram:
    #
    # - Une el texto sin espacios en blanco (juntamos todas las palabras)
    df["key"] = df["key"].str.join("")
    #
    # - Convierte el texto a una lista de n-gramas
    # (subconjuntos de caracteres de longitud n)
    df["key"] = df["key"].map(
        lambda x: [x[t : t + n] for t in range(len(x))],
    )
    #
    # - Ordena la lista de n-gramas y remueve duplicados
    # (para tener una representación única y ordenada)
    df["key"] = df["key"].apply(lambda x: sorted(set(x)))
    #
    # - Convierte la lista de n-gramas a una cadena
    # (para obtener un solo valor que sirva como clave)
    df["key"] = df["key"].str.join("")
    # ------------------------------------------------------

    return df


def generate_cleaned_column(df):
    """Crea la columna 'cleaned' en el DataFrame
    
    Args:
        df: DataFrame con las columnas 'key' y 'raw_text'
        
    Returns:
        DataFrame con la columna 'cleaned_text' añadida
    """

    #
    # Este código es identico al anterior
    #
    # Creamos una copia del DataFrame
    keys = df.copy()
    # Ordenamos por key y texto original para consistencia
    keys = keys.sort_values(by=["key", "raw_text"], ascending=[True, True])
    # Eliminamos duplicados de keys, quedándonos con el primer texto encontrado
    keys = keys.drop_duplicates(subset="key", keep="first")
    # Creamos un diccionario que mapea cada key a su texto original
    key_dict = dict(zip(keys["key"], keys["raw_text"]))
    # Usamos el diccionario para asignar a cada key su texto "limpio"
    df["cleaned_text"] = df["key"].map(key_dict)

    return df


def save_data(df, output_file):
    """Guarda el DataFrame en un archivo
    
    Args:
        df: DataFrame con las columnas a guardar
        output_file: Ruta donde se guardará el archivo
    """
    #
    # Este código es identico al anterior
    #
    # Creamos una copia del DataFrame
    df = df.copy()
    # Seleccionamos solo las columnas que nos interesan
    df = df[["raw_text", "cleaned_text"]]
    # Guardamos el DataFrame como CSV
    df.to_csv(output_file, index=False)


def main(input_file, output_file, n=2):
    """Ejecuta la limpieza de datos
    
    Args:
        input_file: Ruta al archivo de entrada
        output_file: Ruta al archivo de salida
        n: Tamaño de los n-gramas (por defecto 2)
    """
    #
    # Este código es identico al anterior
    #
    # Cargamos los datos desde el archivo
    df = load_data(input_file)
    # Creamos la columna key usando n-gramas
    df = create_key(df, n)
    # Generamos la columna con el texto limpio
    df = generate_cleaned_column(df)
    # Guardamos una copia de prueba
    df.to_csv("files/test.csv", index=False)
    # Guardamos el resultado final
    save_data(df, output_file)


if __name__ == "__main__":
    # Este bloque se ejecuta solo cuando se ejecuta este script directamente
    # Llamamos a la función principal con los archivos de entrada y salida predeterminados
    main(
        input_file="files/input.txt",  # Archivo de entrada
        output_file="files/output.txt",  # Archivo de salida
    )