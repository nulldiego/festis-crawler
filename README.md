# festis-crawler
Crawler en Scrapy de la página web [festis](https://festis.es). Conectado a un servidor ElasticSearch de AWS mediante un pipeline, en el que indexa los documentos.

## Requerimientos
El fichero `requirements.txt` contiene las dependencias del proyecto, pueden instalarse mediante el comando:
```sh
$ pip install -r requirements.txt
```
Es recomendable crear un entorno virtual de Python en el que instalar las dependencias (con `virtualenv`).

## Configuración

El fichero `settings.py` debe ajustarse para apuntar al domino de ElasticSearch correcto y con las credenciales de Amazon Web Services.

```python
ELASTICSEARCH_AWS_ACCOUNTID = 'AccID' # Id de cuenta de AWS
ELASTICSEARCH_AWS_SECRETKEY = 'SecretKey' # Clave secreta de AWS
ELASTICSEARCH_AWS_ENDPOINT = 'AWS elastic domain' # Dominio en AWS de ElasticSearch
ELASTICSEARCH_AWS_REGION = 'AWS region' # Region
ELASTICSEARCH_INDEX = 'festis' # Indice en ElasticSearch
```

## Uso

Para ejecutar el crawler:

```sh
$ cd festis
$ scrapy crawl festis_crawler
```