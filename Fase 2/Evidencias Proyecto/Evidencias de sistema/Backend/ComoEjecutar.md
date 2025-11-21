# Instrucciones para ejecutar el Backend (FastAPI + Docker)

## Requisitos previos:

- Tener instalado Docker Desktop (Windows/Mac) o Docker Engine (Linux).
- Iniciar Docker (Puedes comprobarlo usando este comando):
  ```bash
    docker info
  ```

## Ejecución

En la raíz del proyecto ejecuta:

```bash
  cd backend
  docker compose up --build
```

Esto hará lo siguiente:

- Entrara al directorio backend (Donde estan las instrucciones para que Docker las lea)
- Construirá una imagen de Python 3.11 slim con todas las dependencias.
- Copiará el código del backend dentro del contenedor.
- Levantará el servidor de FastAPI con Uvicorn.

## Acceso a la API

En tu navegador abre el siguiente enlace http://localhost:8000/docs para ver la documentación de tus `Endpoints`

Y usa http://localhost:8000/`Endpoints` para comunicarte con la API

## Comandos Útiles

- Detener el servicio sin dejar rastro (Esto eliminará todo lo creado con `docker compose up -- build`):
  ```bash
    docker compose down --volumes --remove-orphans
  ```
- Reconstruir sin usar cache:
  ```bash
    docker compose build --no-cache && docker compose up
  ```
- Ver logs en tiempo real:
  ```bash
    docker compose logs -f
  ```
