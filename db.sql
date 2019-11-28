-- tabla de usuarios
CREATE SCHEMA seguridad;


CREATE TABLE seguridad.usuario(
id_usuario SERIAL PRIMARY KEY,
nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
password_usuario VARCHAR (300) NOT NULL,
salt_usuario VARCHAR (50));
 
CREATE SEQUENCE seguridad.id_usuario_seq owned by seguridad.usuario.id_usuario;
alter table seguridad.usuario alter column id_usuario set default nextval('seguridad.id_usuario_seq');

----------------------------------------------------------------------------------------------------------

create schema persona;
create schema catalogo;

create table catalogo.estatus(
id_estatus int primary key,
descripcion_estatus varchar(80) not null);

insert into catalogo.estatus values(1,'Activo');
insert into catalogo.estatus values(2,'Cancelado');
insert into catalogo.estatus values(3,'Concluido');


create table persona.deuda(
id_deuda serial primary key,
descripcion_deuda varchar(80) NOT NULL,
fecha_deudad timestamp default (current_timestamp),
fecha_deudad_fin date,
mensualidades bit,
id_estatus int,
foreign key (id_estatus) references catalogo.estatus (id_estatus)
);


CREATE SEQUENCE persona.id_deuda_seq owned by persona.deuda.id_deuda;
alter table persona.deuda alter column id_deuda set default nextval('persona.id_deuda_seq');