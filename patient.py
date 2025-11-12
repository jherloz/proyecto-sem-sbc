from typing import Any
from database import Database


class Patient:
    def __init__(
        self,
        id: int = 0,
        medico: int | None = None,
        nombre: str = "",
        apellido: str = "",
        curp: str = "",
        activo: int = 1,
    ):
        self.m_id: int = id
        self.m_medico: int | None = medico
        self.m_nombre: str = nombre
        self.m_apellido: str = apellido
        self.m_curp: str = curp
        self.m_activo: int = activo

    # ----------------------------
    # INSERTAR NUEVO PACIENTE
    # ----------------------------
    def insert(self):
        Database.execute(
            "INSERT INTO paciente (medico, nombre, apellido, curp, activo) VALUES (%s, %s, %s, %s, %s);",
            [self.m_medico, self.m_nombre, self.m_apellido, self.m_curp, self.m_activo],
        )
        self.m_id = Database.last_insert_id()

    # ----------------------------
    # ACTUALIZAR CAMPOS
    # ----------------------------
    def update_name(self, nombre: str):
        Database.execute(
            "UPDATE paciente SET nombre=%s WHERE id=%s;", [nombre, self.m_id]
        )
        self.m_nombre = nombre

    def update_lastname(self, apellido: str):
        Database.execute(
            "UPDATE paciente SET apellido=%s WHERE id=%s;", [apellido, self.m_id]
        )
        self.m_apellido = apellido

    def update_curp(self, curp: str):
        Database.execute(
            "UPDATE paciente SET curp=%s WHERE id=%s;", [curp, self.m_id]
        )
        self.m_curp = curp

    def update_active(self, activo: int):
        Database.execute(
            "UPDATE paciente SET activo=%s WHERE id=%s;", [activo, self.m_id]
        )
        self.m_activo = activo

    # ----------------------------
    # CONSULTAS
    # ----------------------------
    @staticmethod
    def get_all() -> list["Patient"]:
        Database.execute("SELECT * FROM paciente;")
        results = Database.fetchall()
        return [dict_to_patient(r) for r in results]

    @staticmethod
    def get_by_id(id_: int) -> "Patient | None":
        Database.execute("SELECT * FROM paciente WHERE id=%s;", [id_])
        r = Database.fetchone()
        return dict_to_patient(r) if r else None

    @staticmethod
    def get_by_medic(medic_id: int) -> list["Patient"]:
        Database.execute("SELECT * FROM paciente WHERE medico=%s;", [medic_id])
        results = Database.fetchall()
        return [dict_to_patient(r) for r in results]

    # ----------------------------
    # UTILIDAD
    # ----------------------------
    def get_full_name(self) -> str:
        return f"{self.m_nombre} {self.m_apellido}".strip()

    def to_list(self) -> list[Any]:
        return [
            str(self.m_id),
            self.get_full_name(),
            self.m_curp,
            str(self.m_medico) if self.m_medico is not None else "",
            bool(self.m_activo),
        ]

    def __bool__(self):
        return bool(self.m_nombre and self.m_apellido and self.m_curp)


# ---------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------
def dict_to_patient(row: dict[str, Any]) -> Patient:
    return Patient(
        id=row["id"],
        medico=row.get("medico"),
        nombre=row["nombre"],
        apellido=row["apellido"],
        curp=row["curp"],
        activo=row["activo"],
    )


def get_patients() -> list[Patient]:
    Database.execute("SELECT * FROM paciente;")
    results = Database.fetchall()
    return [dict_to_patient(r) for r in results]


def get_patients_by_medic(medic_id: int) -> list[Patient]:
    Database.execute("SELECT * FROM paciente WHERE medico=%s;", [medic_id])
    results = Database.fetchall()
    return [dict_to_patient(r) for r in results]
