import numpy as np


class MAF_PLL:
    def __init__(self, window_size, nominal_frequency, dt):
        self.nominal_omega_frequency = nominal_frequency * 2 * np.pi
        self.pll_omega_frequency = 0
        self.window_size = window_size
        self.dt = dt
        self.window_vd = []
        self.window_vq = []
        self.proportional_gain = 300
        self.integrator_gain = 4500
        self.output_proportional = 0
        self.output_integrator = 0
        self.theta = 0

    def calculate(self, vd_signal, vq_signal):
        self.window_vd.append(vd_signal)
        self.window_vq.append(vq_signal)
        if len(self.window_vd) > self.window_size:
            self.window_vd.pop(0)
        if len(self.window_vq) > self.window_size:
            self.window_vq.pop(0)

        vd_mean = sum(self.window_vd) / len(self.window_vd)
        vq_mean = sum(self.window_vq) / len(self.window_vq)

        error = vq_mean

        self.output_proportional = self.proportional_gain * error
        self.output_integrator = self.output_integrator + (self.integrator_gain * self.dt * error)

        self.pll_omega_frequency = self.output_integrator + self.output_proportional + self.nominal_omega_frequency

        self.theta = self.theta + (self.dt * self.pll_omega_frequency)

        if self.theta >= np.pi:
            self.theta = self.theta - (2.0 * np.pi)

        return self.pll_omega_frequency, self.theta
