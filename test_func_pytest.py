"""
this script contains set of unit tests for PyCB
unit test check basic functionality as well as
compare output of CSD.py functions against known reference numbers
"""
import pytest
#from bokeh.io import curdoc
import numpy as np
import csd


def test_hydrogen():
    """test importing data from elements.json"""
    elem = csd.get_element_data('H')
    assert elem[0]['1s']['E'] == pytest.approx(13.5984487)

"""
def test_csd_plot():
    #test dummy CSD plot generation
    csd_plot = csd.csd_base_figure()
    curdoc().add_root(csd_plot)
    figure_json = curdoc().to_json()
    # figure_dict=json.loads(figure_json)
    print(figure_json.keys())
    for i in range(len(figure_json['roots']['references'])):
        # print(figure_json['roots']['references'][i])
        if figure_json['roots']['references'][i]['type'] == 'LogAxis':
            log_axis_label = (figure_json['roots']['references'][i]['attributes']['axis_label'])

    curdoc().remove_root(csd_plot)
    assert log_axis_label == 'time[s]'


def test_cs_plot():
    #test dummy CS plot generation
    cs_plot = csd.cs_base_figure()
    curdoc().add_root(cs_plot)
    figure_json = curdoc().to_json()
    # figure_dict=json.loads(figure_json)
    print(figure_json.keys())
    for i in range(len(figure_json['roots']['references'])):
        # print(figure_json['roots']['references'][i])
        if figure_json['roots']['references'][i]['type'] == 'LinearAxis':
            linear_axis_label = (figure_json['roots']['references'][i]['attributes']['axis_label'])
    curdoc().remove_root(cs_plot)
    assert linear_axis_label == 'charge state'
"""


def test_mo_ei_watanabe():
    """based on Watanabe value  on H-like Molybdenum
    check if deviation by Lotz formula from experiemntal
    value exceeds error bars specified by Lotz
    """
    elem = csd.get_element_data('Mo')
    e_e = 64400
    watanabe__ei = csd.ei_lotz_cs(elem, 41, e_e)
    print('Error Watanabe Mo', abs(watanabe__ei - 3.13E-23) / 3.13E-23)
    assert abs(watanabe__ei - 3.13E-23) / 3.13E-23 < 0.3


def test_rr_marrs():
    """based on Marrs experiemntal RR CSs
    reference RR cross section represented as
    [charge state, electron energy, reference cross section cm2]"""
    rr_reference = {
        'Mo': [[42, 31500, 90.33E-24], [42, 36100, 72.39E-24],
               [42, 64800, 26.56E-24], [42, 95600, 13.01E-24]]}
    elem = csd.get_element_data('Mo')
    error_list = [abs(csd.rr_pk_cs(elem, case[0], case[1])- case[2])/case[2]
                  for case in rr_reference['Mo']]
    mean_error = sum(error_list) / len(error_list)
    print('Mean error RR Marrs Mo', mean_error)
    assert mean_error < 0.3


def test_ei_marrs():
    """ based on Marrs experimental EI CSs
    # reference EI cross section represented as
    # [charge state, electron energy, reference cross section cm2]"""
    ei_reference = {'Mo': [[41, 31500, 15.9E-24], [41, 36100, 21.2E-24],
                           [41, 64800, 30.8E-24], [41, 95600, 34.7E-24]]}

    error_list = []
    elem = csd.get_element_data('Mo')
    error_list = [abs(csd.ei_lotz_cs(elem, case[0], case[1]) - case[2]) / case[2]
                  for case in ei_reference['Mo']]
    mean_error = sum(error_list) / len(error_list)
    print('Mean error EI Marrs Mo', mean_error)
    assert mean_error < 0.3


def test_rr_trzhaskovskaya():
    """"
    based on Trzhaskovskaya calculated RR CSs
    reference RR cross section represented as
    [charge state, electron energy, reference cross section cm2]"""
    rr_reference = {
        'Fe': [[8, 2964.00, 1.040E-23], [8, 9645.96, 1.1780E-24],
               [8, 15464.38, 4.797E-25], [8, 31391.56, 1.2E-25],
               [8, 50326.87, 4.632E-26],
               [16, 2964.00, 5.267E-23], [16, 9645.96, 6.551E-24], [16, 15464.38, 2.698E-24],
               [16, 31391.56, 6.786E-25], [16, 50326.87, 2.622E-25],
               [24, 2964.00, 2.304E-22], [24, 9645.96, 3.022E-23], [24, 15464.38, 1.268E-23],
               [24, 31391.56, 3.261E-24], [24, 50326.87, 1.272E-24],
               [26, 2964.00, 7.076E-22], [26, 9645.96, 1.291E-22], [26, 15464.38, 6.088E-23],
               [26, 31391.56, 1.790E-23], [26, 50326.87, 7.427E-24]]}
    elem = csd.get_element_data('Fe')
    error_list = [abs(csd.rr_pk_cs(elem, case[0], case[1]) - case[2]) / case[2]
                  for case in rr_reference['Fe']]
    mean_error = sum(error_list) / len(error_list)
    print('Mean error RR_Trzhaskovskaya', mean_error)
    assert mean_error < 0.3


