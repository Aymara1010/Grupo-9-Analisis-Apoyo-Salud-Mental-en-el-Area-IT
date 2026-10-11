import sqlite3
import os

def limpiar_base_de_datos(db_path="mental_health.sqlite"):

    if not os.path.exists(db_path):
        print(f"No se encontró el archivo.")
        return

    print(f"Conectando a {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Limpiando Variables...")
    script = """
-- Freelance

UPDATE Trabajo_Usuario
SET Freelance = CASE WHEN Num_Empleados ='1-5' THEN 1 ELSE 0 END
WHERE Freelance IS NULL

-- Pais Empleo

UPDATE Info_Usuario
SET Pais_Empleo = Pais_Vivienda 
WHERE Pais_Empleo  IS NULL

-- Pais Vivienda

UPDATE Info_Usuario
SET Pais_Vivienda = Pais_Empleo 
WHERE Pais_Vivienda  IS NULL

-- Raza
UPDATE Info_Usuario
SET Raza_Etnia = 'No Declarado' 
WHERE Raza_Etnia   IS NULL

-- Genero
UPDATE Info_Usuario
SET Genero = 'No Declarado' 
WHERE Genero   IS NULL

-- edad
UPDATE Info_Usuario
SET Edad = ROUND((SELECT AVG(b.Edad)
                  FROM Info_Usuario b
                  WHERE b.Genero = Info_Usuario.Genero 
                  AND Info_Usuario.Pais_Vivienda = b.Pais_Vivienda 
                  AND b.Edad IS NOT NULL), 2)
WHERE Edad IS NULL
    """

    try:
        cursor.executescript(script)
        conn.commit()
        print("Variables Limpiadas correctamente.")
    except sqlite3.Error as e:
        print("Error de creación")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    limpiar_base_de_datos("mental_health.sqlite")