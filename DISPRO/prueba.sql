CREATE TABLE [dbo].[Estudiantes](
	[IdEstudiante] [int] IDENTITY(1,1) NOT NULL,
	[TipoDocumento] [nvarchar](50) NOT NULL,
	[NumeroDocumento] [nvarchar](50) NOT NULL,
	[NombresEstudiante] [nvarchar](100) NOT NULL,
	[ApellidosEstudiante] [nvarchar](100) NOT NULL,
	[Grado] [nvarchar](50) NOT NULL,
	[Seccion] [nvarchar](50) NOT NULL,
	[Jornada] [nvarchar](50) NOT NULL,
	[IdAcudiente] [nvarchar](20) NOT NULL,
	[NombreAcudiente] [nvarchar](100) NOT NULL,
	[ApellidoAcudiente] [nvarchar](100) NOT NULL,
	[TelefonoAcudiente] [nvarchar](15) NOT NULL,
	[CorreoAcudiente] [nvarchar](100) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[IdEstudiante] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


CREATE TABLE [dbo].[proceso_1](
	[identificacion] [int] NULL,
	[nombres] [varchar](100) NULL,
	[apellidos] [varchar](100) NULL,
	[grado] [varchar](50) NULL,
	[seccion] [varchar](50) NULL,
	[jornada] [varchar](50) NULL,
	[idacudiente] [int] NULL,
	[nombre_acudiente] [varchar](100) NULL,
	[apellidos_acudiente] [varchar](100) NULL,
	[correoacudiente] [varchar](100) NULL,
	[telefono] [int] NULL,
	[rutafoto] [varchar](255) NULL,
	[rutavideos] [varchar](255) NULL,
	[estado] [varchar](50) NULL
)

CREATE TABLE [dbo].[Usuarios](
	[IdUsuario] [int] IDENTITY(1,1) NOT NULL,
	[Rol] [nvarchar](50) NULL,
	[NombresCompletos] [nvarchar](100) NULL,
	[ApellidosUsuario] [nvarchar](100) NULL,
	[Contrasena] [nvarchar](100) NULL,
	[NumeroTelefono] [nvarchar](15) NULL,
	[CorreoElectronico] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[IdUsuario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

