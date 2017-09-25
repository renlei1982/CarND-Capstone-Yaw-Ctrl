
GAS_DENSITY = 2.858
ONE_MPH = 0.44704

import rospy
from pid import PID
from yaw_controller import YawController


class Controller(object):
    def __init__(self, vehicle_mass, wheel_radius, brake_deadband,
                 decel_limit, accel_limit, wheel_base, steer_ratio, max_lat_accel, max_steer_angle):
        # TODO: Implement
        # Fixed parameters
        self.vehicle_mass = vehicle_mass
        self.brake_deadband = brake_deadband
        self.wheel_radius = wheel_radius
        self.accel_limit = accel_limit
        self.wheel_base = wheel_base
        self.steer_ratio = steer_ratio
        self.max_lat_accel = max_lat_accel
        self.max_steer_angle = max_steer_angle
        
        # To be Updated in each cycle
        self.twist_command = None
        self.current_velocity = None
        self.enabled = False
        self.sample_time = 1/50 # initial value, gets updated in loop

        self.throttle_PID = PID(0.1, 0.1, 0.1) # Dummy values

        self.throttle_error = 0

        self.yaw_ctrl = YawController(self.wheel_base,
                                      self.steer_ratio,
                                      0,
                                      self.max_lat_accel,
                                      self.max_steer_angle) # Set the min_speed as 0
        




    def control(self, target_v, target_angular_v, actual_v, dbw_status):
        # TODO: Change the arg, kwarg list to suit your needs
        self.throttle_error = target_v - actual_v

        throttle = self.throttle_PID.step(self.throttle_error, self.sample_time) #sample_time should be sampled from 'dbw_node.py' loop func 

        steer = self.yaw_ctrl.get_steering(target_v, target_angular_v, actual_v)

        brake = 0; # to be implemented
        # Return throttle, brake, steer
        return throttle, brake, steer
