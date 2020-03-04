# Descripción de los archivos
En la raíz del repositorio de encuentran archivos .xml de configuración del simulador de tráfico urbano [SUMO](http://sumo.sourceforge.net/userdoc/index.html).
+ `demo.sumocfg` : Archivo de configuración principal de la simulación. En el se define que archivo de red de carreteras se usará y que archivo de generación de vehículos, entre otras configuraciones.
+ `demo.net.xml` : Define una red de carreteras y su contenido (semáforos, reglas de conexión entre carriles, prioridad, sentido, etc.). Este archivo fue creado con el editor gráfico [NETEDIT](http://sumo.sourceforge.net/userdoc/NETEDIT.html), que viene incluido en la instalación por defecto de SUMO.
+ `vehiculos.rou.xml` : Define tipos de vehículos y sus propiedades, flujos, rutas e instancias de los mismos. Este archivo se genera dinámicamente en el script `demo.py` a partir de probabilidades arbitrarias para cada dirección y tipo de vehículo.
+ Otros xml: Definen entidades extra, como detectores de tráfico y políticas de control de semáforos.
+ `demo.py`: Script que genera el archivo de configuracion que controla las rutas, tipos y flujo de los vehiculos. Luego SUMO es iniciado como un subproceso y entonces el script se conecta y tiene acceso en tiempo real a la simulación a través de la interfaz [TraCI](http://sumo.sourceforge.net/userdoc/TraCI.html) ([documentación](https://sumo.dlr.de/daily/pydoc/traci.html)) incluida en la instalación por defecto de SUMO.
+ Para más información, consultar la [documentación oficial de SUMO](http://sumo.sourceforge.net/userdoc/SUMO_User_Documentation.html).

En la carpeta `/petri_network` se encuentra una versión en desarrollo de una implementación de redes de petri para en un futuro cercano controlar los semáforos utilizándolas. El archivo principal es `/petri_network/main.py`.

# Instalación y ejecución
Para ejecutar el script de pruebas de la creación de redes de petri solo es necesario el [interprete de Python](https://www.python.org/downloads/) y no es necesario (de momento) tener instalado SUMO. Para ejecutar demo.py es necesario lo siguiente:
1. Instalar SUMO. Las instrucciones para cada sistema operativo se encuentran en su [web](http://sumo.sourceforge.net/userdoc/Downloads.html).
2. [Solo Windows] Tener agregada la ruta de herramientas de SUMO al PATH de Windows. Dicha ruta se agrega de manera automática con el [instalador](https://sumo.dlr.de/releases/1.3.1/sumo-win64-1.3.1.msi) para Windows. En su defecto, se puede agregar la ruta `C:\Program Files (x86)\Eclipse\Sumo\tools\` [manualmente](https://www.java.com/en/download/help/path.xml).

Una vez instalado todo, ubicarse con la terminal en la ruta del script y ejecutarlo:
```
cd /ruta/a/carpeta/de/mi/script/
python demo.py
```
Esto abrirá SumoGui (interfáz gráfica de SUMO) y será necesario apretar el botón de inicio de la simulación.

# Uso futuro de la red de petri
 + Se toma al conjunto de agentes en cada semaforo como un [sistema distribuido](https://en.wikipedia.org/wiki/Distributed_computing).
 + Se los agentes se comunican unos con otros pasandose mensajes para lograr un objetivo común.