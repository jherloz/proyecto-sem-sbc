from pymysql import Connect, Connection
from pymysql.cursors import DictCursor


class Database:
	m_conn: Connection
	m_cursor: DictCursor

	@staticmethod
	def open(host: str, user: str, password: str, database: str, port: int) -> None:
		Database.m_conn = Connect(
			host=host,
			user=user,
			password=password,
			database=database,
			port=port,
			autocommit=True,
			cursorclass=DictCursor,
		)
		Database.m_cursor = Database.m_conn.cursor(DictCursor)

		Database.execute(
			"CREATE TABLE IF NOT EXISTS medico("
			"id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
			"nombre VARCHAR(50) NOT NULL,"
			"apellido VARCHAR(50) NOT NULL,"
			"especialidad VARCHAR(50) NOT NULL,"
			"cedula VARCHAR(50) UNIQUE NOT NULL,"
			"activo TINYINT(1) NOT NULL DEFAULT 1"
			") CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
		)

		Database.execute(
			"CREATE TABLE IF NOT EXISTS usuario("
			"id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
			"usuario VARCHAR(50) UNIQUE NOT NULL,"
			"contrasena VARCHAR(50) NOT NULL,"
			"rol INT UNSIGNED DEFAULT NULL,"
			"activo TINYINT(1) NOT NULL DEFAULT 1,"
			"FOREIGN KEY(rol) REFERENCES medico(id)"
			") CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
		)

		Database.execute(
			"CREATE TABLE IF NOT EXISTS paciente("
			"id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
			"medico INT UNSIGNED DEFAULT NULL,"
			"nombre VARCHAR(50) NOT NULL,"
			"apellido VARCHAR(50) NOT NULL,"
			"curp VARCHAR(50) UNIQUE NOT NULL,"
			"activo TINYINT(1) NOT NULL DEFAULT 1,"
			"FOREIGN KEY(medico) REFERENCES medico(id)"
			") CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
		)

		Database.execute(
			"CREATE TABLE IF NOT EXISTS sintoma("
			"id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
			"nombre VARCHAR(50) UNIQUE NOT NULL,"
			"activo TINYINT(1) NOT NULL DEFAULT 1"
			") CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
		)

		Database.execute(
			"CREATE TABLE IF NOT EXISTS enfermedad("
			"id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
			"nombre VARCHAR(50) UNIQUE NOT NULL,"
			"activo TINYINT(1) NOT NULL DEFAULT 1"
			") CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
		)

	@staticmethod
	def close():
		Database.m_cursor.close()
		Database.m_conn.close()

	@staticmethod
	def execute(query: str, data: list | None = None):
		Database.m_cursor.execute(query, data)

	@staticmethod
	def fetchone():
		return Database.m_cursor.fetchone()

	@staticmethod
	def fetchall():
		return Database.m_cursor.fetchall()
