 # -*- coding: utf-8 -*-

import os
from math import pi

import matplotlib.pyplot as pl
import pandas as pd


from pybemt.solver import Solver

from prop_toolkit import DATA_PATH



s = Solver(os.path.join(DATA_PATH,'propeller.ini'))

df, sections = s.run_sweep('twist', 20, 0, 20)

#df_exp = pd.read_csv("propeller_data.csv", delimiter=' ')

ax = df.plot(x='twist', y='eta', legend=None) 
#df_exp.plot(x='J',y='eta',style='C0o',ax=ax, legend=None)
#pl.legend(('BEMT, $\eta$','Exp, $\eta$'),loc='center left')

pl.ylabel('$\eta$')
ax2 = ax.twinx()
pl.ylabel('$C_P, C_T$')

df.plot(x='twist', y='CP', style='C1-',ax=ax2) 
#df_exp.plot(x='J',y='CP',style='C1o',ax=ax2, legend=None)

df.plot(x='twist', y='CT', style='C2-',ax=ax2) 
#df_exp.plot(x='J',y='CT',style='C2o',ax=ax2, legend=None)



pl.show()