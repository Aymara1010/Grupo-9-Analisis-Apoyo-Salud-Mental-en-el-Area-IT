import os
import sqlite3
import Modelo_Relacional as mr

bd_original = "mental_health.sqlite"
bd_relacional = "modelo_relacional.sqlite"

if __name__ == "__main__":
    conexion = mr.clonar_datos_filtrados(bd_original, bd_relacional)