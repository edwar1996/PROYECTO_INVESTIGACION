--usuarioss

CREATE TABLE Usuarios (
    ID INT PRIMARY KEY IDENTITY(1,1),
    NombresCompletos NVARCHAR(100),
    ApellidosUsuario NVARCHAR(100),
    CorreoElectronico NVARCHAR(100),
    Contrasena NVARCHAR(100),
    NumeroTelefono NVARCHAR(15),
    usuario Nvarcahr(255),
    Rol NVARCHAR(50),
    RutaFirma TEXT  -- Campo que almacena el rol, por ejemplo, 'Docente' o 'Acudiente'
);


--estudiantes
CREATE TABLE Estudiantes (
    IdEstudiante INT PRIMARY KEY IDENTITY(1,1),
    TipoDocumento NVARCHAR(50) NOT NULL,  -- Nuevo campo para el tipo de documento
    NumeroDocumento NVARCHAR(50) NOT NULL, -- Nuevo campo para el número de documento
    NombresEstudiante NVARCHAR(100) NOT NULL,
    ApellidosEstudiante NVARCHAR(100) NOT NULL,
    Grado NVARCHAR(50) NOT NULL,
    Seccion NVARCHAR(50) NOT NULL,
    Jornada NVARCHAR(50) NOT NULL,
    IdAcudiente NVARCHAR(20) NOT NULL,
    NombreAcudiente NVARCHAR(100) NOT NULL,
    ApellidoAcudiente NVARCHAR(100) NOT NULL,
    TelefonoAcudiente NVARCHAR(15) NOT NULL,
    CorreoAcudiente NVARCHAR(100) NOT NULL
);


CREATE TABLE proceso_1 (
    identificacion INT,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    grado VARCHAR(50),
    seccion VARCHAR(50),
    jornada VARCHAR(50),
    idacudiente INT,
    nombre_acudiente VARCHAR(100),
    apellidos_acudiente VARCHAR(100),
    correoacudiente VARCHAR(100),
	telefono INT,
    rutafoto VARCHAR(255),
    rutavideos VARCHAR(255),
    estado VARCHAR(50),
    falta_cometida VARCHAR(255),
    descargos VARCHAR(255),
    compromiso VARCHAR(255);
);

CREATE TABLE proceso_2 (
    id INT,
    identificacion NVARCHAR(250)  NULL,
    nombres NVARCHAR(250)  NULL,
    apellidos  NVARCHAR(250)  NULL,
    grado NVARCHAR(250)  NULL,
    seccion NVARCHAR(250)  NULL,
    jornada NVARCHAR(250)  NULL,
    idacudiente NVARCHAR(250)  NULL,
    nombre_acudiente NVARCHAR(250)  NULL,
    apellidos_acudiente NVARCHAR(250)  NULL,
    correoacudiente NVARCHAR(250)  NULL,
    telefono NVARCHAR(250)  NULL,
    estado NVARCHAR (250) DEFAULT 'Activo',
    falta_cometida NVARCHAR(250)  NULL,
    rutafoto TEXT,
    mediador1 NVARCHAR(250)  NULL,
    mediador2 NVARCHAR(250)  NULL
);

--agregar cmapo de usuaruos 
ALTER TABLE Usuarios ADD RutaFirma TEXT;
