# Tabla de Contenidos

1. [Resumen](#resumen)
2. [Motivación](#motivación)
3. [Get started](#get-started)
    1. [Entorno virtual](#1-entorno-virtual)
    2. [Clonar repositorio](#2-clonar- repositorio)
    3. [Instalar dependencias](#3-instalar-dependencias)
    4. [Ejecutar dory](#4-ejecutar-dory)
4. [Desarrollo](#desarrollo)



# Resumen

Tienes memoria de pez, esta es tu aplicación

Aun en desarrollo...


## Motivación

Este proyecto nace como **prueba de concepto** después de una típica discusión de café. Todos nos olvidamos de ponernos en pausa de café o nos vamos los viernes sin finalizar la jornada laboral y nos llama recursos humanos al final de mes diciendo como es posible que llevamos 60 horas trabajadas de más. Y en esa discusión siempre salta uno que dice: "*por favor, que somos desarrolladores, esto lo podemos automatizar fácilmente*" (ese fui yo). Y después del oportuno desafió aquí esta el resultado.



## Información

Aunque este proyecto nace como prueba de concepto al avanzar en su desarrollo lo he diseñado para que fuese modular y de ese modo se pudiese escalar fácilmente. 

He definido tres módulos:

* **Calendario**: El calendario es donde se guarda el calendario laboral. Puede ser un archivo en formato json, una base de datos o google calendar. El calendario le facilita al motor información de cuando debe registrar las acciones. Por ejemplo yo uso google calendar, voy creando los eventos con la hora de inicio y fin de la jornada laboral. Si usas otro tipo de calendario por ejemplo el de Outlook, podrías crear tu propia clase y extenderla de `CalendarBase`. Y por último sólo tendrías que decirle a dory que use ese calendario modificando el parámetro de configuración `"calendar.type"`
* **Registrador**: Es donde se registran las acciones, por ejemplo el inicio de la jornada, la pausa del café. También facilita información al motor para la toma de decisiones. Le informa del estado actual y de los registros que ya se han realizado. Lo mismo que el modulo de calendario se puede extender, por defecto existe el registrador para Odoo, que es el que se usa en mi organización, pero puedes añadir cualquiera. Extiende de la clase `RegisterBase` y modifica el parámetro `"register.type"`.
* **Motor**: Es el encargado de la toma de decisiones, recupera información del calendario y el registrador y hace las llamadas al registrador en el momento indicado. Si encuentra algún tipo de discrepancia lanza un error fatal y finaliza la ejecución.

Esquema:

​			Calendario  =>  Motor  <=> Registrador



## Get started

#### 1. Entorno virtual

Yo recomiendo que uses entornos virtuales en tus desarrollos. Si no quieres usarlo sáltate este paso.

Lo primer que deberías es crear el entorno virtual, para eso créalo con el comando:

```bash
virtualenv ~/python-env/dory --python=python3
```

Donde `python-env` es la carpeta donde almaceno mis entornos virtuales. Es una convención personal, puedes sustituir dicha carpeta por la que quieras usar. Recuerda crearla antes de crear el entorno virtual.

Con el modificador `--python` le estamos indicando que versión de `python` vamos a usar, en este caso `python3`.

Si no tienes instalado `virtualenv`, puedes instalarlo en `debian` con el siguiente comando:

```bash
sudo apt install virtualenv
```

También puedes instalarlo con `pip`:

```bash
sudo pip install virtualenv
```

Una vez que tenemos creado nuestro entorno virtual debemos activarlo:

```bash
source ~/python-env/dory/bin/activate
```

Comprobarás que estará activado porque el `prompt` del sistema cambiará y delante aparecerá el nombre del entorno virtual en nuestro caso "`(dory)`"

Si quieres salir del entorno virtual sólo tienes que ejecutar:

```bash
deactivate
```


#### 2. Clonar repositorio

Este proyecto dispone de **módulos**, para clonar el proyecto debes hacerlo en modo **recursivo**.

Ejemplo de comando para clonar el repositorio en la carpeta actual.

```bash
git clone --recursive git@github.com:nicoalonso/dory.git .
```


#### 3. Instalar dependencias

Para instalar las dependencias del proyecto debes ejecutar el siguiente comando, sitúate en la carpeta del proyecto si no lo has hecho aun.

```bash
pip install -r requirements.txt
```

Recuerda tener activado el entorno virtual cuando hagas esto, para instalar las dependencias en el entorno virtual y no globalmente. Por otro lado, si no usas el entorno virtual entonces modifica el comando anterior por `pip3`, ya que el proyecto esta programado sobre `python3`.


#### 4. Ejecutar dory

Esta todo listo para ejecutar dory:

```bash
python dory.py
```

Si no usas `virtualenv` ejecútalo así:

```bash
python3 dory.py
```



## Desarrollo

Eres libre para crear un **fork** del proyecto y extenderlo como quieras. Y si aparte quieres aportar mejoras a mi proyecto, eres bienvenido.

Si añades nuevas librerías para implementar diferentes APIs recuerda actualizar el fichero `requirements.txt`, puedes hacerlo de la siguiente manera:

```bash
pip freeze > requirements.txt
```

#### Ejecutar los tests unitarios

Para ejecutar los tests unitarios utiliza el comando:

```bash
python -m unittest
```

Para generar el **coverage** usa el siguiente comando:

```bash
coverage run -m unittest
```

Con el siguiente comando obtienes un report:

```
coverage report -m
```

Y por último si quieres obtenerlo en html:

```bash
coverage html
```

Para visualizarlo en el navegador hay muchas formas, yo lo hago usando el `http-server` de `nodejs`, tienes aquí el  enlace a su **github**: [http-server](https://github.com/http-party/http-server)