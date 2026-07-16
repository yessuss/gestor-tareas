# Gestor de Tareas

Aplicación full-stack para gestionar el ciclo de vida de tareas (pendiente → en progreso → completada), desarrollada como ejercicio técnico.

**Stack:** Flask (Python) · PostgreSQL · SQLAlchemy · Angular · Docker

## Vista general

- Tablero visual con tareas organizadas en 3 columnas según su estado.
- CRUD completo: crear, listar, actualizar estado y eliminar tareas.
- Prioridad configurable (baja / media / alta) por tarea.
- Interfaz en español, con validaciones básicas en el formulario.
- Proyecto completamente contenerizado con Docker Compose.



## Cómo ejecutar el proyecto (con Docker — recomendado)

**Requisitos:** tener [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado y corriendo.

```bash
git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
cd mi-gestor-tareas
docker compose up --build
```

Una vez que termine de construir e iniciar los contenedores:

- **Frontend:** http://localhost:4200
- **Backend / API:** http://localhost:5000/api/tasks
- **Base de datos:** PostgreSQL expuesta en el puerto 5432 de tu máquina (usuario `taskuser`, base `taskmanager`)

### Para detener el proyecto

```bash
docker compose down
```

### Para volver a levantarlo después (sin reconstruir)

```bash
docker compose up
```

### Si hiciste cambios en el código (backend o frontend)

```bash
docker compose up --build
```

## Cómo ejecutar en local sin Docker (alternativa)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # En Windows
# source venv/bin/activate  # En Mac/Linux

pip install -r requirements.txt
python app.py
```

Necesitarás una instancia de PostgreSQL corriendo (puede ser en un contenedor Docker suelto) y ajustar las variables de entorno `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` y `DB_NAME` según tu configuración.

### Frontend

```bash
cd frontend
npm install
ng serve
```

El frontend estará disponible en `http://localhost:4200` y se conecta al backend en `http://localhost:5000/api`.
