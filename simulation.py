"""
this script contains simple example of charge state distribution
calculation

"""
from datetime import datetime

import numpy as np
from bokeh.palettes import Category20_20 as palette   # import bokeh palette for
from bokeh.plotting import show
from scipy.integrate import odeint         # import odeint to integrate system of ODE
from bokeh.models import ColumnDataSource, Label, LabelSet
import numba
import csd

#uncommet for Jupyter notebook use
#from bokeh.io import push_notebook, show, output_notebook
#output_notebook()

# -----------------------define simulation variables
startTime = datetime.now()
ELEMENT_NAME = 'Au'
ELEM = csd.get_element_data(ELEMENT_NAME)
ch_states = np.linspace(0, len(ELEM), len(ELEM) + 1)  # define charge states

ENERGY = 32500  # electron energy eV
IP = 13.6  # ionization potential of rest gas
P_VAC = 1E-10  # vacuum pressure mbar
J = 5000  # A/cm2
T_ion = 300  # ion temperature in eV


# ------------------ define time independent reaction rates-----------------

rates = csd.get_reaction_rates(elem=ELEM, j_e=J, e_e=ENERGY, t_ion=T_ion, p_vac=P_VAC, ip=IP, ch_states=ch_states)

#--------------- define initial conditions and time frame----------------

initial_CSD = np.zeros(len(ch_states))
initial_CSD[0] = 1  # starts from some gas injected in a shot
# initial_CSD[1]=1   # starts from primary ion injection in 1+ charge state
timescale = np.logspace(-6, 1, num=1000)  # generate  log linear time range

#----------------------- solve system of ODEs-----------------------------------
# integrate ODE system

solution = odeint(csd.csd_evolution, initial_CSD, timescale, args=rates)


print(datetime.now() - startTime) # timing without graphic part

csd_plot = csd.csd_base_figure(add_custom_hover=False)  # instantinate default CSD figure

# generate color palette for ploting
colors = [csd.color_picker(len(ch_states), i, palette) for i in range(len(ch_states))]
#line_width=[3 for i in range(len(ch_states))]
time_list=[timescale for i in range(len(ch_states))]
#solution_list=[solution[:, i] for i in range(len(ch_states))]
solution_list=solution.T.tolist()
#print(solution_list.shape)
#legend_label=[(ELEMENT_NAME + str(i) + '+') for i in range(len(ch_states))]
x_label=[timescale[np.argmax(solution[:, i])] for i in range(len(ch_states))]
y_label=[np.amax(solution[:, i]) + 0.01 for i in range(len(ch_states))]
text_label=[ ''.join([str(i),'+']) for i in range(len(ch_states))]

multi_line_source = ColumnDataSource({
    'xs': time_list,
    'ys': solution_list,
    'color': colors,
    'x_label': x_label,
    'y_label': y_label,
    'text_label': text_label

})


lines = csd_plot.multi_line('xs', 'ys', color='color', line_width=3, legend_field='text_label',source=multi_line_source)
"""
lines = [csd_plot.line(timescale, solution[:, i], color=colors[i], line_width=3,
                       muted_alpha=0.2, muted_color=colors[i],
                  legend_label=ELEMENT_NAME + str(i) + '+') for i in range(len(ch_states))]

for i in range(len(ch_states)):
    peak_label = Label(x=timescale[np.argmax(solution[:, i])], y=max(solution[:, i]) + 0.01,
                       text=str(i) + '+', text_color=colors[i])
    csd_plot.add_layout(peak_label)
    
    
#------------------- populate CSD figure and legend---------------------------
"""
csd_plot.title.text = ''.join([ELEMENT_NAME,' CSD Evolution'])
csd_plot.add_layout(
    LabelSet(
        x='x_label',
        y='y_label',
        text='text_label',
        source=multi_line_source,
        level="overlay",
        x_offset=0,
        y_offset=0,
        render_mode="canvas",
        text_font_size="10pt",
        text_color='color',
        background_fill_color="white",
        border_line_color="white",
    )
)

csd_plot.sizing_mode='fixed'
csd_plot.width = 800
csd_plot.height = 600
show(csd_plot)
print(datetime.now() - startTime) # timing without graphic part
