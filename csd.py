"""
This script contains functions calculating atomic processes cross sections,
plotting dummy graphs and performing other routine tasks for charge

"""
import json
import numpy as np  # import numpy for general array operations
from bokeh.models import PrintfTickFormatter, HoverTool, Legend
from bokeh.plotting import figure
import numba
from numba import jit

ELEM_NAMES = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na",
              "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti",
              "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As",
              "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru",
              "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs",
              "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy",
              "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir",
              "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra",
              "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es",
              "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs"]

ELEM_MASSES = [1.0079, 4.0026, 6.941, 9.0122, 10.811, 12.0107, 14.0067, 15.9994,
               18.9984, 20.1797, 22.9897, 24.305, 26.9815, 28.0855, 30.9738, 32.065,
               35.453, 39.0983, 39.948, 40.078, 44.9559, 47.867, 50.9415, 51.9961,
               54.938, 55.845, 58.6934, 58.9332, 63.546, 65.39, 69.723, 72.64,
               74.9216, 78.96, 79.904, 83.8, 85.4678, 87.62, 88.9059, 91.224, 92.9064,
               95.94, 98, 101.07, 102.9055, 106.42, 107.8682, 112.411, 114.818, 118.71,
               121.76, 126.9045, 127.6, 131.293, 132.9055, 137.327, 138.9055, 140.116,
               140.9077, 144.24, 145, 150.36, 151.964, 157.25, 158.9253, 162.5, 164.9303,
               167.259, 168.9342, 173.04, 174.967, 178.49, 180.9479, 183.84, 186.207,
               190.23, 192.217, 195.078, 196.9665, 200.59, 204.3833, 207.2, 208.9804,
               209, 210, 222, 223, 226, 227, 231.0359, 232.0381, 237, 238.0289, 243, 244,
               247, 247, 251, 252, 257, 258, 259, 261, 262, 262, 264, 266, 268, 272, 277]

CONST = {"k_b": 1.38E-23, "q": 1.6E-19, "RT": 300, "Ry": 13.6}

@jit()
def color_picker(total_items, current_item, palette):
    """ pick color for charge states"""
    if total_items < len(palette):
        return palette[current_item]
    if total_items >= len(palette):
        return palette[current_item % len(palette)]

#just-in-time compiled function with predefined signature to speed up calculation
@jit(numba.float64(numba.int32,numba.int32,numba.float32), nopython=True)
def cx_sm_cs(i, k, ionization_potential):
    """Charge exchange cross section for single and multiple electron capture"""
    if i == 0:
        sigma = 0
    else:
        """
        see original Salborn Mueller publication
        https://doi.org/10.1016/0375-9601(77)90672-7
        """
        scaling_factor = np.array([1.43e-12, 1.08e-12, 5.5e-14, 3.57e-16])
        alpha = np.array([1.17, 0.71, 2.1, 4.2])
        beta = np.array([-2.76, -2.8, -2.89, -3.03])
        sigma = scaling_factor[k - 1] * i ** alpha[k - 1] * (ionization_potential) ** beta[k - 1]
    return sigma


def shell_stat(elem, i):
    """
    caclulations of shell statistics for RR cross section
    using effective principle quantum number approximation
    """
    if i == len(elem):  # stats for bare ion
        return [1, 2, 0]
    else:
        # electron states in shells by principal quantum number
        principal_n_states = {1: 2, 2: 8, 3: 18, 4: 32, 5: 50, 6: 72, 7: 98}
        # population of subshells by principal quantum numbers with repeats
        populations = {subshell: elem[i][subshell]['p'] for subshell in elem[i].keys()}
        # get only unique values of principal quantum number
        principal_n = set(int(k[0]) for k in populations.keys())
        # create empty dictionary for populations of shells
        principal_n_population = {k: 0 for k in principal_n}

        # populate the dictionary with actual populations from element JSON
        for k in populations.keys():
            principal_n_population[int(k[0])] = principal_n_population[int(k[0])] + populations[k]
        # get principal quantum number of last filled shell
        principal_q_number = len(principal_n_population)

        # get total number of states in that shell
        states = principal_n_states[principal_q_number]

        return [principal_q_number, states, principal_n_population[principal_q_number]]


