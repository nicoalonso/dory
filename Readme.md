# Tabla de Contenidos

1. [Resumen](#resumen)
2. [Motivación](#motivación)
3. [Get started](#get-started)
    1. [Entorno virtual](#1-entorno-virtual)
    2. [Clonar repositorio](#2-clonar-repositorio)
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

Recomiendo que uses entornos virtuales en tus desarrollos. Si no quieres usarlo sáltate este paso.

Lo primer que deberías es crear el entorno virtual, para eso créalo con el comando:

```bash
virtualenv ~/python-env/dory --python=python3
```

Donde `python-env` es la carpeta donde almaceno mis entornos virtuales. Es una convención personal, puedes sustituir dicha carpeta por la que quieras usar. Recuerda crearla antes de ejecutar el comando.

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

Comprobarás que estará activado porque el `prompt` de la terminal cambiará y delante aparecerá el nombre del entorno virtual en nuestro caso "`(dory)`"

Si quieres salir del entorno virtual sólo tienes que ejecutar:

```bash
deactivate
```


#### 2. Clonar repositorio

En este proyecto estoy usando los **módulos de git**, ya que tengo código re-utilizable en otros proyectos. 

Por este motivo a la hora de clonar el proyecto deberás hacerlo en modo **recursivo**.

Ejemplo:

```bash
git clone --recursive git@github.com:nicoalonso/dory.git .
```



#### 3. Instalar dependencias

Sitúate en la carpeta del proyecto, recuerda tener el entrono virtual activado si no quieres instalar las dependencias de modo global. Y ejecuta el siguiente comando:

```bash
pip install -r requirements.txt
```

En caso de que no desees usar el entorno virtual, ejecútalo de este modo:

```bash
pip3 install -r requirements.txt
```




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

Método abreviado para ejecutar los tests y generar el coverage:

```bash
coverage run -m unitest && coverage html
```

