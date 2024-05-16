import  os,sys
import numpy as np
import matplotlib.pyplot as plt
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'],'tools')
    sys.path.append(tools)
else:
    sys.exit("set SUMO_HOME")

import traci


#tau = 0.4
k_p = 0.7
k_d = 0.4
h = 0.7
N = 100.
kp = 1.4
kd = 0.8
ki = 0.
tau = 0.4

e_bar = np.array([0., 0., 0., 0., 0.])

ua = np.array([0., 0., 0., 0., 0.])

def run_step(v: float, a: float, u: float, dt):
    """
                    :param state_lon: Longitudinal State
                    :param u: Longitudinal input(desired acceleration)
    """

    # print(self.state_lon._u)
    a_dot = round(1.0 / tau * (u - a), 2)
    #print(u)
    a1 = a + a_dot * dt
    v1 = v + a1 * dt
    #s1 = s + v1 * dt
    data1 = np.array([v1, a1])
    return data1

def CACC(s0, v0, a0, s1, v1, a1):
    error = s0 -s1 - h * v1
    e_d = v0 - v1 - h * a1
    des_a = np.clip( a1 - tau/h * a1 + tau/h * (kp * error + kd * e_d + a0), -5.0, 3.0)
    return des_a



def Run():
    theta = 0
    theta2 =0
    dt = 0.1
    t = 0
    k =0
    t_all = np.array([0.])
    v_all = np.array([15., 15., 15., 15., 15.])
    v_one = np.array([15., 15., 15., 15., 15.])
    a_all = np.array([0., 0., 0., 0., 0.])
    a_one = np.array([0., 0., 0., 0., 0.])
    s = np.array([0., 0., 0., 0., 0.])
    error = np.array([0., 0., 0., 0., 0.])
    error_all = np.array([0., 0., 0., 0., 0.])
    current_directory = os.path.dirname(os.path.abspath(__file__))
    traci.start(['sumo-gui','-c',current_directory+'/cavers_pla.sumocfg'])
    step = 0
    a = np.array([0., 0., 0., 0., 0.])
    ua = np.array([0., 0., 0., 0., 0.])
    v_desired =15
    vehicle_positions = []
    traci.simulationStep()
    timesim = traci.simulation.getTime()
    pla_list= ('00', '01', '02', '03', '04')
    print(('00', '01', '02', '03', '04'))
    for i in traci.vehicle.getIDList():
        traci.vehicle.setSpeedMode(i, 0)
        traci.vehicle.setLaneChangeMode(i, 0)
        traci.vehicle.setSpeed(i, 15)
    while step<180:
        traci.simulationStep()
        for i in pla_list:
            if traci.simulation.getTime() > 40:
                v_desired = 18
            if traci.simulation.getTime() > 70:
                v_desired = 22
            if traci.simulation.getTime() > 100:
                v_desired = 18
            if traci.simulation.getTime() > 130:
                v_desired = 15
            match i:
                case '00':
                    k = 0
                    data = run_step(traci.vehicle.getSpeed(i), a[k], v_desired - traci.vehicle.getSpeed(i), 0.1)
                    a[k] = data[1]
                    traci.vehicle.setSpeed(i, data[0])
                    #print(traci.vehicle.getSpeed(i))
                    v_one[k] = data[0]
                    t  = t + dt

                case _:
                    k = k + 1
                    id0 = pla_list[k-1]
                    id_ = pla_list[k]
                    s0 = traci.vehicle.getPosition(id0)[0]
                    s1 = traci.vehicle.getPosition(id_)[0]
                    v1 = traci.vehicle.getSpeed(id_)
                    ua[k] = CACC(traci.vehicle.getPosition(id0)[0], traci.vehicle.getSpeed(id0), a[k-1], traci.vehicle.getPosition(id_)[0], traci.vehicle.getSpeed(id_),  a[k])
                    error[k] = s0 - s1 - h * v1
                    data = run_step(traci.vehicle.getSpeed(id_), a[k], ua[k], 0.1)
                    a[k] = data[1]
                    v_one[k] = data[0]
                    traci.vehicle.setSpeed(i, data[0])
                    #ua[k]


                #print(traci.vehicle.getPosition(i)[0])
            if t >= 30:
                v_all = np.vstack((v_all, v_one))
                a_all = np.vstack((a_all, a))
                t_all = np.vstack((t_all, t - 30))
                error_all = np.vstack((error_all, error))

        #print(traci.simulation.getTime())
        #if traci.simulation.getTime()>0:
           # print("stop")a
        # traci.vehicle.setSpeed(traci.vehicle.getIDList()[0],traci.vehicle.getSpeed(traci.vehicle.getIDList()[0])*0.5)
        step+=0.1

    plt.figure(figsize=(10, 6))
    for i in range(1):
        plt.subplot(2, 1, 1)
        plt.plot(t_all, v_all, label=('leader', 'vehicle 1', 'vehicle 2', 'vehicle 3', 'vehicle 4'))
        # plt.legend('Velocity response')
        plt.title("Platooning Response")
        plt.xlim(0, 120)
        plt.ylim(14, 25)
        # plt.xlabel('Time[s]')
        plt.ylabel('Vel[m/s]')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(t_all, error_all)
        plt.xlim(0, 140)
        plt.ylim(-0.4, 0.5)
        # plt.legend('Error response')
        plt.xlabel('time[s]')
        plt.ylabel('Error[m]')
        plt.savefig("cacc.pdf", format="pdf")
    traci.close()
    plt.show()
if __name__=="__main__":
    Run()