from typing import Any
from database import Database


class User:
	# Almacenará datos de ambas tablas
	def __init__(
		self,
		aidi: int = 0,
		user: str = "",
		password: str = "",
		role: int | None = None,
		active: int = 1,
		# Campos opcionales de médico
		nombre: str | None = None,
		apellido: str | None = None,
		especialidad: str | None = None,
		cedula: str | None = None,
	):
		# Campos de 'usuario'
		self.m_id: int = aidi
		self.m_user: str = user
		self.m_password: str = password
		self.m_role: int | None = role
		self.m_active: int = active

		# Campos de 'medico'
		self.m_nombre: str | None = nombre
		self.m_apellido: str | None = apellido
		self.m_especialidad: str | None = especialidad
		self.m_cedula: str | None = cedula

	def insert(self):
		Database.execute(
			"INSERT INTO usuario(usuario, contrasena, rol) VALUES(%s, %s, %s);",
			[self.m_user, self.m_password, self.m_role],
		)

	def select_by_id(self, aidi: int):
		"""Obtiene los datos fusionados (JOIN) para este usuario."""
		query = (
			"SELECT u.id, u.usuario, u.contrasena, u.rol, u.activo, "
			"m.nombre, m.apellido, m.especialidad, m.cedula "
			"FROM usuario u "
			"LEFT JOIN medico m ON u.rol = m.id "
			"WHERE u.id = %s;"
		)
		Database.execute(query, [aidi])
		res = Database.fetchone()

		if res:
			user = dict_to_user(res)
			self.__dict__.update(user.__dict__)

	def to_list(self) -> list[Any]:
		"""Devuelve una lista plana para el DataViewListCtrl."""
		rol_str = "Médico" if self.m_role is not None else "Admin"
		
		return [
			str(self.m_id),
			self.m_user,
			"****" if self.m_id != 1 else self.m_password, 
			rol_str,
			self.m_nombre if self.m_nombre is not None else "",
			self.m_apellido if self.m_apellido is not None else "",
			self.m_especialidad if self.m_especialidad is not None else "",
			self.m_cedula if self.m_cedula is not None else "",
			bool(self.m_active),
		]

	#Métodos de Actualización (Tabla 'usuario')
	def update_user(self, user: str):
		Database.execute(
			"UPDATE usuario SET usuario=%s WHERE id=%s;", [user, self.m_id]
		)
		self.m_user = user

	def update_password(self, password: str):
		Database.execute(
			"UPDATE usuario SET contrasena=%s WHERE id=%s;", [password, self.m_id]
		)
		self.m_password = password

	def update_active(self, active: int):
		Database.execute(
			"UPDATE usuario SET activo=%s WHERE id=%s;", [active, self.m_id]
		)
		if self.m_role:
			Database.execute(
				"UPDATE medico SET activo=%s WHERE id=%s;", [active, self.m_role]
			)
		self.m_active = active

	#Métodos de Actualización (Tabla 'medico')
	def update_medic_name(self, name: str):
		if self.m_role:
			Database.execute(
				"UPDATE medico SET nombre=%s WHERE id=%s;", [name, self.m_role]
			)
			self.m_nombre = name

	def update_medic_lastname(self, lastname: str):
		if self.m_role:
			Database.execute(
				"UPDATE medico SET apellido=%s WHERE id=%s;", [lastname, self.m_role]
			)
			self.m_apellido = lastname

	def update_medic_specialty(self, specialty: str):
		if self.m_role:
			Database.execute(
				"UPDATE medico SET especialidad=%s WHERE id=%s;", [specialty, self.m_role]
			)
			self.m_especialidad = specialty

	def update_medic_certificate(self, certificate: str):
		if self.m_role:
			Database.execute(
				"UPDATE medico SET cedula=%s WHERE id=%s;", [certificate, self.m_role]
			)
			self.m_cedula = certificate

	# Lógica de Roles
	def is_admin(self) -> bool:
		return self.m_role is None or self.m_role == 0

	def is_medic(self) -> bool:
		return self.m_role is not None and self.m_role > 0

	def __bool__(self):
		if self.m_user and self.m_password:
			return True
		return False


def count_users() -> int:
	Database.execute("SELECT COUNT(*) AS n FROM usuario;")
	res = Database.fetchone()
	return int(res["n"]) if res else 0


def dict_to_user(user: dict[str, Any]):
	return User(
		user["id"],
		user["usuario"],
		user["contrasena"],
		user["rol"],
		user["activo"],
		user.get("nombre"),
		user.get("apellido"),
		user.get("especialidad"),
		user.get("cedula"),
	)


def get_users() -> list[User]:
	"""Obtiene todos los usuarios y sus datos de médico (si los tienen)."""
	users: list[User] = []
	query = (
		"SELECT u.id, u.usuario, u.contrasena, u.rol, u.activo, "
		"m.nombre, m.apellido, m.especialidad, m.cedula "
		"FROM usuario u "
		"LEFT JOIN medico m ON u.rol = m.id;"
	)
	Database.execute(query)

	for i in Database.fetchall():
		users.append(dict_to_user(i))
	return users


def log_in(user: str, password: str):
	Database.execute(
		"SELECT * FROM usuario WHERE usuario=%s AND contrasena=%s AND activo = 1;",
		[user, password],
	)
	res = Database.fetchone()
	return dict_to_user(res) if res else None