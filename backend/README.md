# Prode Mundial 2026 — Backend Django

## Setup inicial

### 1. Crear y activar entorno virtual
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Crear la base de datos MySQL
```bash
mysql -u root -p < crear_db.sql
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus datos de MySQL
```

### 5. Correr migraciones
```bash
python manage.py makemigrations usuarios fixture pronosticos eliminatorias premios
python manage.py migrate
```

### 6. Crear superusuario (admin)
```bash
python manage.py createsuperuser
```

### 7. Correr el servidor
```bash
python manage.py runserver
```

El backend corre en: http://localhost:8000
El admin panel en: http://localhost:8000/admin

---

## Endpoints disponibles

### Auth
| Método | URL | Descripción |
|--------|-----|-------------|
| POST | /api/auth/registro/ | Registrar usuario |
| POST | /api/auth/login/ | Login → devuelve access + refresh token |
| POST | /api/auth/token/refresh/ | Renovar access token |
| GET/PUT | /api/auth/perfil/ | Ver/editar perfil |
| GET/POST | /api/auth/grupos/ | Listar/crear grupos privados |
| POST | /api/auth/grupos/unirse/ | Unirse con código |

### Fixture
| Método | URL | Descripción |
|--------|-----|-------------|
| GET | /api/fixture/equipos/ | Lista de equipos |
| GET | /api/fixture/jugadores/ | Lista de jugadores (filtros: equipo, posicion, sub21) |
| GET | /api/fixture/grupos/ | Fixture organizado por grupo y jornada |
| GET | /api/fixture/partidos/{id}/ | Detalle de un partido |

### Pronósticos de grupos
| Método | URL | Descripción |
|--------|-----|-------------|
| GET | /api/pronosticos/ | Mis pronósticos |
| POST | /api/pronosticos/ | Crear pronóstico |
| PUT/PATCH | /api/pronosticos/{id}/ | Editar pronóstico |
| GET | /api/pronosticos/ranking/global/ | Tabla de posiciones global |
| GET | /api/pronosticos/ranking/grupo/{id}/ | Ranking de un grupo privado |

### Eliminatorias (llaves dinámicas)
| Método | URL | Descripción |
|--------|-----|-------------|
| GET | /api/eliminatorias/bracket/ | Mi bracket generado |
| GET | /api/eliminatorias/bracket/{usuario_id}/ | Bracket de otro usuario |
| GET/POST | /api/eliminatorias/pronosticos/ | Pronósticos eliminatorias |
| PUT/PATCH | /api/eliminatorias/pronosticos/{id}/ | Editar pronóstico elim. |

### Premios individuales
| Método | URL | Descripción |
|--------|-----|-------------|
| GET/PUT | /api/premios/ | Ver/editar mis pronósticos de premios |
| GET | /api/premios/candidatos/ | Jugadores candidatos por categoría |

---

## Flujo de carga de resultados (admin)

1. Ir a http://localhost:8000/admin
2. En **Partidos**: editar el resultado (goles_local, goles_visitante, estado=FINALIZADO)
3. El sistema recalcula automáticamente los puntos de todos los pronósticos

---

## Estructura del proyecto

```
backend/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── usuarios/      ← Auth, grupos privados
│   ├── fixture/       ← Equipos, jugadores, partidos
│   ├── pronosticos/   ← Pronósticos grupos + puntuación + ranking
│   ├── eliminatorias/ ← Motor de llaves dinámicas + pronósticos elim.
│   └── premios/       ← Bota/Guante/Balón/Joven
├── requirements.txt
├── manage.py
└── .env.example
```
