import math


class ClarkTransform:
    @staticmethod
    def abc_to_alphabeta(a, b, c):
        alpha = (2/3) * (a - 0.5*b - 0.5*c)
        beta = (2/3) * (math.sqrt(3)/2*b - math.sqrt(3)/2*c)

        return alpha, beta
