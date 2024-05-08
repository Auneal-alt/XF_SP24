# DualCycle.py
from Air import air, StateDataForPlotting, units
import numpy as np


class DualCycleModel():
    def __init__(self, p_initial=100000, t_initial=300, ratio=18, cutoff_ratio=1.2, pressure_ratio=1.5):
        self.units = units()
        self.units.SI = True
        self.air = air()  # the working fluid
        self.air.set(P=p_initial, T=t_initial)  # initial state is fixed at p_initial, t_initial

        self.Ratio = ratio  # Compression ratio V1/V2
        self.Cutoff_ratio = cutoff_ratio  # Cutoff ratio V4/V3
        self.Pressure_ratio = pressure_ratio  # Pressure ratio P3/P2

        # Calculate the states based on the cycle description
        self.State1 = self.air.set(P=p_initial, T=t_initial)
        self.State2 = self.air.set(v=self.State1.v / self.Ratio, s=self.State1.s)  # Isentropic compression
        self.State3 = self.air.set(P=self.State2.P * self.Pressure_ratio,
                                   v=self.State2.v)  # Constant volume heat addition
        self.State4 = self.air.set(P=self.State3.P,
                                   v=self.State3.v * self.Cutoff_ratio)  # Constant pressure heat addition
        self.State5 = self.air.set(v=self.State1.v, s=self.State4.s)  # Isentropic expansion

        # Heat and work calculations for the cycle
        self.Q_in = self.air.n * (self.State3.h - self.State2.h + self.State4.h - self.State3.h)
        self.W_net = self.air.n * ((self.State2.u - self.State1.u) + (self.State4.u - self.State5.u))
        self.Efficiency = 100 * (self.W_net / self.Q_in if self.Q_in != 0 else 0)

    def update_states(self):
        # Re-calculate all states based on current parameters
        pass


class DualCycleController():
    def __init__(self, model=None):
        self.model = DualCycleModel() if model is None else model

    def calc(self):
        self.model.update_states()

    def set_parameters(self, P0, T0, r, rc, pr, SI=True):
        # Convert units if necessary and update model parameters
        self.model.units.set(SI=SI)
        self.model.air.set(P=P0, T=T0)
        self.model.Ratio = r
        self.model.Cutoff_ratio = rc
        self.model.Pressure_ratio = pr
        self.model.update_states()

    def update_view(self):
        # Method to update the GUI based on the current state of the model
        pass
