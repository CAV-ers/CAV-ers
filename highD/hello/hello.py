import  os,sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'],'tools')
    sys.path.append(tools)
else:
    sys.exit("set SUMO_HOME")


import traci

# from randomTrips import buildTripGenerator

def Run():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    traci.start(['sumo-gui','-c',current_directory+'/hello.sumocfg'])
    step = 0
    while step<10000:
        traci.simulationStep()

        vehicles=traci.vehicle.getIDList
        print(vehicles)

        # traci.vehicle.getRouteID()
        # traci.vehicle.getRoute()
        # print(traci.vehicle.getIDList())
        # print(traci.simulation.getTime())
        # if traci.simulation.getTime()>0:
        #     print("stop")
        # for i in traci.vehicle.getIDList():
        #     print(traci.vehicle.getLaneID(i))
        #     print(i,traci.vehicle.getRoute(i))
        # traci.vehicle.setSpeed(traci.vehicle.getIDList()[0],traci.vehicle.getSpeed(traci.vehicle.getIDList()[0])*0.5)
        step+=0.01
    traci.close()

if __name__=="__main__":
    Run()