from config import traci
import config
import petri

def hacerAlgo():
    print("haciendo algo...")

def generatePetriNet():
    # Generando una lista de objetos Places() (Lugares) en una lista llamada 'places'
    places = petri.generatePlaces(range(4))
    # Repitiendo el mismo proceso para generar los objetos tipo Transition() en la lista 'transition'
    transition = petri.generateTransitions(range(4))
    # Estableciendo las relaciones entre Places y Transitions
    places[0].addNext(transition[0]) 
    transition[0].addNext(places[1])
    places[1].addNext(transition[1])
    transition[1].addNext(places[2])
    places[2].addNext(transition[2])
    transition[2].addNext(places[3])
    places[3].addNext(transition[3])
    transition[3].addNext(places[0])
    
    transition[1].wait_time = 30
    transition[2].wait_time = 6
    transition[3].wait_time = 35
    transition[0].wait_time = 6
    
    transition[0].action = lambda:traci.trafficlight.setRedYellowGreenState("semaforo_principal", "GrGr")
    transition[1].action = lambda:traci.trafficlight.setRedYellowGreenState("semaforo_principal", "yryr")
    transition[2].action = lambda:traci.trafficlight.setRedYellowGreenState("semaforo_principal", "rGrG")
    transition[3].action = lambda:traci.trafficlight.setRedYellowGreenState("semaforo_principal", "ryry")
    
    # transition[0].action = lambda:traci.trafficlight.setPhase("semaforo_principal", 0)
    # transition[1].action = lambda:traci.trafficlight.setPhase("semaforo_principal", 1)
    # transition[2].action = lambda:traci.trafficlight.setPhase("semaforo_principal", 2)
    # transition[3].action = lambda:traci.trafficlight.setPhase("semaforo_principal", 3)
    
    initial_state = [1,0,0,0]
    return petri.Network(places, transition, initial_state, 6)

def run(net):
    #? define la politica de control a usarse
    traci.trafficlight.setProgram("semaforo_principal", "manual")
    
    #* Ejecuta el bucle de control de TraCI
    while traci.simulation.getMinExpectedNumber() > 0:
        estado_anterior = traci.trafficlight.getRedYellowGreenState("semaforo_principal")
        traci.simulationStep()
        net.nextStep()
        estado_actual = traci.trafficlight.getRedYellowGreenState("semaforo_principal")
        if estado_actual != estado_anterior:
            print("Estado cambiado: {}->{}".format(estado_anterior, estado_actual))
        
    traci.close()

# este es el punto de entrada al script
if __name__ == "__main__":
    #? genera el archivo de configuracion que controla las rutas, tipos y flujo de los vehiculos
    config.generar_archivo_vehiculos()
    #? Generando la red de petri
    net = generatePetriNet()
    #? este es el modo normal de usar traci. sumo es iniciado como un subproceso y entonces el script de python se conecta y ejecuta
    traci.start(['sumo-gui', "-c", config.sumo_data_path+'demo.sumocfg'])
    #? ejecutando la funcion que controla a la simulacion
    run(net)