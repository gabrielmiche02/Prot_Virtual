import numpy as np


class ParkTransform:

    @staticmethod
    def abc_to_dq0(a, b, c, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        cos_theta_120 = np.cos(theta - 2*np.pi/3)
        sin_theta_120 = np.sin(theta - 2*np.pi/3)
        cos_theta_p120 = np.cos(theta + 2*np.pi/3)
        sin_theta_p120 = np.sin(theta + 2*np.pi/3)

        d = (2/3) * (a * sin_theta + b * sin_theta_120 + c * sin_theta_p120)

        q = (2/3) * (a * cos_theta + b * cos_theta_120 + c * cos_theta_p120)

        z = (1/3) * (a + b + c)

        return d, q, z

    @staticmethod
    def alphabeta_to_dq(alpha, beta, theta):
        d = np.cos(theta) * alpha + np.sin(theta) * beta
        q = -np.sin(theta) * alpha + np.cos(theta) * beta

        return d, q
