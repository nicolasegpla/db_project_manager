# Base de Datos – Empresas, Usuarios y Proyectos

Este repositorio contiene la **capa de base de datos** del sistema, independiente del backend (API).  
Aquí se modelan y versionan las tablas principales de:

- `empresas`
- `usuarios`
- `proyectos`

usando **PostgreSQL**, **SQLAlchemy** y **Alembic**.

> 💡 La API que consume esta base de datos vive en otro repositorio.  
> Este proyecto solo se encarga del **esquema**, **modelos** y **migraciones**.

---

## 🧱 Tecnologías

- **PostgreSQL** (motor de base de datos relacional)
- **Python 3.10+**
- **SQLAlchemy 2.x** (ORM)
- **Alembic** 1.16.x (migraciones)
- **python-dotenv** (carga de variables de entorno)

---

## 📂 Estructura del proyecto

```bash
.
├─ alembic/              # Configuración y scripts de migración
│  ├─ env.py
│  ├─ script.py.mako
│  └─ versions/          # Migraciones generadas por Alembic
├─ alembic.ini           # Configuración de Alembic (sin secretos)
├─ app/
│  ├─ __init__.py
│  ├─ db.py              # Configuración de SQLAlchemy (engine, Base, SessionLocal)
│  └─ models.py          # Modelos ORM (Empresa, Usuario, Proyecto, etc.)
├─ requirements.txt      # Dependencias del proyecto
└─ venv/                 # Entorno virtual (no se versiona)
```

> 🔐 Los secretos (URL real de conexión a la base de datos) **no** se guardan en `alembic.ini`,  
> sino en un archivo `.env` que está excluido del repositorio mediante `.gitignore`.

---

## 🧩 Modelos principales

De forma resumida, el esquema incluye:

- **Empresa (`empresas`)**
  - Datos de identificación, contacto, país/ciudad.
  - Credenciales de acceso (hash de contraseña).
  - Campos de integración con **WhatsApp Cloud API**.
  - Campos de auditoría (`creada_en`, `actualizada_en`, `activa`, etc.).

- **Usuario (`usuarios`)**
  - Pertenece a una empresa (`empresa_id` → FK a `empresas.id`).
  - Campos como nombre, email, `password_hash`, rol, estado, fecha de registro.

- **Proyecto (`proyectos`)**
  - También vinculado a una empresa (`empresa_id`).
  - Estructura pensada para asociar proyectos al contexto de cada empresa.

Las relaciones están definidas usando `relationship` de SQLAlchemy y llaves foráneas con `ON DELETE CASCADE`.

---

## ✅ Requisitos previos

En cualquier máquina donde se quiera usar este proyecto se requieren:

- **Python** 3.10 o superior.
- **PostgreSQL** 14+ (idealmente la misma versión usada en el entorno original o compatible).
- `git` instalado (para clonar el repositorio).

---

## 🚀 Instalación en una máquina nueva (paso a paso)

A continuación se describe cómo levantar este proyecto en **otra PC**, partiendo de cero.

### 1. Clonar el repositorio

```bash
git clone <URL_DE_TU_REPO>
cd <NOMBRE_DEL_REPO>
```

Ejemplo:

```bash
git clone https://github.com/tu-usuario/mi-db-empresas-usuarios.git
cd mi-db-empresas-usuarios
```

---

### 2. Crear y activar entorno virtual

En Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

En Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4. Instalar y configurar PostgreSQL en la nueva máquina

Si la nueva PC es Ubuntu/Debian:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Verifica que PostgreSQL está corriendo:

```bash
sudo service postgresql status
```

Si es necesario, inícialo:

```bash
sudo service postgresql start
```

---

### 5. Crear base de datos y usuario en PostgreSQL

Entra a PostgreSQL como usuario `postgres`:

```bash
sudo -u postgres psql
```

Dentro de `psql`, crea la base de datos y usuario para este proyecto (puedes personalizar nombres y contraseña):

