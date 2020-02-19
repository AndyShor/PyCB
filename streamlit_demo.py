"""
this script contains simple example of charge state distribution
calculation with user interface based on streamlit package

"""
import streamlit as st
import numpy as np
from bokeh.palettes import Category20_20 as palette  # import bokeh palette for
from bokeh.models import Label
#from bokeh.plotting import figure, output_file, show
from scipy.integrate import odeint  # import odeint to integrate system of ODE
import csd

# import element data from JSON to a dictionary

ELEMENT_NAME = st.sidebar.selectbox('Select element', csd.ELEM_NAMES)
# create a dictionary with charge states as iteger keys
ELEM = csd.get_element_data(ELEMENT_NAME)

def converter(string, default):
    """
    function to convert string input to float with default alternative
    """
    try:
        value = float(string)
    except:
        value = default
    return value

# -----------------------define simulation variables

# electron energy eV
ENERGY = st.sidebar.number_input('Electron energy [eV]', value=2200)
J = st.sidebar.number_input('Electron current density [A/cm2]', value=500)
# ionization potential of rest gas
IP = st.sidebar.number_input('ionization potential [eV]', value=13.6)
P_VAC_text = st.sidebar.text_input('vacuum pressure [mbar]', value='1E-10')  # vacuum pressure mbar
P_VAC=converter(P_VAC_text,1E-10)
Log_t_lower = st.sidebar.number_input('set log₁₀ time lower time limit', value=-6)
Log_t_upper = st.sidebar.number_input('set log₁₀ time upper time limit', value=1)
show_legend=st.sidebar.checkbox('show legend', value=True, key=None)
show_labels=st.sidebar.checkbox('show labels', value=True, key=None)

ch_states_to_show=st.slider('Show charge states', min_value=0, max_value=len(ELEM), value=(0,len(ELEM)), step=1, format=None, key=None)

T_ion = 300  # ion temperature in eV
ch_states = np.linspace(0, len(ELEM), len(ELEM) + 1)  # define charge states




time = np.logspace(Log_t_lower, Log_t_upper, num=1000)  # generate  log linear time range


# below is the cached function that allows to minimize heave recalculations if only UI parameters were changed
@st.cache
def cached_solution(ELEM, J, ENERGY, T_ion, P_VAC, IP, ch_states):
    # ----- define time independent reaction rates
    rates = csd.get_reaction_rates(elem=ELEM, j_e=J, e_e=ENERGY, t_ion=T_ion, p_vac=P_VAC, ip=IP, ch_states=ch_states)
    initial_CSD = np.zeros(len(ch_states))
    initial_CSD[0] = 1
    # solve system of ODEs
    solution = odeint(csd.csd_evolution, initial_CSD, time, args=rates)

    return solution

solution=cached_solution(ELEM, J, ENERGY, T_ion, P_VAC, IP, ch_states)
csd_plot = csd.csd_base_figure()  # instantinate default CSD figure



# generate color palette for ploting
colors = [csd.color_picker(len(ch_states), i, palette) for i in range(len(ch_states))]

# populate CSD figure and legend

for i in range(ch_states_to_show[0], ch_states_to_show[1]+1, 1):
    current_color = csd.color_picker(len(ch_states), i, palette)
    csd_plot.line(time, solution[:, i], color=colors[i],
                  line_width=3, muted_alpha=0.2, muted_color=colors[i],
                  legend_label=ELEMENT_NAME+str(i)+'+')
    if show_labels:
        peak_label = Label(x=time[np.argmax(solution[:, i])], y=max(solution[:, i]) + 0.01,
                       text=str(i) + '+', text_color=colors[i])
        csd_plot.add_layout(peak_label)
if not show_legend:
    csd_plot.legend.items=[]

csd_plot.sizing_mode = 'stretch_width'
csd_plot.title.text = ELEMENT_NAME + ',  Eₑ = ' + \
                      str(round(ENERGY / 1000, 2)) + ' keV, ' + 'Jₑ=' + \
                      str(round(J, 0)) + ' A/cm², ' + 'Pᵥ=' + str(P_VAC) + ' mbar '
csd_plot.title.text_font_style = "normal"
#csd_plot.sizing_mode = 'stretch_width'
csd_plot.width = 1000
csd_plot.height = 600

#st.show(csd_plot)
st.bokeh_chart(csd_plot)