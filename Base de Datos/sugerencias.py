import re
import duckdb
import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi

DICCIONARIOS = {
    'negativa': [
        'fired', 'dismissed', 'toxic', 'burnout', 'anxiety', 'panic', 'depression',
        'depressed', 'hostile', 'punished', 'ridiculed', 'mocked', 'ignored',
        'isolated', 'stress', 'stigma', 'afraid', 'fear', 'worst', 'harassment',
        'unsupportive', 'bad', 'crying', 'terrible', 'discriminated', 'overtime',
        'pressure', 'retaliation', 'shame', 'guilt', 'burden'
    ],
    'positiva': [
        'supportive', 'understanding', 'support', 'helpful', 'empathy', 'caring',
        'great', 'good', 'accepted', 'comforting', 'encouraging', 'welcomed',
        'listened', 'listening', 'compassion', 'open', 'accommodating', 'safe',
        'appreciate', 'helped', 'improved', 'kind', 'positive', 'receptive'
    ],
    'neutra': [
        'talked', 'discussed', 'mentioned', 'standard', 'conversation', 'normal',
        'policy', 'process', 'procedure', 'meeting', 'noted', 'matter-of-fact',
        'casual', 'formal', 'routine', 'told', 'sharing', 'neither'
    ]
}

def clasificar_con_bm25(textos):
    corpus = [
        re.findall(r'\b[a-zA-Z]{3,}\b', str(t).lower())
        if pd.notna(t) and str(t).strip() else []
        for t in textos
    ]
    validos = [i for i, tokens in enumerate(corpus) if len(tokens) > 0]
    sub_corpus = [corpus[i] for i in validos]

    ids = [None] * len(textos)
    if not sub_corpus:
        return ids

    bm25 = BM25Okapi(sub_corpus)
    scores_neg = bm25.get_scores(DICCIONARIOS['negativa'])
    scores_pos = bm25.get_scores(DICCIONARIOS['positiva'])
    scores_neu = bm25.get_scores(DICCIONARIOS['neutra'])

    for local_idx, orig_idx in enumerate(validos):
        s_neg = scores_neg[local_idx]
        s_pos = scores_pos[local_idx]
        s_neu = scores_neu[local_idx]
        max_score = max(s_neg, s_pos, s_neu)

        if max_score == 0:
            ids[orig_idx] = 3  # Neutra
        elif s_neg >= s_pos and s_neg >= s_neu:
            ids[orig_idx] = 1 if s_neg >= 3.5 else 2  # Muy Alta vs Alta
        elif s_pos > s_neg and s_pos >= s_neu:
            ids[orig_idx] = 5 if s_pos >= 3.5 else 4  # Muy Alta vs Alta
        else:
            ids[orig_idx] = 3  # Neutra

    return ids


def actualizar_emociones_bd(duckdb_path="mental_health_dimensional.duckdb"):
    con = duckdb.connect(duckdb_path)
    try:

        df = con.execute("""
            SELECT 
                RespuestaID,
                Descripcion_Conversacion_Companeros_Sobre_SM AS t1,
                Descripcion_Conversacion_Sobre_Companero_SM AS t2
            FROM Fact_Respuesta_Encuestado;
        """).fetchdf()

        df['id_1'] = clasificar_con_bm25(df['t1'])
        df['id_2'] = clasificar_con_bm25(df['t2'])

        actualizar_df = df[['RespuestaID', 'id_1', 'id_2']]
        con.register('actualizar_df', actualizar_df)

        con.execute("""
            UPDATE Fact_Respuesta_Encuestado
            SET 
                Emocion_Conversacion_Companeros = actualizar_df.id_1,
                Emocion_Conversacion_Sobre_Companero = actualizar_df.id_2
            FROM actualizar_df
            WHERE Fact_Respuesta_Encuestado.RespuestaID = actualizar_df.RespuestaID;
        """)
        print("Emociones insertadas correctamente en Fact_Respuesta_Encuestado.")
    finally:
        con.close()