```sql
CREATE DATABASE myapp_db;

CREATE USER myapp_user WITH PASSWORD 'mi_password_segura';

GRANT ALL PRIVILEGES ON DATABASE myapp_db TO myapp_user;
GRANT ALL ON SCHEMA public TO myapp_user;
```

Opcionalmente, para otorgar permisos por defecto en tablas futuras:

```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO myapp_user;
```

Salir de `psql`:

```sql
\q
```

---

### 6. Crear el archivo `.env` (no se versiona)

En la raíz del proyecto crea un archivo `.env`:

```bash
nano .env
```

Con el siguiente contenido (ajustando con tu usuario, contraseña y base):

```env
DATABASE_URL=postgresql+psycopg2://myapp_user:mi_password_segura@localhost:5432/myapp_db
```

> ⚠️ Este archivo **no** se sube a Git.  
> Asegúrate de que `.env` está incluido en `.gitignore`.

---

### 7. Verificar conexión a la base de datos (opcional)

Puedes hacer una prueba rápida ejecutando el módulo `app.db`:

```bash
python -m app.db
```

Si la configuración es correcta, no debería lanzar errores al crear el `engine`.

---

### 8. Ejecutar migraciones de Alembic

Con el entorno virtual activado y estando en la raíz del proyecto:

```bash
alembic upgrade head
```

Esto hará:

- Crear la tabla interna `alembic_version`.
- Crear todas las tablas definidas en el esquema (empresas, usuarios, proyectos, etc.).

---

### 9. Verificar tablas en PostgreSQL

Para confirmar que todo se creó correctamente:

```bash
sudo -u postgres psql
```

Dentro de `psql`:

```sql
\c myapp_db
\dt          -- lista todas las tablas
\d empresas  -- descripción de la tabla empresas
\d usuarios  -- descripción de la tabla usuarios
\d proyectos -- descripción de la tabla proyectos (si existe)
```

Salir:

```sql
\q
```

---

## 🔄 Flujo de trabajo con migraciones

Cuando quieras **modificar el esquema** (por ejemplo, agregar una columna o una nueva tabla):

1. Edita/añade tus modelos en `app/models.py`.
2. Genera una nueva migración:

   ```bash
   alembic revision --autogenerate -m "descripcion del cambio"
   ```

3. Revisa el archivo generado en `alembic/versions/`.
4. Aplica la migración:

   ```bash
   alembic upgrade head
   ```

Cualquier otra máquina que use este proyecto solo necesita:

```bash
alembic upgrade head
```

para quedar en el mismo estado de esquema.

---

## 🔐 Seguridad y buenas prácticas

- **No** guardar usuarios, contraseñas ni URLs reales de la DB en:
  - `alembic.ini`
  - código fuente (`.py`)
- Centralizar la configuración de conexión siempre en:
  - `.env` (local)
  - Variables de entorno en el servidor (producción)
- Mantener `requirements.txt` actualizado tras añadir nuevas librerías:

  ```bash
  pip freeze > requirements.txt
  ```

---

## 🧩 Integración con la API

La API (en otro repositorio) solo necesita conocer la misma `DATABASE_URL` para conectarse a esta base de datos.

Ejemplo de uso en otro proyecto:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://myapp_user:mi_password_segura@localhost:5432/myapp_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

Con esto, la API puede reutilizar el esquema y las tablas generadas por este proyecto, manteniendo una separación clara entre:

- **Capa de datos** (este repo)
- **Capa de API / negocio** (otro repo)

---

## 📌 Notas finales

- Este repositorio está pensado para ser la **fuente de verdad del esquema** de base de datos.
- Cualquier cambio estructural debe pasar por:
  1. Edición de modelos (`app/models.py`)
  2. Generación de migración Alembic
  3. Aplicación de migraciones en los entornos correspondientes

De esta forma, mantienes una base sólida y consistente para todos los servicios que dependan de esta base de datos.
