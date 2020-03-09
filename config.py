import os
import sys
import random
# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
from sumolib import checkBinary  # noqa
import traci


base_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
sumo_data_path = os.path.join(base_path, 'data', 'sumo') + os.sep

def generar_archivo_vehiculos():
    random.seed(42)  # Hace que la prueba sea reproducible
    N = 3600  # numero de time steps (segundos de la simulacion)
    # demanda por segundo desde las diferentes direcciones
    probabilidad_coche_desde_izquierda = 1. / 10
    probabilidad_ambulancia_desde_izquierda =  1. / 100
    probabilidad_coche_desde_abajo = 1. / 50
    probabilidad_ambulancia_desde_abajo = 0
    with open(sumo_data_path+"vehiculos.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="coche_normal" length="5" color="1,1,0" maxSpeed="50" accel="2.6" decel="4.5" sigma="0.2" vClass="passenger"/>
    <vType id="emergencia" length="5" color="1,0,0" maxSpeed="50" accel="2.6" decel="4.5" sigma="0.2" vClass="emergency"/>
    <route id="de_izquierda_a_derecha" edges="izquierda_a_derecha_inicio izquierda_a_derecha_fin" />
    <route id="de_abajo_a_arriba" edges="abajo_a_arriba_inicio abajo_a_arriba_fin" />
    """, file=routes)
        coches_contador = 0
        for i in range(N):
            if random.uniform(0, 1) < probabilidad_coche_desde_izquierda:
                print('    <vehicle id="izq_%i" type="coche_normal" route="de_izquierda_a_derecha" depart="%i" color="1,1,0" />' % (
                    coches_contador, i), file=routes)
                coches_contador += 1
            if random.uniform(0, 1) < probabilidad_ambulancia_desde_izquierda:
                print('    <vehicle id="izq_ambulancia_%i" type="emergencia" route="de_izquierda_a_derecha" depart="%i" color="1,0,0" />' % (
                    coches_contador, i), file=routes)
                coches_contador += 1
            if random.uniform(0, 1) < probabilidad_coche_desde_abajo:
                print('    <vehicle id="abajo_%i" type="coche_normal" route="de_abajo_a_arriba" depart="%i" color="1,1,0" />' % (
                    coches_contador, i), file=routes)
                coches_contador += 1
            if random.uniform(0, 1) < probabilidad_ambulancia_desde_abajo:
                print('    <vehicle id="abajo_ambulancia_%i" type="emergencia" route="de_abajo_a_arriba" depart="%i" color="1,0,0" />' % (
                    coches_contador, i), file=routes)
                coches_contador += 1
            
        print("</routes>", file=routes)