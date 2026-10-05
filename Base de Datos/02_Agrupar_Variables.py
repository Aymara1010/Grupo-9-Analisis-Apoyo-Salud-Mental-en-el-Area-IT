import sqlite3
import os

def agrupar_variables(db_path="mental_health.sqlite"):

    if not os.path.exists(db_path):
        print(f"No se encontró el archivo.")
        return

    print(f"Conectando a {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Agrupando Variables...")
    script = """
-- Genero
UPDATE Answer
SET AnswerText = 'Masculino'
WHERE QuestionID = 2
  AND TRIM(AnswerText) IN (
      'Male', 'male', 'MALE', 'Male-ish', 'something kinda male?',
      'Guy (-ish) ^_^', 'male leaning androgynous', 'ostensibly male, unsure what that really means',
      'Ostensibly Male', 'Cishet male', 'Masculine', 'masculino', 'SWM', 'Demiguy', 'I have a penis'
  );

UPDATE Answer
SET AnswerText = 'Femenino'
WHERE QuestionID = 2
  AND TRIM(AnswerText) IN (
      'Female', 'female', 'Woman-identified', 'Female-identified',
      'Female assigned at birth', 'fm', 'femmina', 'Female-ish'
  );

UPDATE Answer
SET AnswerText = 'Otro'
WHERE QuestionID = 2
  AND AnswerText NOT IN ('Masculino', 'Femenino', '-1');

-- Pais
UPDATE Answer
SET AnswerText = 'United States'
WHERE QuestionID IN (3, 50)
  AND (TRIM(AnswerText) IN ('USA', 'US', 'United States of America', 'U.S.', 'U.S.A.', 'United States'));
    """

    try:
        cursor.executescript(script)
        conn.commit()
        print("Variables correctamente.")
    except sqlite3.Error as e:
        print("Error")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    agrupar_variables("mental_health.sqlite")