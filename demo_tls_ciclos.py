import config
from config import traci

def run():
    # define la politica de control a usarse
    traci.trafficlight.setProgram("semaforo_principal", "principal")
    print("Programa cambiado a:", traci.trafficlight.getProgram("semaforo_principal"))
    
    while traci.simulation.getMinExpectedNumber() > 0:
        

if __name__ == "__main__":
    config.generar_archivo_vehiculos()
    traci.start(['sumo-gui', "-c", config.sumo_data_path+'demo.sumocfg'])
    run()