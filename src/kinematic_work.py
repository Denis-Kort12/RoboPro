import numpy as np
from ikpy.chain import Chain
from ikpy.link import OriginLink, DHLink

class KinematicCalculation:

    def __init__(self, dh_params, name="MyRobot"):
        self.robot_chain = self.build_chain(dh_params, name)

    def build_chain(self, dh_params, name):
        links = [OriginLink()]
        for params in dh_params:
            links.append(DHLink(theta=0, d=params["d"], a=params["a"], alpha=params["alpha"]))

        return Chain(name=name, links=links)

    def compute_position(self, joint_angles_deg):
        angles_rad = [0.0] + [np.radians(angle) for angle in joint_angles_deg]
        frame = self.robot_chain.forward_kinematics(angles_rad)
        return frame[:3, 3]