def rr_pk_cs(elem, i, e_e):
    """
    see original publication by Kim and Pratt
    https://doi.org/10.1103/PhysRevA.27.2913"""
    nuclear_charge = len(elem)
    alpha = 1 / 137.035  # fine-structure const
    lambda_e = 3.86E-11  # electron reduced(!) Compton wavelength
    rydberg = 13.605  # Hydrogen atom ionization potential
    c_rr = 8.0 * 3.1416 / (3.0 * (3.0) ** 0.5)  # norming constant
    if i == 0:
        sigma = 0
    else:
        q_eff = 0.5 * (nuclear_charge + i)  # effective charge of the ion
        chi = 2 * q_eff ** 2 * rydberg / e_e  # chi factor
        n_outermost = shell_stat(elem, i)[0]  # principal quantum number of the outermost shell
        # statistical  weight
        wn0 = (shell_stat(elem, i)[1] - shell_stat(elem, i)[2]) / shell_stat(elem, i)[1]
        n0_eff = n_outermost + (1 - wn0) - 0.3  # effective quantum number
        # cross section
        sigma = c_rr * alpha * lambda_e ** 2 * chi * np.log(1 + chi / (2 * n0_eff ** 2))
    return sigma


def ei_lotz_cs(elem, i, e_e):
    """
    see original publication by Lotz
    https://doi.org/10.1103/PhysRevA.27.2913"""
    if i == len(elem):  # if ion is bare there is no ionization possible
        sigma = 0
    else:  # use energies and Lotz coefficients from Elemnts JSON to calculate EI CS

        condition = {subshell: (elem[i][subshell]['E'] < e_e)
                               &(elem[i][subshell]['p'] > 0)
                               &(elem[i][subshell]['E'] > 0) for subshell in elem[i].keys()}

        energies = np.array([elem[i][subshell]['E'] for subshell in elem[i].keys()
                             if condition[subshell]])
        populations = np.array([elem[i][subshell]['p'] for subshell in elem[i].keys()
                                if condition[subshell]])
        lotz_a = np.array([elem[i][subshell]['a'] for subshell in elem[i].keys()
                           if condition[subshell]])
        lotz_b = np.array([elem[i][subshell]['b'] for subshell in elem[i].keys()
                           if condition[subshell]])
        lotz_c = np.array([elem[i][subshell]['c'] for subshell in elem[i].keys()
                           if condition[subshell]])
        sigma = sum(lotz_a * (1 - lotz_b * np.exp(-1 * lotz_c * ((e_e / energies) - 1)))
                    * populations * np.log(e_e / energies) / (e_e * energies))
    return sigma * 1E-14

#Just-in-time compiled function to speed up calculation
@jit( nopython=True)
def csd_evolution(abundances, time, rei, rrr, rcx):
    """
    define RHS for time derivative system of equations"""
    matrix = np.zeros((len(abundances), len(abundances)))  # generate zero matrix
    matrix[0][0] = -(rei[0])  #
    matrix[0][1] = (rrr[1] + rcx[1])
    matrix[-1][-2] = rei[-2]
    matrix[-1][-1] = -(rrr[-1] + rcx[-1])
    for i in np.arange(1, len(abundances) - 1, 1):
        matrix[i][i - 1] = rei[i - 1]
        matrix[i][i] = -(rei[i] + rrr[i] + rcx[i])
        matrix[i][i + 1] = (rrr[i + 1] + rcx[i + 1])

    derivatives = np.dot(matrix, abundances)

    return derivatives

