-- CREATE SCHEMA Seguridad;

-- CREATE SEQUENCE Seguridad.Usuario_Id_Usuario;

CREATE TABLE IF NOT EXISTS Seguridad.Usuario(
Id_Usuario SERIAL PRIMARY KEY,
Nombre_Usuario VARCHAR(50) UNIQUE NOT NULL,
Password_Usuario VARCHAR (300) NOT NULL,
Salt_Usuario VARCHAR (50));
 
 ALTER SEQUENCE Seguridad.Usuario_Id_Usuario
 OWNED BY Seguridad.Usuario;
