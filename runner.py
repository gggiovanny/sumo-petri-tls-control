from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import random
sys.path.append("petri_network/")
import Petri
# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
    

from sumolib import checkBinary  # noqa
import traci  # noqa

ruta = os.path.dirname(os.path.realpath(__file__)) + os.sep

def generar_archivo_vehiculos():
    random.seed(42)  # Hace que la prueba sea reproducible
    N = 3600  # numero de time steps (segundos de la simulacion)
    # demanda por segundo desde las diferentes direcciones
    probabilidad_coche_desde_izquierda = 1. / 10
    probabilidad_ambulancia_desde_izquierda =  1. / 30
    probabilidad_coche_desde_abajo = 1. / 10
    probabilidad_ambulancia_desde_abajo = 0
    with open(ruta+"vehiculos.rou.xml", "w") as routes:
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

# la logica de la politica de contro (program logic) se ve asi
# <tlLogic id="semaforo_principal" type="static" programID="principal" offset="0">
#     <phase duration="40" state="GrGr"/>   # indice 0
#     <phase duration="6" state="yryr"/>    # indice 1
#     <phase duration="40" state="rGrG"/>   # indice 2
#     <phase duration="6" state="ryry"/>    # indice 3
# </tlLogic>

def hacerAlgo():
    print("haciendo algo...")

def run():
    # define la politica de control a usarse
    traci.trafficlight.setProgram("semaforo_principal", "principal")
    net = Petri.getDemoNetwork()
    # for transition in net.transitions:
    #     transition.action = hacerAlgo

    """Ejecuta el bucle de control de TraCI"""
    step = 0
    hay_ambulancia_abajo = False
    hay_ambulancia_izquierda = False
    contador_fase_2 = 0
    contador_fase_0 = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        net.nextStep()
        hay_ambulancia_izquierda = False
        if traci.inductionloop.getLastStepVehicleNumber("detector_izquierda") > 0:
            carID = traci.inductionloop.getLastStepVehicleIDs("detector_izquierda")[0]
            carClass = traci.vehicle.getVehicleClass(carID)
            # print('[time=%s, detector_izquierda] id=%s, class=%s' % (step, carID, carClass))
            if carClass == "emergency":
                hay_ambulancia_izquierda = True
        # si el semaforo esta en rojo para la izquierda y en verde para abajo
        if traci.trafficlight.getPhase("semaforo_principal") == 0:
            contador_fase_0 += 1
            if hay_ambulancia_izquierda: # si viene una ambulancia por la izquierda...
                traci.trafficlight.setPhase("semaforo_principal", 1) # ... cambiar la luz para darle paso
        else:
            if contador_fase_0 != 0:
                print("Total fase 0: ", contador_fase_0)
                contador_fase_0 = 0
        # si el semaforo esta en verde para la izquierda y en rojo para abajo
        if traci.trafficlight.getPhase("semaforo_principal") == 2:
            contador_fase_2 += 1
            if hay_ambulancia_izquierda: # si viene una ambulancia por la izquierda...
                traci.trafficlight.setPhaseDuration("semaforo_principal", contador_fase_2 + 10) # ... aumentar la duracion del estado en verde
        else:
            if contador_fase_2 != 0:
                print("Total fase 2: ", contador_fase_2)
                contador_fase_2 = 0
        if traci.trafficlight.getPhase("semaforo_principal") == 3:
            if hay_ambulancia_izquierda: # si viene una ambulancia por la izquierda...
                traci.trafficlight.setPhase("semaforo_principal", 1) # ... cambiar la luz para darle paso
        step+=1
        
    traci.close()
    sys.stdout.flush()

def runPruebas():
    """execute the TraCI control loop"""
    step = 0
    # we start with phase 2 where EW has green
    traci.trafficlight.setPhase("0", 2)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if traci.trafficlight.getPhase("0") == 2:
            # we are not already switching
            if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
                # there is a vehicle from the north, switch
                traci.trafficlight.setPhase("0", 3)
            else:
                # otherwise try to keep green for EW
                traci.trafficlight.setPhase("0", 2)
        step += 1
    traci.close()
    sys.stdout.flush()

# este es el punto de entrada al script
if __name__ == "__main__":
    # genera el archivo de configuracion que controla las rutas, tipos y flujo de los vehiculos
    generar_archivo_vehiculos()
    # este es el modo normal de usar traci. sumo es iniciado como un subproceso y entonces el script de python se conecta y ejecuta
    traci.start(['sumo-gui', "-c", ruta+'demo.sumocfg'])
    run()
