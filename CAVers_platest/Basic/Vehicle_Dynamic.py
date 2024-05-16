import  os,sys
import numpy as np
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'],'tools')
    sys.path.append(tools)
else:
    sys.exit("set SUMO_HOME")

import traci
from Controller_Manager import CACC, ACC, CACC_2


class MassPoint:
    """
    Longitudinal state in curvilinear coordinate system
    """
    def __init__(self, ego_pos: float, ego_vel: float, vx: float, vy: float):
        """
        :param: ego_s = position states in a global coordinate system [x,y]
        :param: ego_v = velocity states in a global coordinate system [vx, vy]
        """
        self.sx = sx
        self.sy = sy
        self.vx=  vx
        self.vy = vy
        self.u = np.array([0, 0])
        self.a = self.u


class LongitudinalEM:
    """
    Longitudinal state of engine dynamics model in curvilinear coordinate system
    """
    def __init__(self, id, ego_pos, ego_vel, front_pos, front_vel):
        """
        :param s: longitudinal position in curvilinear coordinates
        :param v: longitudinal velocity in curvilinear coordinates
        :param a: longitudinal acceleration in curvilinear coordinates
        """
        self.id = id
        self.ego_x = ego_pos[0]
        self.ego_v = ego_vel[0]
        self.front_x = front_pos[0]
        self.front_v = front_vel[0]
        self._ego_x = self.ego_x
        self._ego_v = self.ego_v
        self._front_x = self.front_x
        self._front_v = self.front_v
        self.ego_a = 0.0
        self._ego_a = 0.0
        self.ego_u = 0.0
        self._ego_u = 0.0
        self.ego_ua = 0.0
        self._ego_ua = 0.0
        self.controller = ACC

    def update_info(self, front_vehicle):
        """
        Update ego vehicle information for controller.
        """
        self.ego_x = traci.vehicle.getPosition(self.id)[0]
        self.ego_v = traci.vehicle.getVelocity(front_vehicle.id)[0]
        self.front_x = traci.vehicle.getPosition(self.id)[0]
        self.front_v = traci.vehicle.getVelocity(front_vehicle.id)[0]
        self.controller.update_info(self, front_vehicle)

    def simulation_step(self):
        """
        Execute current controller step.
        """
        control_command = self.controller.calculate_input(self)

        return control_command

    def update_state(self, ego_pos, ego_speed):
        """
        Update ego vehicle information for controller.
        """
        self.controller.update_info(ego_pos, ego_speed)

class StateBicycle:
    """
    Longitudinal state in curvilinear coordinate system
    """
    def __init__(self, sx: float, sy: float, v: float, delta: float, psi: float):
        """
        :param: x = x-position in a global coordinate system
        :param: y = y-position in a global coordinate system
        :param: v = velocity in yaw direction
        :param: delta = steering angle of front wheels
        :param: psi = yaw angle
        """
        self._sx = sx
        self._sy = sy
        self._delta = delta
        self._v = v
        self._psi = psi
        self._u = np.array([0, 0])
        self._a = 0.0
        self._vd = 0.0 # v_delta