# use add_custom_hover=False call for plotting with bokeh multiline
def csd_base_figure(add_legend=True, add_custom_hover=True):
    """ function to make a CSD plot dummy"""
    fig = figure(width=800, height=600, sizing_mode='scale_both',
                 tools=['pan', 'box_zoom', 'reset', 'save', 'crosshair'],
                 toolbar_location='right', x_axis_type="log",
                 y_axis_type="linear", x_axis_label='time[s]',
                 y_axis_label='abundance')
    # fig.y_range = Range1d(1E-3, 1)
    fig.title.text = 'CSD Evolution'  # diagram name
    fig.title.align = 'left'  # setting layout
    fig.title.text_font_size = "14pt"
    fig.xaxis.axis_label_text_font_size = "16pt"
    fig.yaxis.axis_label_text_font_size = "16pt"
    fig.yaxis.major_label_text_font_size = "14pt"
    fig.xaxis.major_label_text_font_size = "14pt"
    fig.xaxis[0].formatter = PrintfTickFormatter(format="%4.1e")
    custom_hover = HoverTool()
    custom_hover.tooltips = """
        <style>
            .bk-tooltip>div:not(:first-child) {display:none;}
        </style>

        <b>time [s] </b> @x <br>
        <b>Relative abundance: </b> @y
    """
    if add_custom_hover:
        fig.add_tools(custom_hover)

    if add_legend:
        legend = Legend(items=[])
        fig.add_layout(legend)
        # fig.legend.title = 'charge states'
        fig.legend.location = "top_left"  # setup plot legend
        fig.legend.click_policy = "mute"
    return fig


def cs_base_figure():
    """ function to make a CS plot dummy"""
    fig = figure(width=800, height=600, sizing_mode='scale_both',
                 tools=['pan', 'box_zoom', 'reset', 'save', 'crosshair'],
                 toolbar_location='right', x_axis_type="linear",
                 y_axis_type="log", x_axis_label='charge state',
                 y_axis_label='reaction cross sections, cm²')
    fig.title.text = 'Processes cross sections, cm²'  # diagram name
    fig.title.align = 'left'  # setting layout
    fig.title.text_font_size = "14pt"
    fig.xaxis.axis_label_text_font_size = "16pt"
    fig.yaxis.axis_label_text_font_size = "16pt"
    fig.yaxis.major_label_text_font_size = "14pt"
    fig.xaxis.major_label_text_font_size = "14pt"
    fig.yaxis[0].formatter = PrintfTickFormatter(format="%4.1e")

    custom_hover = HoverTool()
    custom_hover.tooltips = """
        <style>
            .bk-tooltip>div:not(:first-child) {display:none;}
        </style>

        <b>charge state: </b> @x <br>
        <b>process rate: </b> @y
    """
    fig.add_tools(custom_hover)
    legend = Legend(items=[])
    fig.add_layout(legend)
    fig.legend.location = "top_right"  # setup plot legend
    fig.legend.click_policy = "mute"
    return fig

def get_element_data(name):
    """ import element data from JSON to a dictionary
    convert to a dictionary with charge states as iteger keys"""
    element_json = open('elements.json')
    elements_data = json.load(element_json)
    element_name = name
    # convert to a dictionary with charge states as iteger keys
    elem = {int(k): v for k, v in elements_data[element_name].items()}
    return elem


def get_neutral_density(pressure, t_gas=CONST['RT']):
    """
    returns neutral signal"""
    k_b = CONST['k_b'] # Boltzman constant
    # takes pressure in mbars
    n_0 = 100 * pressure / (k_b * t_gas) * 1E-6
    return n_0

def get_ion_velocity(elem, t_ion):
    """
    returns ion velocity in cm/s"""
    m_i = ELEM_MASSES[len(elem) - 1] * 1.6726E-27  # ion mass kg
    v_i = 100 * (8 * t_ion * 1.6E-19 / (3.1416 * m_i)) ** 0.5  # ion velocity cm/s
    return v_i


def get_reaction_rates(*, elem, j_e, e_e, t_ion, p_vac, ip, ch_states):
    """
    returs tuple of EI,RR and CX reaction rates for given conditions
    """
    q = CONST['q']  # elementary charge
    v_i = get_ion_velocity(elem, t_ion)  # ion velocity cm/s
    n_0 = get_neutral_density(p_vac)  # neutrals density per cubic cm

    rrr = j_e / q * (np.array([rr_pk_cs(elem, i, e_e) for i in ch_states]))
    rei = j_e / q * (np.array([ei_lotz_cs(elem, i, e_e) for i in ch_states]))
    rcx = n_0 * v_i * (np.array([cx_sm_cs(i, 1, ip) for i in ch_states]))

    return (rei, rrr, rcx)
