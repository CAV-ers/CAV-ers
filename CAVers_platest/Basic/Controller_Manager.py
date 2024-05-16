import numpy as np

class ACC(object):
    def __init__(self, ego_x: float, ego_v: float, front_x: float, front_v: float):
        """
        :param: sx = x-position in a global coordinate system
        :param: sy = y-position in a global coordinate system
        :param: vx = x-velocity a global coordinate system
        :param: vy = y-velocity a global coordinate system
        """
        self.ego_x = ego_x
        self.ego_v = ego_v
        self.front_x = front_x
        self.front_v = front_v
        self._ego_x = ego_x
        self._ego_v = ego_v
        self._front_x = front_x
        self._front_v = front_v
        self.ego_a = 0.0
        self._ego_a = 0.0
        self.ego_u = 0.0
        self._ego_u = 0.0
        self.ego_ua = self.u
        self._ego_ua = self.u
        self.h = 0.7
        self.k_p = 0.7
        self.k_d = 0.3

    def update_info(self, ego_vehicle, front_vehicle):
        """
            Calculate the current control input for next step.
            """

        self.ego_x = ego_vehicle.ego_x
        self.ego_v = ego_vehicle.ego_v
        self.front_x = front_vehicle.
        self.front_v = front_vehicle

    # return control_command
    def calculate_input(self, vehicle):
        """
            Calculate the current control input for next step.
            """
        control_input = self.k_p * (vehicle.front_x - self.ego_x - self.h * self.ego_v) \
                        + self.k_d * (vehicle.front_v - self.ego_v)
        return control_input


class CACC(object):
    def __init__(self, ego_x: float, ego_v: float, front_x: float, front_v: float):
        """
            :param: sx = x-position in a global coordinate system
            :param: sy = y-position in a global coordinate system
            :param: vx = x-velocity a global coordinate system
            :param: vy = y-velocity a global coordinate system
            """
        self.ego_x = ego_x
        self.ego_v = ego_v
        self.ego_a = 0.0
        self.front_x = front_x
        self.front_v = front_v
        self.front_ua = 0.0
        self.a = 0.0
        self.u = 0.0
        self.ua = self.u
        self.h = 0.7
        self.k_p = 0.7
        self.k_d = 0.3

    def update_info(self, ego_x: float, ego_v: float, ego_a:float, front_x: float, front_v: float, front_ua: float):
        """
                Calculate the current control input for next step.
                """

        self.ego_x = ego_x
        self.ego_v = ego_v
        self.ego_a = ego_a
        self.front_x = front_x
        self.front_v = front_v
        self.front_ua = front_ua
        # return control_command
    def calculate_input(self, target_speed, waypoint):
        """
                Calculate the current control input for next step.
                """
        control_input = self.k_p * (self.front_x - self.ego_x - self.h * self.ego_v) \
                            + self.k_d * (self.front_v - self.ego_v - self.h * self.a) + self.front_ua
        return control_input


class CACC_2(object):
    def __init__(self, ego_x: float, ego_v: float, front_x: float, front_v: float, tau: float):
        """
            :param: sx = x-position in a global coordinate system
            :param: sy = y-position in a global coordinate system
            :param: vx = x-velocity a global coordinate system
            :param: vy = y-velocity a global coordinate system
            """
        self.ego_x = ego_x
        self.ego_v = ego_v
        self.ego_a = 0.0
        self.front_x = front_x
        self.front_v = front_v
        self.front_ua = 0.0
        self.a = 0.0
        self.u = 0.0
        self.ua = self.u
        self.h = 0.7
        self.k_p = 0.7
        self.k_d = 0.3
        self.tau = tau
    def update_info(self, ego_x: float, ego_v: float, ego_a: float, front_x: float, front_v: float, front_a: float):
        """
                Calculate the current control input for next step.
                """

        self.ego_x = ego_x
        self.ego_v = ego_v
        self.ego_a = ego_a
        self.front_x = front_x
        self.front_v = front_v
        self.front_a = front_a
        # return control_command

    def calculate_input(self, target_speed, waypoint):
        """
                Calculate the current control input for next step.
                """
        control_input = self.ego_a - self.tau/self.h  *(-self.ego_a+ self.k_p * (self.front_x - self.ego_x - self.h * self.ego_v) \
                        + self.k_d * (self.front_v - self.ego_v - self.h * self.a) + self.front_a)
        return control_input

