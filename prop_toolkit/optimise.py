 # -*- coding: utf-8 -*-

import os
from math import pi

import matplotlib.pyplot as pl
import pandas as pd


from pybemt.solver import Solver

from prop_toolkit import DATA_PATH




s = Solver(os.path.join(DATA_PATH,'tmotor28.ini'))

df, sections = s.run_sweep('rpm', 20, 1000.0, 3200.0)
ax = df.plot(x='rpm', y='T') 

p = s.optimize_pitch()

print(p)

# df, sections = s.run_sweep('rpm', 20, 1000.0, 3200.0)
# df.plot(x='rpm', y='T', ax=ax) 

# pl.xlabel('RPM')
# pl.ylabel('Thrust (N)')
# pl.legend(('Baseline','Optimized'))


# pl.show()