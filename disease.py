from typing import Any
from database import Database


class Disease:
    def __init__(self, aidi: int = 0, name: str = "", active: int = 1):
        self.m_id = aidi
        self.m_name = name
        self.m_active = active

    # ----------------------------
    # INSERCIÓN
    # ----------------------------
    def insert(self):
        Database.execute("INSERT INTO enfermedad(nombre) VALUES(%s);", [self.m_name])
        self.m_id = Database.last_insert_id()

    def insert_with_relations(self, sign_ids: list[int], symptom_ids: list[int]):
        """Inserta la enfermedad junto con sus relaciones signo/síntoma."""
        self.insert()

        # Insertar relaciones con signos
        for sign_id in sign_ids:
            Database.execute(
                "INSERT INTO enfermedad_signo (enfermedad_id, signo_id) VALUES (%s, %s);",
                [self.m_id, sign_id],
            )

        # Insertar relaciones con síntomas
        for symptom_id in symptom_ids:
            Database.execute(
                "INSERT INTO enfermedad_sintoma (enfermedad_id, sintoma_id) VALUES (%s, %s);",
                [self.m_id, symptom_id],
            )

    # ----------------------------
    # CONSULTAS
    # ----------------------------
    def select_by_id(self, aidi: int):
        Database.execute("SELECT * FROM enfermedad WHERE id=%s;", [aidi])
        res = Database.fetchone()
        if res:
            d = dict_to_disease(res)
            self.__dict__.update(d.__dict__)

    def get_signs(self):
        """Obtiene los signos asociados a esta enfermedad."""
        Database.execute(
            "SELECT s.id, s.nombre, s.activo "
            "FROM signo s "
            "JOIN enfermedad_signo es ON s.id = es.signo_id "
            "WHERE es.enfermedad_id = %s;",
            [self.m_id],
        )
        return [dict_to_sign(r) for r in Database.fetchall()]

    def get_symptoms(self):
        """Obtiene los síntomas asociados a esta enfermedad."""
        Database.execute(
            "SELECT si.id, si.nombre, si.activo "
            "FROM sintoma si "
            "JOIN enfermedad_sintoma esi ON si.id = esi.sintoma_id "
            "WHERE esi.enfermedad_id = %s;",
            [self.m_id],
        )
        return [dict_to_symptom(r) for r in Database.fetchall()]

    # ----------------------------
    # ACTUALIZACIONES
    # ----------------------------
    def update_name(self, name: str):
        Database.execute("UPDATE enfermedad SET nombre=%s WHERE id=%s;", [name, self.m_id])
        self.m_name = name

    def update_active(self, active: int):
        Database.execute("UPDATE enfermedad SET activo=%s WHERE id=%s;", [active, self.m_id])
        self.m_active = active

    # ----------------------------
    # UTILIDAD
    # ----------------------------
    def to_list(self) -> list[Any]:
        return [str(self.m_id), self.m_name, bool(self.m_active)]


# ---------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------
def dict_to_disease(d: dict[str, Any]) -> Disease:
    return Disease(d["id"], d["nombre"], d["activo"])


def get_diseases() -> list[Disease]:
    diseases = []
    Database.execute("SELECT * FROM enfermedad;")
    for i in Database.fetchall():
        diseases.append(dict_to_disease(i))
    return diseases


def dict_to_sign(r):
    """Convierte un diccionario de signo a objeto Sign (importación diferida)."""
    from sign import Sign
    return Sign(r["id"], r["nombre"], r["activo"])


def dict_to_symptom(r):
    """Convierte un diccionario de síntoma a objeto Symptom (importación diferida)."""
    from symptom import Symptom
    return Symptom(r["id"], r["nombre"], r["activo"])
