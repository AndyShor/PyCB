"""
this script contains simple example of charge state distribution
calculation

"""
import numpy as np
from bokeh.palettes import Category20_20 as palette   # import bokeh palette for
from bokeh.plotting import show
from scipy.integrate import odeint         # import odeint to integrate system of ODE
import csd

#uncommet for Jupyter notebook use
#from bokeh.io import push_notebook, show, output_notebook
#output_notebook()

# -----------------------define simulation variables
ELEMENT_NAME = 'Ar'
ELEM = csd.get_element_data(ELEMENT_NAME)
ch_states = np.linspace(0, len(ELEM), len(ELEM) + 1)  # define charge states

ENERGY = 3900  # electron energy eV
IP = 13.6  # ionization potential of rest gas
P_VAC = 1E-10  # vacuum pressure mbar
J = 1000  # A/cm2
T_ion = 300  # ion temperature in eV


# ------------------ define time independent reaction rates-----------------

rates = csd.get_reaction_rates(elem=ELEM, j_e=J, e_e=ENERGY, t_ion=T_ion, p_vac=P_VAC, ip=IP, ch_states=ch_states)

#--------------- define initial conditions and time frame----------------

initial_CSD = np.zeros(len(ch_states))
initial_CSD[0] = 1  # starts from some gas injected in a shot
# initial_CSD[1]=1   # starts from primary ion injection in 1+ charge state
time = np.logspace(-6, -1, num=1000)  # generate  log linear time range

#----------------------- solve system of ODEs-----------------------------------
# integrate ODE system

solution = odeint(csd.csd_evolution, initial_CSD, time, args=rates)
csd_plot = csd.csd_base_figure()  # instantinate default CSD figure

# generate color palette for ploting
colors = [csd.color_picker(len(ch_states), i, palette) for i in range(len(ch_states))]

#------------------- populate CSD figure and legend---------------------------

for i in range(0, len(ch_states), 1):
    current_color = csd.color_picker(len(ch_states), i, palette)
    csd_plot.line(time, solution[:, i], color=colors[i], line_width=3,
                  muted_alpha=0.2, muted_color=colors[i],
                  legend_label=ELEMENT_NAME + str(i) + '+')

"""total = np.sum(solution, axis=1)
csd_plot.line(time, total, color='black', line_width=3, muted_alpha=0.2,
              muted_color='black', legend='total')
"""
csd_plot.sizing_mode='fixed'
csd_plot.width = 800
csd_plot.height = 600
show(csd_plot)
