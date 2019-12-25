# Resumen

Tienes memoria de pez, esta es tu aplicación

Aun en desarrollo...



## Motivación

Este proyecto nace como **prueba de concepto** después de una típica discusión de café. Todos nos olvidamos de ponernos en pausa de café o nos vamos los viernes sin finalizar la jornada laboral y nos llama recursos humanos al final de mes diciendo como es posible que llevamos más de 60 horas trabajadas. Y en esa discusión siempre salta uno que dice: "*por favor, que somos desarrolladores, esto lo podemos automatizar fácilmente*" (ese fui yo). Y después del oportuno desafió aquí esta el resultado.



## Información

Aunque este proyecto nace como prueba de concepto al avanzar en su desarrollo lo he diseñado para que fuese modular y así que fuese fácilmente escalable. 

Existen tres módulos:

* **Calendario**: El calendario es donde se guarda el calendario laboral. Puede ser un archivo en formato json, una base de datos o google calendar. El calendario le facilita al motor información de cuando debe registrar las acciones. Por ejemplo yo uso google calendar, voy creando los eventos con la hora de inicio y fin de la jornada laboral. Si usas otro tipo de calendario por ejemplo el de Outlook, podrías crear tu propia clase y extenderla de `CalendarBase`. Y por último sólo tendrías que decirle a dory que use ese calendario modificando el parámetro de configuración `"calendar.type"`
* **Registrador**: Es donde se registran las acciones, por ejemplo el inicio de la jornada, la pausa del café. También facilita información al motor para la toma de decisiones. Le informa del estado actual y de los registros que ya se han realizado. Lo mismo que el modulo de calendario se puede extender, por defecto existe el registrador para Odoo, que es el que uso yo, pero puedes añadir cualquiera. Extiende de la clase `RegisterBase` y modifica la variable `"register.type"`.
* **Motor**: Es el encargado de la toma de decisiones, recupera información del calendario y el registrador y hace las llamadas al registrador en el momento indicado. Si encuentra algún tipo de discrepancia sale con error fatal.

Esquema:

​			Calendario  =>  Motor  <=> Registrador







## Dependencias

* termcolor
* google-api-python-client
* google-auth-httplib2
* google-auth-oauthlib
* python-dateutil



```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

