
import sqlite3
from graphlib import TopologicalSorter
import pandas as pd
from sqlalchemy import text
from conexion import engine

ORIGEN = "Grupo-9-Analisis-Apoyo-Salud-Mental-en-el-Area-IT/bd_normalizada.sqlite"
EXCLUIR = {"Survey", "Question", "sqlite_sequence"}  

sqlite = sqlite3.connect(ORIGEN)

tablas = [r[0] for r in sqlite.execute(
    "SELECT name FROM sqlite_master WHERE type='table'") if r[0] not in EXCLUIR]
dependencias = {
    t: {fk[2] for fk in sqlite.execute(f'PRAGMA foreign_key_list("{t}")')}
    for t in tablas
}
orden = list(TopologicalSorter(dependencias).static_order())
print(len(orden), "tablas a subir")

with engine.begin() as con:
    for t in orden:
        con.execute(text(f"DROP TABLE IF EXISTS public.{t.lower()} CASCADE"))

for t in orden:
    df = pd.read_sql(f'SELECT * FROM "{t}"', sqlite)
    df.columns = df.columns.str.lower()

    
    if t == "Pregunta" and 84 not in set(df["questionid"]):
        extra = pd.read_sql(
            "SELECT questionid, questiontext FROM Question WHERE questionid = 84", sqlite)
        df = pd.concat([df, extra], ignore_index=True)
        print("Aviso: se agrego la pregunta 84 a 'pregunta' (faltaba).")

    df = df.convert_dtypes()  
    df.to_sql(t.lower(), engine, 
              schema="public",          
              if_exists="replace", 
              index=False,
              chunksize=2000, 
              method="multi") 
    print(t.lower(), len(df), "filas subidas")


with engine.begin() as con:
    for t in orden:
        cols = sqlite.execute(f'PRAGMA table_info("{t}")').fetchall()
        pk = [c[1].lower() for c in sorted((c for c in cols if c[5]), key=lambda c: c[5])]
        if pk:
            con.execute(text(f"ALTER TABLE {t.lower()} ADD PRIMARY KEY ({', '.join(pk)})"))
    for t in orden:
        for fk in sqlite.execute(f'PRAGMA foreign_key_list("{t}")').fetchall():
            con.execute(text(
                f"ALTER TABLE {t.lower()} ADD FOREIGN KEY ({fk[3].lower()}) "
                f"REFERENCES {fk[2].lower()} ({fk[4].lower()})"))
print("Claves primarias y foraneas creadas")


print("Seguridad activada. Listo.")