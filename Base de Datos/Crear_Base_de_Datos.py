import Modelo_Relacional as mr
import Insertar_Datos_Modelo_Relacional as id

bd_original = "mental_health.sqlite"
bd_relacional = "modelo_relacional.sqlite"

if __name__ == "__main__":
    conexion = mr.clonar_datos_filtrados(bd_original, bd_relacional)
    if conexion:
        mr.limpiar_respuestas(conexion, bd_relacional)
    normalizar = mr.normalizar_base_de_datos(bd_relacional)
    preguntas = mr.insertar_preguntas(bd_relacional)
    
if __name__ == "__main__":
    catalogos = id.migrar_catalogos_y_centro()
    demofrafia = id.migrar_demografia_y_trabajo()
    estado = id.migrar_estado_y_trabajo_actual()
    anterior = id.migrar_social_y_trabajo_anterior()
    limpieza = id.limpieza()