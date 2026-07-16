# Gestor de Tareas

Aplicación full-stack para gestionar el ciclo de vida de tareas (pendiente → en progreso → completada), desarrollada como ejercicio técnico.

**Stack:** Flask (Python) · PostgreSQL · SQLAlchemy · Angular · Docker

## Vista general

- Tablero visual con tareas organizadas en 3 columnas según su estado.
- CRUD completo: crear, listar, actualizar estado y eliminar tareas.
- Prioridad configurable (baja / media / alta) por tarea.
- Interfaz en español, con validaciones básicas en el formulario.
- Proyecto completamente contenerizado con Docker Compose.

## Estructura del proyecto

```
mi-gestor-tareas/
├── backend/              # API REST en Flask
│   ├── app.py             # Modelo, rutas y configuración de la app
│   ├── requirements.txt   # Dependencias de Python
│   └── Dockerfile
├── frontend/             # Aplicación Angular
│   ├── src/app/
│   │   ├── models/task.model.ts
│   │   ├── services/task.service.ts
│   │   ├── app.component.ts
│   │   ├── app.component.html
│   │   └── app.component.css
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Modelo de datos (Task)

| Campo         | Tipo                                       | Notas                          |
|---------------|---------------------------------------------|----------------------------------|
| id            | Integer                                     | PK autoincremental               |
| title         | String                                       | Obligatorio                      |
| description   | Text                                         | Opcional                         |
| priority      | Enum: low / medium / high                   | Por defecto: medium              |
| status        | Enum: pending / in_progress / completed     | Por defecto: pending              |
| created_at    | DateTime                                    | Se asigna automáticamente        |

## Endpoints de la API

| Método | Ruta                          | Descripción                          |
|--------|-------------------------------|----------------------------------------|
| GET    | /api/tasks                    | Lista todas las tareas                |
| GET    | /api/tasks/:id                 | Obtiene una tarea específica          |
| POST   | /api/tasks                    | Crea una tarea nueva                  |
| PUT    | /api/tasks/:id                 | Actualiza título/descripción de una tarea |
| PATCH  | /api/tasks/:id/status           | Cambia el estado de una tarea          |
| DELETE | /api/tasks/:id                 | Elimina una tarea                     |

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
- **Base de datos:** PostgreSQL expuesta en el puerto 5433 de tu máquina (usuario `taskuser`, base `taskmanager`)

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

## Funcionalidades implementadas

- [x] CRUD completo de tareas
- [x] Tablero visual con columnas por estado (Pendiente / En progreso / Completada)
- [x] Cambio de estado mediante botones ("Iniciar", "Completar")
- [x] Prioridad con selector (con placeholder obligatorio)
- [x] Interfaz completamente en español
- [x] Validaciones básicas (título obligatorio, prioridad obligatoria)
- [x] Contenerización completa con Docker Compose (base de datos + backend + frontend)

## Notas técnicas

- El backend usa variables de entorno para la conexión a la base de datos, permitiendo que el mismo código funcione tanto en local como dentro de Docker (usando el nombre del servicio `db` como host cuando corre en Docker Compose).
- El frontend usa Angular con arquitectura basada en módulos (`NgModule`).
- Los valores internos de estado y prioridad se manejan en inglés (`pending`, `high`, etc.) por convención de código, mientras que la interfaz visual los traduce al español mediante diccionarios de traducción en el componente.
