import sqlite3
from graphlib import TopologicalSorter
import pandas as pd
from sqlalchemy import text
from conexion import engine

ORIGEN = "Grupo-9-Analisis-Apoyo-Salud-Mental-en-el-Area-IT/Base de Datos/modelo_relacional.sqlite"
EXCLUIR = {"Survey", "Question", "Answer", "sqlite_sequence"}  

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
    tablas_viejas = con.execute(text(
        "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
    )).fetchall()
    for (t_vieja,) in tablas_viejas:
        con.execute(text(f'DROP TABLE IF EXISTS public."{t_vieja}" CASCADE'))


for t in orden:
    df = pd.read_sql(f'SELECT * FROM "{t}"', sqlite)
    df.columns = df.columns.str.lower()

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
            con.execute(text(f"ALTER TABLE public.{t.lower()} ADD PRIMARY KEY ({', '.join(pk)})"))
    for t in orden:
        for fk in sqlite.execute(f'PRAGMA foreign_key_list("{t}")').fetchall():
            con.execute(text(
                f"ALTER TABLE public.{t.lower()} ADD FOREIGN KEY ({fk[3].lower()}) "
                f"REFERENCES public.{fk[2].lower()} ({fk[4].lower()})"))
print("Claves primarias y foraneas creadas")

with engine.begin() as con:
    for t in orden:
        con.execute(text(f"ALTER TABLE public.{t.lower()} ENABLE ROW LEVEL SECURITY"))
print("Seguridad activada. Listo.")