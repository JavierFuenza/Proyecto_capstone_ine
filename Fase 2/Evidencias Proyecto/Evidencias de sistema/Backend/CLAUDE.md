# CLAUDE.md - Observatorio Ambiental Backend

## Proyecto
Backend para capstone - Observatorio ambiental construido con FastAPI + Docker.

## Estructura del Proyecto
```
backend/
├── app/
│   ├── core/                    # Configuración centralizada
│   │   ├── config.py           # Settings con Pydantic
│   │   ├── database.py         # Configuración DB mejorada
│   │   └── dependencies.py     # Dependencias comunes
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── agua.py             # Modelos de agua
│   │   └── aire.py             # Modelos de aire
│   ├── schemas/                 # Schemas Pydantic
│   │   ├── agua.py             # Validación agua
│   │   ├── aire.py             # Validación aire
│   │   └── common.py           # Schemas comunes
│   ├── routers/                 # Endpoints organizados
│   │   ├── public/             # APIs públicas
│   │   │   └── general.py      # Health & Info
│   │   └── private/            # APIs privadas
│   │       ├── agua.py         # Endpoints agua
│   │       └── aire.py         # Endpoints aire
│   ├── middleware/              # Middleware personalizado
│   │   └── cors.py             # CORS configurado
│   ├── main.py                  # Aplicación FastAPI
│   └── requirements.txt         # Dependencias actualizadas
├── Dockerfile                   # Imagen Docker
└── docker-compose.yml          # Configuración contenedores
```

## Comandos de Desarrollo

### Ejecutar el proyecto
```bash
cd backend
docker compose up --build
```

### Acceso a la API
- Documentación: http://localhost:8000/docs
- API base: http://localhost:8000/

### Comandos útiles de Docker
```bash
# Detener y limpiar completamente
docker compose down --volumes --remove-orphans

# Reconstruir sin cache
docker compose build --no-cache && docker compose up

# Ver logs
docker compose logs -f
```

## Base de Datos
- Usa Neon (PostgreSQL en la nube)
- Modelos definidos con SQLAlchemy
- Configuración en `database.py`

## Convenciones
- Modelos en `/app/models/`
- FastAPI endpoints en `main.py`
- Docker para desarrollo y despliegue
- Python 3.11 slim como base

## Endpoints Disponibles

### 🌐 Públicos (`/api/public/`)
- `GET /health` - Health check de la API
- `GET /info` - Información general de la API

### 🔒 Privados (`/api/private/`)
#### Aire:
- `GET /aire/temperatura` - Datos de temperatura
- `GET /aire/mp25/anual` - Material particulado 2.5 anual
- `GET /aire/mp25/mensual` - Material particulado 2.5 mensual
- `GET /aire/o3/anual` - Ozono anual
- *(19 endpoints total para aire)*

#### Agua:
- `GET /agua/mar-mensual` - Datos mensuales del mar
- `GET /agua/glaciares-anual-cuenca` - Glaciares por cuenca
- `GET /agua/coliformes-biologica` - Coliformes en matriz biológica
- *(10 endpoints total para agua)*

## Estado Actual
- ✅ Estructura modular implementada
- ✅ Schemas Pydantic para validación
- ✅ Routers organizados público/privado
- ✅ Configuración centralizada
- ✅ Middleware CORS configurado
- ✅ Documentación automática en `/docs`