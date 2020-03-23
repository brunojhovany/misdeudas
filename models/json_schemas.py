
class Schemas:
    nueva_deuda = {
        "type": "object",
        "descripcion": {"type": "string"},
        "fecha": {"type": "date"},
        "mensualidades": {"type": "number"},
        "total": {"type": "string"},
        "id_entidad_bancaria": {"type": "numner"},
        "required": ["descripcion", "fecha", "total", "id_entidad_bancaria"]
    }
