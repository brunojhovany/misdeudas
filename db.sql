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

--------------------------------------------------------------------------------------------------------------

CREATE TABLE seguridad.revoke_token(
    id_revoke_token serial primary key, 
    jti_revoke_token varchar (120)
)
CREATE SEQUENCE seguridad.id_revoke_token_seq OWNED by seguridad.revoke_token.id_revoke_token;
ALTER table seguridad.revoke_token alter COLUMN id_revoke_token set DEFAULT nextval('seguridad.id_revoke_token_seq');
--------------------------------------------------------------------------------------------------------------

create table catalogo.entidad_bancaria(
    id_entidad serial primary KEY,
    descripcion_entidad varchar(50) NOT NULL,
    id_estatus int,
    FOREIGN KEY(id_estatus) REFERENCES catalogo.estatus(id_estatus)
);

CREATE SEQUENCE catalogo.id_entidad_bancaria_seq OWNED by catalogo.entidad_bancaria.id_entidad;
ALTER TABLE catalogo.entidad_bancaria ALTER COLUMN id_entidad SET DEFAULT nextval('catalogo.id_entidad_bancaria_seq');

---------------------------------------------------------------------------------------------------------------

ALTER TABLE persona.deuda ADD COLUMN id_entidad_bancaria FOREIGN KEY (id_entidad_bancaria) REFERENCES catalogo.entidad_bancaria(id_entidad_bancaria);
alter table persona.deuda rename column id_suario to id_usuario;
alter table persona.deuda add constraint id_usuario_fk foreign key (id_usuario) references seguridad.usuario(id_usuario)


---------------------------------------------------------------------------------------------------------------
create table persona.mensualidad(
id_deuda serial not null,
id_pago int not null,
id_usuario serial not null,
monto_mensualidad money not null,
	primary key (id_deuda,id_pago),
	foreign key (id_deuda) references persona.deuda(id_deuda)
);

alter table persona.mensualidad add column fecha_pago date not null;
alter table persona.mensualidad add column id_estatus int not null;

alter table persona.mensualidad add constraint id_estatus_fk foreign key (id_estatus) references catalogo.estatus(id_estatus);