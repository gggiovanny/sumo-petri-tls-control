# Descripción de los archivos
En la carpeta raiz del repositorio se encuentra una versión en desarrollo de una implementación de redes de petri. En un futuro cercano se usará para controlar semáforos en SUMO.
+ `petri.py` : Modulo con todas la logica de una red de Petri. Contiene clases que permiten crear a través de nodos tipo Place() y Transition() la estructura de una red de petri, bindear acciones a las transiciones, configurar tiempos de espera individuales a cada transición y funciones útiles para implementar todo de la manera más sencilla posible.
+ `config.py` : Contiene variables y funciones comunes de varios scripts, como la ruta actual y la funcion que genera el archivo de configuracion que controla las rutas, tipos y flujo de los vehiculos
+ `demo_prioridad.py`: Este script hace uso de la interfaz [TraCI](http://sumo.sourceforge.net/userdoc/TraCI.html) ([documentación](https://sumo.dlr.de/daily/pydoc/traci.html)) para acceder en tiempo real al simulador de tráfico urbano [SUMO](http://sumo.sourceforge.net/userdoc/index.html) y controlar los semaforos para darle prioridad a ambulancias que vienen desde la izquierda.
+ `demo_tls_ciclos.py` : En este demo se detectan los tipos de vehículos que circulan a través de detectores y cuando circula una ambulancia en cualquier dirección, se cambia el programa de control del semáforo (es decir, la política de control) a una especial para esta situacion que dura 30 segundos y en su defecto se usa una politica base. Tambien a manera de demostración, se cambia la politica base de acuerdo a rangos de tiempo para simular horas pico en la mañana y en la tarde.
+ `demo_petri.py` : En este demo, la lógica de los cambios de fases de los semáforos se hace usando una red de petri creada con el módulo `petri.py`, en lugar de la manera por defecto en la que lo hace SUMO. Esto es la base para implementaciones mucho más complejas.

En la carpeta `/data/sumo` de encuentran archivos .xml de configuración del simulador de tráfico urbano [SUMO](http://sumo.sourceforge.net/userdoc/index.html).
+ `demo.sumocfg` : Archivo de configuración principal de la simulación. En el se define que archivo de red de carreteras se usará y que archivo de generación de vehículos, entre otras configuraciones.
+ `demo.net.xml` : Define una red de carreteras y su contenido (semáforos, reglas de conexión entre carriles, prioridad, sentido, etc.). Este archivo fue creado con el editor gráfico [NETEDIT](http://sumo.sourceforge.net/userdoc/NETEDIT.html), que viene incluido en la instalación por defecto de SUMO.
+ `vehiculos.rou.xml` : Define tipos de vehículos y sus propiedades, flujos, rutas e instancias de los mismos. Este archivo se genera dinámicamente en el script `demo.py` a partir de probabilidades arbitrarias para cada dirección y tipo de vehículo.
+ Otros xml: Definen entidades extra, como detectores de tráfico y políticas de control de semáforos.
+ Para más información, consultar la [documentación oficial de SUMO](http://sumo.sourceforge.net/userdoc/SUMO_User_Documentation.html).

# Instalación y ejecución
Para ejecutar el módulo `Petri.py` de la creación de redes de petri solo es necesario el [interprete de Python](https://www.python.org/downloads/) y no es necesario (de momento) tener instalado SUMO. Pero para ejecutar `runner.py` o `demo.py` si es necesario lo siguiente:
1. Instalar SUMO. Las instrucciones para cada sistema operativo se encuentran en su [web](http://sumo.sourceforge.net/userdoc/Downloads.html).
2. [Solo Windows] Tener agregada la ruta de herramientas de SUMO al PATH de Windows. Dicha ruta se agrega de manera automática con el [instalador](https://sumo.dlr.de/releases/1.3.1/sumo-win64-1.3.1.msi) para Windows. En su defecto, se puede agregar la ruta `C:\Program Files (x86)\Eclipse\Sumo\tools\` [manualmente](https://www.java.com/en/download/help/path.xml).

Una vez instalado todo, ubicarse con la terminal en la ruta del script y ejecutarlo:
```
cd /ruta/a/carpeta/de/mi/script/
python runner.py
```
Esto abrirá SumoGui (interfáz gráfica de SUMO) y será necesario apretar el botón de inicio de la simulación.

<!-- # Uso futuro de la red de petri
 + Se toma al conjunto de agentes en cada semaforo como un [sistema distribuido](https://en.wikipedia.org/wiki/Distributed_computing).
 + Se los agentes se comunican unos con otros pasandose mensajes para lograr un objetivo común. -->

# Funciones para controlar los semaforos
+ petri.trafficlight.[setRedYellowGreenState](https://sumo.dlr.de/daily/pydoc/traci._trafficlight.html#TrafficLightDomain-setRedYellowGreenState)(self, tlsID, state): Permite ingresar un estado para el semáforo a través de una [cadena](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#signal_state_definitions) como "GrGr" para verde-rojo-verde-rojo en sentido de las manecillas del reloj, empezando desde arriba. Letras en minúsculas significa que los vehículos tienen que desacelerar. 
+ traci.trafficlight.[setProgram](https://sumo.dlr.de/daily/pydoc/traci._trafficlight.html#TrafficLightDomain-setProgram)(self, tlsID, programID): Cambia a el programa (politica de control)con el programID dado. El programa debe haber sido cargado previamente (mediante código o mediante un archivo de configuración `xml`). El valor especial 'off' se puede usar para apagar el semáforo.
