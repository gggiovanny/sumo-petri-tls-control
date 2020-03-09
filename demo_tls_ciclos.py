import config
from config import traci

def hoursToSeconds(horas):
    return horas*60*60

def run():
    programa_todo_el_dia = "principal"
    programa_tarde = "hora_pico_tarde"
    programa_dia = "hora_pico_dia"
    programa_emergencia = "emergencia"
    programa_base = programa_todo_el_dia
    detectores = ['detector_izquierda', 'detector_abajo']    
    
    traci.trafficlight.setProgram("semaforo_principal", programa_base) #? # define la politica de control a usarse
    print("[t=-1] Programa cambiado a:", traci.trafficlight.getProgram("semaforo_principal"))
    
    tiempo_emergencia = 30
    programa_anterior = programa_base
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        programa_anterior = traci.trafficlight.getProgram("semaforo_principal")
        #* Cambiando el programa principal segun la hora
        if 100 < step < 250:
            programa_base = programa_dia
        elif 600 < step < 750:
            programa_base = programa_tarde
        else:
            programa_base = programa_todo_el_dia   
        step+=1
        #* Detectando ambulancias y logueando tipos de vehiculos
        hay_ambulancia = False #? bandera que indica si hay alguna ambulancia en alguno de los detectores
        for detector in detectores:
            if traci.inductionloop.getLastStepVehicleNumber(detector) > 0:
                carID = traci.inductionloop.getLastStepVehicleIDs(detector)[0]
                carClass = traci.vehicle.getVehicleClass(carID)
                if carClass == "emergency":
                    hay_ambulancia = True
                    print('**[t={}, {}] carID={}, class={}**'.format(step, detector, carID, carClass))
                else:
                    print('[t={}, {}] carID={}, class={}'.format(step, detector, carID, carClass))
        #* Cambiando el programa si hay ambulancia en cualquier detector
        if hay_ambulancia and programa_anterior != programa_emergencia:
            traci.trafficlight.setProgram("semaforo_principal", programa_emergencia)
            tiempo_emergencia = 30
            print("[t={}] Programa cambiado a: {}".format(step, traci.trafficlight.getProgram("semaforo_principal")))
        elif programa_anterior == programa_emergencia:
            if tiempo_emergencia == 0:
                traci.trafficlight.setProgram("semaforo_principal", programa_base)
                print("[t={}] Programa cambiado a: {}".format(step, traci.trafficlight.getProgram("semaforo_principal")))
            else:
                tiempo_emergencia-=1
    traci.close()

if __name__ == "__main__":
    # genera el archivo de configuracion que controla las rutas, tipos y flujo de los vehiculos
    config.generar_archivo_vehiculos()
    # este es el modo normal de usar traci. sumo es iniciado como un subproceso y entonces el script de python se conecta y ejecuta
    traci.start(['sumo-gui', "-c", config.sumo_data_path+'demo.sumocfg'])
    run()