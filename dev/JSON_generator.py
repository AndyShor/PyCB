import json
import numpy as np


name_list = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K",
             "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb",
             "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs",
             "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta",
             "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa",
             "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs"]

subshell_list = ["1s", "2s", "2p-", "2p+", "3s", "3p-", "3p+", "3d-", "3d+", "4s", "4p-", "4p+", "4d-", "4d+", "5s",
                 "5p-", "5p+", "4f-", "4f+", "5d-", "5d+", "6s", "6p-", "6p+", "5f-", "5f+", "6d-", "6d+", "7s"]

# see Lotz https://doi.org/10.1007/BF01393132
Lotz_coefficients = {"1s": [[4, 0.6, 0.56], [4, 0.75, 0.50]],
                     "2s": [[4, 0.3, 0.6], [4, 0.5, 0.60]],
                     "2p": [[3.8, 0.6, 0.4], [3.5, 0.7, 0.3], [3.2, 0.8, 0.25], [3.0, 0.85, 0.22], [2.8, 0.9, 0.20],
                            [2.6, 0.92, 0.19]],
                     "3s": [[4, 0.0, 0.0], [4, 0.3, 0.60]],
                     "3p": [[4, 0.35, 0.6], [4, 0.4, 0.6], [4, 0.45, 0.6], [4, 0.5, 0.5], [4, 0.55, 0.45],
                            [4, 0.6, 0.4]],
                     "3d": [[3.7, 0.6, 0.4], [3.4, 0.7, 0.3], [3.1, 0.8, 0.25], [2.8, 0.85, 0.2], [2.5, 0.9, 0.18],
                            [2.2, 0.92, 0.17], [2.0, 0.93, 0.16], [1.8, 0.94, 0.15], [1.6, 0.95, 0.14],
                            [1.4, 0.96, 0.13]],
                     "4s": [[4, 0, 0], [4, 0, 0]],
                     "4p": [[4, 0, 0], [4, 0, 0], [4, 0.2, 0.6], [4, 0.3, 0.6], [4, 0.4, 0.6], [4, 0.5, 0.5]],
                     "4d": [[4, 0.3, 0.6], [3.8, 0.45, 0.5], [3.5, 0.6, 0.4], [3.2, 0.7, 0.3], [3.0, 0.8, 0.25],
                            [2.8, 0.85, 0.2], [2.6, 0.9, 0.18], [2.4, 0.92, 0.17], [2.2, 0.93, 0.16],
                            [2.0, 0.94, 0.15]],
                     "5s": [[4, 0, 0], [4, 0, 0]],
                     "5p": [[4, 0, 0], [4, 0, 0], [4, 0.2, 0.6], [4, 0.3, 0.6], [4, 0.4, 0.6], [4, 0.5, 0.5]],
                     "4f": [[3.7, 0.6, 0.4], [3.4, 0.7, 0.3], [3.1, 0.8, 0.25], [2.8, 0.85, 0.2], [2.5, 0.9, 0.18],
                            [2.2, 0.92, 0.17], [2.0, 0.93, 0.16], [1.8, 0.94, 0.15], [1.6, 0.95, 0.14],
                            [1.4, 0.96, 0.13], [1.3, 0.96, 0.12], [1.2, 0.97, 0.12], [1.1, 0.97, 0.11],
                            [1.0, 0.97, 0.11]],
                     "5d": [[4, 0, 0], [4, 0.2, 0.6], [3.8, 0.3, 0.6], [3.6, 0.45, 0.5], [3.4, 0.6, 0.4],
                            [3.2, 0.7, 0.3], [3.0, 0.8, 0.25], [2.8, 0.85, 0.2], [2.6, 0.9, 0.18], [2.4, 0.92, 0.17]],
                     "6s": [[4, 0, 0], [4, 0, 0]],
                     "6p": [[4, 0, 0], [4, 0, 0], [4, 0.2, 0.6], [4, 0.3, 0.6], [4, 0.4, 0.6], [4, 0.5, 0.5]],
                     "5f": [[3.7, 0.6, 0.4], [3.4, 0.7, 0.3], [3.1, 0.8, 0.25], [2.8, 0.85, 0.2], [2.5, 0.9, 0.18],
                            [2.2, 0.92, 0.17], [2.0, 0.93, 0.16], [1.8, 0.94, 0.15], [1.6, 0.95, 0.14],
                            [1.4, 0.96, 0.13], [1.3, 0.96, 0.12], [1.2, 0.97, 0.12], [1.1, 0.97, 0.11],
                            [1.0, 0.97, 0.11]],
                     "6d": [[4, 0, 0], [4, 0.2, 0.6], [3.8, 0.3, 0.6], [3.6, 0.45, 0.5], [3.4, 0.6, 0.4],
                            [3.2, 0.7, 0.3], [3.0, 0.8, 0.25], [2.8, 0.85, 0.2], [2.6, 0.9, 0.18], [2.4, 0.92, 0.17]],
                     "7s": [[4, 0, 0], [4, 0, 0]]}

subshells = []

def charge_state_dict(Z, q):
    charge_state_dict = {}

    ip_filename = 'data/' + str(Z) + '.txt'
    ip_datafile = open(ip_filename)
    ip_databuffer = ip_datafile.readlines()
    charge_state_line = ip_databuffer[q + 1]
    charge_state_buffer = charge_state_line.split('	')

    conf_filename = 'data/' + str(Z) + 'conf.txt'
    conf_datafile = open(conf_filename)
    conf_databuffer = conf_datafile.readlines()
    populations_line = conf_databuffer[q]
    populations_buffer = populations_line.split('	')
    principal_subshells = set([subshell_list[i][:2] for i in range(len(charge_state_buffer))])
    # print(principal_subshells)
    electron_formula = {k: 0 for k in principal_subshells}
    # print(electron_formula)

    total_charge = 0
    for i in range(len(charge_state_buffer)):
        charge_state_dict[subshell_list[i]] = {"E": float(charge_state_buffer[i]), "p": int(populations_buffer[i])}
        electron_formula[subshell_list[i][:2]] = electron_formula[subshell_list[i][:2]] + int(populations_buffer[i])
        total_charge += int(populations_buffer[i])
    # print(electron_formula)
    if total_charge + q != Z:
        print('Error in data for', Z, q)
        print('Population summ=', total_charge)
        print(electron_formula)
    for i in range(len(charge_state_buffer)):
        if q <= 4:
            charge_state_dict[subshell_list[i]]["a"] = \
            Lotz_coefficients[subshell_list[i][:2]][electron_formula[subshell_list[i][:2]] - 1][0]
            charge_state_dict[subshell_list[i]]["b"] = \
                Lotz_coefficients[subshell_list[i][:2]][electron_formula[subshell_list[i][:2]] - 1][1]
            charge_state_dict[subshell_list[i]]["c"] = \
                Lotz_coefficients[subshell_list[i][:2]][electron_formula[subshell_list[i][:2]] - 1][2]
        else:
            charge_state_dict[subshell_list[i]]["a"] = 4.5
            charge_state_dict[subshell_list[i]]["b"] = 0
            charge_state_dict[subshell_list[i]]["c"] = 0

    return charge_state_dict


json_dict = {}
for Z in range(1, 95, 1):
    name = name_list[Z - 1]
    print(name, Z)
    charge_states = {}

    for n in range(Z):
        data_dict = {}
        charge_states[str(n)] = charge_state_dict(Z, n)
        # print(str(n))
    json_dict[name] = charge_states

    print(len(json_dict[name]))

with open('elements.json', 'w') as fp:
    json.dump(json_dict, fp)