def test_cx_kravis():
    """based on Kravis data on CX cross sections"""
    cx_ref = {'Ar': [[6, 7.05E-15], [7, 8.93E-15], [8, 7.54E-15],
                     [9, 12.1E-15], [11, 20.5E-15]]}
    error_list = []
    error_list = [abs(csd.cx_sm_cs(case[0], 1, 13.6) - case[1]) / case[1]
                  for case in cx_ref['Ar']]
    mean_error = sum(error_list) / len(error_list)
    print('mean Kravis CX error', mean_error)
    assert mean_error < 0.3


def test_csd_evolution():
    """ test correctness of CSD evolution calculation based
     on simplified example, returned value of time derivatives
      is compared to a test answer"""
    max_charge = 9
    test_result = np.array([-1., 0., 0., 0., 0., 0., 0., 0., 0., 1.])
    ch_states = np.linspace(0, max_charge, max_charge + 1)
    rcx = np.zeros(len(ch_states))
    rrr = np.zeros(len(ch_states))
    rei = 1 * np.ones(len(ch_states))
    csd_derivatives = csd.csd_evolution(np.ones(len(ch_states)), 0, rei, rrr, rcx)

    assert np.linalg.norm(csd_derivatives - test_result) < 1E-6


def test_element_stat():
    """
    based on Watanabe and Marrs papers on H-like Molybdenum"""
    elem = csd.get_element_data('Ar')
    shell_data = csd.shell_stat(elem, 0)
    assert shell_data == [3, 18, 8]

def test_neutral_density():
    """
    test for calculations of neutral density gas molecules per cubic cm
    """
    temperature = 300 #K
    pressure = 1 #mbar
    k_b = 1.38E-23
    neutrals = 100 * pressure / (k_b * temperature) * 1E-6
    assert neutrals == pytest.approx(csd.get_neutral_density(pressure=pressure, t_gas=temperature))

def test_ion_velosity():
    """
    test of ion velocity calculations
    """
    m_hydrogen = 1.0079*1.6726E-27  # ion mass kg, accout for Deuterium fraction!
    t_hydrogen = 100 #eV
    elem = csd.get_element_data('H')
    # ion velocity cm/s
    velocity_hydrogen = 100 * (8 * t_hydrogen * 1.6E-19 / (3.1416 * m_hydrogen)) ** 0.5
    assert velocity_hydrogen == pytest.approx(csd.get_ion_velocity(elem, t_hydrogen))

def test_rates():
    """
    test to verify correct calculation of reaction rates
    on axample of Helium
    """
    element_name = 'He'  # specify element to study by name
    # convert element data to a dictionary with charge states as iteger keys
    elem = csd.get_element_data(element_name)
    ionization_potential = csd.CONST["Ry"]  # ionization potential of rest gas
    # ----------------define simulation variables---------------
    e_e = 100  # electron energy eV
    p_vac = 1E-10  # vacuum pressure mbar
    t_ion = 100  # ion temperature in eV
    j_e = 100  # A/cm2
    ch_states = np.linspace(0, len(elem), len(elem) + 1)  # define charge states
    # ----- -----define time independent reaction rates----------------------

    rates = csd.get_reaction_rates(elem=elem, j_e=j_e, e_e=e_e,
                                   t_ion=t_ion, p_vac=p_vac,
                                   ip=ionization_potential, ch_states=ch_states)
    test_values = [[26417.58181096, 1746.13008181, 0.0], [0.0, 0.00387869, 0.02672259],
                   [0.0, 0.02004152, 0.04509577]]
    flat_list_test = [item for sublist in test_values for item in sublist]
    func_list = [rates[0], rates[1], rates[2]]
    func_flat_list = [item for sublist in func_list for item in sublist]

    assert all(a == pytest.approx(b) for a, b in zip(func_flat_list, flat_list_test))
