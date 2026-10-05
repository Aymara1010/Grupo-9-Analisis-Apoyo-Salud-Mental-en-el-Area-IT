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
 
-- Condiciones

UPDATE Answer
SET AnswerText = 'Trastornos del Estado de Ánimo'
WHERE QuestionID = 115 
  AND (AnswerText LIKE '%Mood Disorder%' 
       OR AnswerText = 'Depression' 
       OR AnswerText LIKE '%Seasonal Affective%');

UPDATE Answer
SET AnswerText = 'Trastornos de Ansiedad'
WHERE QuestionID = 115 
  AND (AnswerText LIKE '%Anxiety Disorder%' 
       OR AnswerText LIKE '%post-partum%' 
       OR AnswerText LIKE '%Social Anxiety%');

UPDATE Answer
SET AnswerText = 'Trastorno por Déficit de Atención e Hiperactividad (TDAH)'
WHERE QuestionID = 115 
  AND (AnswerText LIKE '%Attention Deficit%' 
       OR AnswerText LIKE 'ADD%' 
       OR AnswerText LIKE '%ADHD%');

UPDATE Answer
SET AnswerText = 'Trastornos Relacionados con Traumas y Estrés'
WHERE QuestionID = 115 
  AND (AnswerText LIKE '%Post-traumatic%' 
       OR AnswerText LIKE '%Stress Response%' 
       OR AnswerText LIKE '%PTSD%');

UPDATE Answer
SET AnswerText = 'Trastornos Adictivos y por Uso de Sustancias'
WHERE QuestionID = 115 
  AND (AnswerText LIKE '%Addictive Disorder%' 
       OR AnswerText LIKE '%Substance Use%' 
       OR AnswerText LIKE '%Sexual addiction%');

UPDATE Answer
SET AnswerText = 'Trastornos de la Personalidad'
WHERE QuestionID = 115 
  AND (AnswerText LIKE '%Personality Disorder%' 
       OR AnswerText LIKE '%Schizotypal%');

UPDATE Answer
SET AnswerText = 'Trastorno Obsesivo-Compulsivo (TOC)'
WHERE QuestionID = 115 
  AND AnswerText LIKE '%Obsessive-Compulsive%';

UPDATE Answer
SET AnswerText = 'Trastornos de la Conducta Alimentaria'
WHERE QuestionID = 115 
  AND AnswerText LIKE '%Eating Disorder%';

UPDATE Answer
SET AnswerText = 'Trastornos Disociativos'
WHERE QuestionID = 115 
  AND AnswerText LIKE '%Dissociative%';

UPDATE Answer
SET AnswerText = 'Espectro de la Esquizofrenia y Otros Trastornos Psicóticos'
WHERE QuestionID = 115 
  AND (AnswerText LIKE '%Psychotic Disorder%' 
       OR AnswerText LIKE '%Schizo%');

UPDATE Answer
SET AnswerText = 'Trastorno del Espectro Autista (TEA)'
WHERE QuestionID = 115 
  AND (AnswerText LIKE '%Autism%' 
       OR AnswerText LIKE '%Asperger%' 
       OR AnswerText LIKE '%PDD-NOS%' 
       OR AnswerText LIKE '%Pervasive Development%');

UPDATE Answer
SET AnswerText = 'Disforia de Género / Identidad de Género'
WHERE QuestionID = 115 
  AND (AnswerText LIKE '%Gender Dysphoria%' 
       OR AnswerText LIKE '%Gender Identity%' 
       OR AnswerText LIKE '%Transgender%');

UPDATE Answer
SET AnswerText = 'Otros'
WHERE QuestionID = 115 
  AND (AnswerText LIKE '%Intimate Disorder%' 
       OR AnswerText LIKE '%Suicidal Ideation%' 
       OR AnswerText LIKE '%all hurt%' 
       OR AnswerText LIKE '%Burn out%' 
       OR AnswerText LIKE '%Burnout%' 
       OR AnswerText LIKE '%Brain Injury%' 
       OR AnswerText LIKE '%Tinnitus%' 
       OR AnswerText LIKE '%Sleeping Disorder%');

-- I don't know

UPDATE Answer
SET AnswerText = 'I don''t know'
WHERE QuestionID IN (11, 10, 91)
  AND (TRIM(AnswerText) IN ('Don''t know', 'I don''t know'));  
    """

    try:
        cursor.executescript(script)
        conn.commit()
        print("Variables correctamente.")
    except sqlite3.Error as e:
        print(f"Error {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    agrupar_variables("mental_health.sqlite")