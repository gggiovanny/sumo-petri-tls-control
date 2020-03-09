import sys
from config import traci
import config
import Petri

def hacerAlgo():
    print("haciendo algo...")

def run():
    # define la politica de control a usarse
    traci.trafficlight.setProgram("semaforo_principal", "principal")
    net = Petri.getDemoNetwork()
    # for transition in net.transitions:
    #     transition.action = hacerAlgo

    """Ejecuta el bucle de control de TraCI"""
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        net.nextStep()
        
        
    traci.close()
    sys.stdout.flush()

# este es el punto de entrada al script
if __name__ == "__main__":
    # genera el archivo de configuracion que controla las rutas, tipos y flujo de los vehiculos
    config.generar_archivo_vehiculos()
    # este es el modo normal de usar traci. sumo es iniciado como un subproceso y entonces el script de python se conecta y ejecuta
    traci.start(['sumo-gui', "-c", config.sumo_data_path+'demo.sumocfg'])
    run()
