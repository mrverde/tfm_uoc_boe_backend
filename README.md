# TFM UOC BOE Backend

Este repositorio contiene el backend del trabajo final de máster. Consiste en una aplicación que se integra con las APIs del BOE y ChatGPT para hacer resumenes de los documentos del Boletin Oficial del Estado.

Esta aplicación usa Python, FastAPI y diferentes tecnologías. se generó a partir del repo [FastAPI-template](https://github.com/s3rius/FastAPI-template).


En primer lugar es necesario tener instalado poetry globalmente. Esto lo conseguimos usando:

```bash
pipx install poetry
```

En linux es posible que no tengamos por defecto pipx instalado, por lo que será necesario instalarlo también. En distribuciones debian se hace mediante:
```bash
sudo apt install pipx
```

Después renombraremos el archivo .env.bak a .env y añadiremos los valores de las variables de entorno.

Por último instalaremos las librerías

```bash
poetry install
```

Para ejecutar el proyecto usaremos el comando:
```bash
poetry run python -m tfm_uoc_boe_backend
```

Por defecto las variables de entorno exponen el puerto 8000, por lo que se puede acceder al backend a través de http://localhost:8000


Para acceder a la documentación de swagger usaremos la [siguiente dirección](http://localhost:8000/api/docs).


## Docker

Puede iniciarse el proyecto con docker usando el siguiente comando::

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

Para desarrollar en docker con la autorecarga hay que usar el siguiente comando de docker:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

Este comando expone la aplicación en el puerto 8000, pero si se modifican los archivos `poetry.lock` o `pyproject.toml` habrá que rehacer la imagen de docker con el siguiente comando:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Estructura del proyecto

```bash
$ tree "tfm_uoc_boe_backend"
tfm_uoc_boe_backend
├── conftest.py  # Fixtures para todas las pruebas
├── __main__.py  # Script de inicio. Inicia uvicorn.
├── services  # Librerías para los servicios externos como rabbit, redis, etc.
├── settings.py  # Ajustes principales de configuración del proyecto.
├── static  # Contenido estático.
├── tests  # Tests del proyecto.
└── web  # Paquete que contiene el servidor web, los handlers, la configuración de inicio...
    ├── api  # Paquete con todos los handlers handlers.
    │   └── router.py  # Enrutador principal.
    ├── application.py  # Configuración de la aplicación FastAPI.
    └── lifetime.py  # Acciones a realizar en el arranque y finalización de la aplicación.
```


## Ejecutar tests

Para ejecutarlos en local se hace con python y pytest:

```bash
python -m pytest -vv .
```
