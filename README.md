# django polls SRP

proyecto que va desde la forma más sencilla de django hasta una arquitectura hexagonal, aunque se planea que llege a microservicios, siempre teniendo en mente el principio de responsabilidad única en casi todo momento, aunque a veces no se sigue al 100%, es común de cualquier humano errar.

## dependencias

- python 3.13>= (si hubiese elegido Optional en lugar de pipes | en typehints tal vez 3.8>=. prueba tu mismo)
- ver requirements.txt

## como usar
de preferencia (preferentemente obligatorio) usa un entorno virtual e instala las dependencias

```sh
pip install -r requirements.txt
```

despues de eso situate en el directorio raíz de este proyecto y corre:

```sh
python manage.py migrate
```

si gustas crea un super usuario aunque no es necesario y corre el servidor de pruebas

```sh
python manage.py runserver
```

en tu localhost por el puerto 8000 en la dirección polls podrás ver la aplicación polls, así que en tu navegador entra al esta URI: localhost:8000/polls o 127.0.0.1:8000/polls

## notas

estas mismas dependencias funcionan desde el inico del proyecto, pero por prisa al escibir las instrucciones en un documento olvidé poner este readme, así que pues igual instálalas antes de cambiar a cualquier commit que veas que te interese