# Diccionarios temáticos derivados del vocabulario real de las sugerencias
DICCIONARIOS_SUGERENCIAS = {
    1: [  # Jornada, Carga Laboral y Burnout
        'burnout', 'overwork', 'hours', 'overtime', 'crunch', 'deadlines', 'workload',
        'balance', 'pressure', 'slog', 'marathon', 'unplug', 'vacation', 'pto',
        'remote', 'flexible', 'flexibility', 'schedules', 'disconnect', 'stressful',
        'sustainable', 'pace', 'factory', 'tasks', 'expectations', 'boundaries'
    ],
    2: [  # Desestigmatización y Cultura Abierta
        'stigma', 'destigmatize', 'open', 'openly', 'talk', 'talking', 'conversation',
        'culture', 'bro', 'masculinity', 'toxic', 'alcohol', 'drinking', 'meetup',
        'empathy', 'compassion', 'vulnerability', 'safe', 'judgment', 'taboo',
        'macho', 'acceptance', 'normal', 'normalize', 'shame', 'fear', 'kind'
    ],
    3: [  # Seguros, Beneficios y Cobertura
        'insurance', 'benefits', 'coverage', 'therapy', 'therapist', 'psychiatrist',
        'counseling', 'copay', 'copays', 'deductible', 'hsa', 'fsa', 'cost', 'pay',
        'sessions', 'healthcare', 'parity', 'prescriptions', 'providers', 'network'
    ],
    4: [  # Días de Salud Mental y Licencias
        'leave', 'sick', 'days', 'day', 'off', 'medical', 'absence', 'recharge',
        'recover', 'break', 'breaks', 'wellness', 'allowances', 'permission'
    ],
    5: [  # Capacitación a Líderes y RRHH
        'manager', 'managers', 'leadership', 'training', 'train', 'supervisor',
        'coaching', 'hr', 'management', 'boss', 'counselor', 'interpersonal',
        'leaders', 'supervisors', 'skills', 'reprisal', 'firing', 'fire'
    ],
    6: [  # Educación, Difusión y Espacio Físico
        'education', 'educate', 'awareness', 'information', 'resources', 'handbook',
        'seminars', 'workshops', 'programs', 'disorders', 'signs', 'symptoms',
        'office', 'plans', 'distractions', 'noise', 'quiet', 'rooms', 'light'
    ]
}

def tokenizar(texto):
    if pd.isna(texto) or not str(texto).strip():
        return []
    t = str(texto).lower()
    t = t.replace('over work', 'overwork').replace('health care', 'healthcare').replace('open office', 'office')
    return re.findall(r'\b[a-zA-Z]{3,}\b', t)

def clasificar_sugerencias(textos):
    corpus = [tokenizar(t) for t in textos]
    validos = [i for i, t in enumerate(corpus) if len(t) > 0]
    sub_corpus = [corpus[i] for i in validos]

    ids_resultado = [None] * len(textos)
    if not sub_corpus:
        return ids_resultado

    bm25 = BM25Okapi(sub_corpus)
    vocabulario = set(word for doc in sub_corpus for word in doc)

    scores_por_cat = {}
    for cat_id, palabras in DICCIONARIOS_SUGERENCIAS.items():
        palabras_presentes = [w for w in palabras if w in vocabulario]
        if palabras_presentes:
            scores_matriz = np.array([bm25.get_scores([w]) for w in palabras_presentes])
            scores_por_cat[cat_id] = scores_matriz.sum(axis=0)
        else:
            scores_por_cat[cat_id] = np.zeros(len(sub_corpus))

    for local_idx, orig_idx in enumerate(validos):
        puntajes = {cat_id: scores_por_cat[cat_id][local_idx] for cat_id in DICCIONARIOS_SUGERENCIAS}
        mejor_cat = max(puntajes, key=puntajes.get)


        if puntajes[mejor_cat] > 0:
            ids_resultado[orig_idx] = int(mejor_cat)
        else:
            ids_resultado[orig_idx] = 7

    return ids_resultado

def categorizar_base_datos(duckdb_path="mental_health_dimensional.duckdb"):
    con = duckdb.connect(duckdb_path)
    try:
        df = con.execute("""
            SELECT 
                RespuestaID, 
                Sugerencias_Mejora_SM_Industria AS sugerencia
            FROM Fact_Respuesta_Encuestado;
        """).fetchdf()

        df['cat_id'] = clasificar_sugerencias(df['sugerencia'])

        datos_update = df[['RespuestaID', 'cat_id']].dropna(subset=['cat_id']).copy()
        datos_update['cat_id'] = datos_update['cat_id'].astype(int)

        if len(datos_update) > 0:
            con.register('df_actualizacion', datos_update)
            con.execute("""
                UPDATE Fact_Respuesta_Encuestado
                SET Categoria_Sugerencia_ID = df_actualizacion.cat_id
                FROM df_actualizacion
                WHERE Fact_Respuesta_Encuestado.RespuestaID = df_actualizacion.RespuestaID;
            """)
            print(f"Registros actualizados exitosamente: {len(datos_update)}")
    finally:
        con.close()

