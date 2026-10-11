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

-- trabajo estado
INSERT OR REPLACE INTO Usuarios_Trabaja_USA (RespuestaID, Estado_USA_Empleo)
SELECT 
    iu.RespuestaID, 
    uvu.Estado_USA_Vivienda
FROM Info_Usuario iu
JOIN Usuarios_Vive_USA uvu ON uvu.RespuestaID = iu.RespuestaID
LEFT JOIN Usuarios_Trabaja_USA utu ON utu.RespuestaID = iu.RespuestaID
WHERE iu.Pais_Empleo = 80 
  AND iu.Pais_Vivienda = 80
  AND uvu.Estado_USA_Vivienda IS NOT NULL
  AND (utu.Estado_USA_Empleo IS NULL OR utu.RespuestaID IS NULL);

INSERT OR REPLACE INTO Usuarios_Trabaja_USA (RespuestaID, Estado_USA_Empleo)
SELECT 
    iu.RespuestaID,
    (
        SELECT sub.Estado_USA_Empleo
        FROM Usuarios_Trabaja_USA sub
        WHERE sub.Estado_USA_Empleo IS NOT NULL
        GROUP BY sub.Estado_USA_Empleo
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) AS Moda_Estado
FROM Info_Usuario iu
LEFT JOIN Usuarios_Trabaja_USA utu ON utu.RespuestaID = iu.RespuestaID
WHERE iu.Pais_Empleo = 80
  AND (utu.RespuestaID IS NULL OR utu.Estado_USA_Empleo IS NULL);

-- vivienda estado
INSERT OR REPLACE INTO Usuarios_Vive_USA (RespuestaID, Estado_USA_Vivienda)
SELECT 
    iu.RespuestaID, 
    utu.Estado_USA_Empleo
FROM Info_Usuario iu
JOIN Usuarios_Trabaja_USA utu ON utu.RespuestaID = iu.RespuestaID
LEFT JOIN Usuarios_Vive_USA uvu ON uvu.RespuestaID = iu.RespuestaID
WHERE iu.Pais_Empleo = 80 
  AND iu.Pais_Vivienda = 80
  AND utu.Estado_USA_Empleo IS NOT NULL
  AND (uvu.Estado_USA_Vivienda IS NULL OR uvu.RespuestaID IS NULL);

INSERT OR REPLACE INTO Usuarios_Vive_USA (RespuestaID, Estado_USA_Vivienda)
SELECT 
    iu.RespuestaID,
    (
        SELECT sub.Estado_USA_Vivienda
        FROM Usuarios_Vive_USA sub
        WHERE sub.Estado_USA_Vivienda IS NOT NULL
        GROUP BY sub.Estado_USA_Vivienda
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) AS Moda_Estado
FROM Info_Usuario iu
LEFT JOIN Usuarios_Vive_USA uvu ON uvu.RespuestaID = iu.RespuestaID
WHERE iu.Pais_Vivienda = 80
  AND (uvu.RespuestaID IS NULL OR uvu.Estado_USA_Vivienda IS NULL);

-- Experiencia Negativa
UPDATE Experiencia_Trabajo_Actual
SET Experiencia_Respuesta_Negativa_SM = (
    SELECT sub_exp.Experiencia_Respuesta_Negativa_SM
    FROM Experiencia_Trabajo_Actual sub_exp
    JOIN Info_Usuario sub_iu ON sub_iu.RespuestaID = sub_exp.RespuestaID
    WHERE sub_iu.Pais_Empleo IS iu.Pais_Empleo
      AND sub_exp.Experiencia_Respuesta_Negativa_SM IS NOT NULL
    GROUP BY sub_exp.Experiencia_Respuesta_Negativa_SM
    ORDER BY COUNT(*) DESC
    LIMIT 1
)
FROM Info_Usuario iu
WHERE Experiencia_Trabajo_Actual.RespuestaID = iu.RespuestaID
  AND Experiencia_Trabajo_Actual.Experiencia_Respuesta_Negativa_SM IS NULL;

-- Beneficio
UPDATE Beneficios_Trabajo_Actual
SET Beneficio = (
    SELECT sub.Beneficio
    FROM Beneficios_Trabajo_Actual sub
    WHERE sub.Acceso_Servicios IS Beneficios_Trabajo_Actual.Acceso_Servicios
      AND sub.Conocimiento_Recursos_Externos IS Beneficios_Trabajo_Actual.Conocimiento_Recursos_Externos
      AND sub.Beneficio IS NOT NULL
    GROUP BY sub.Beneficio
    ORDER BY COUNT(*) DESC
    LIMIT 1
)
WHERE Beneficio IS NULL;
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