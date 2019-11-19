
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndyShor/PyCB/master?filepath=CSD_notebook_app.ipynb)

**About**

This simulation and visualization toolkit provides tools to simulate Charge State Distribuion
of ions in Multiply Charged Ion sources ( see for example [Gammino](https://arxiv.org/pdf/1410.7974.pdf)) such Electron Beam Ion Source (EBIS, see for example [Zschornack](https://cds.cern.ch/record/1965922/files/CERN-2013-007-p165.pdf)) or Electron Cyclotron Resonance Ion Source (ECRIS).

Presently there are several isolated legacy projects of this kind, some very specialised, many not maintained or abandoned,
written in languages with shrinking user base such as Fortran, oftentimes lacking systematic tests.
There are also proprietary packages such as CHASER by [Zhao](http://dx.doi.org/10.1063/1.4934686) , which seems inactive  (poke [Far-tech](https://www.far-tech.com/chaser.php)).

This  work means to  serve the role of CBSIM by [Becker](https://dx.doi.org/10.1088/1742-6596/58/1/102) - the basic, free and open source tool.
This toolkit is designed to be used mostly with Jupyter notebooks, or as a deployable Panel-based web application, see **How to use** section.
For more  programming-like OOP-style solution have a look at ebisim Python module by Hannes Pahl ([Pahl](https://github.com/HPLegion/ebisim)).

This toolkit prioritizes transparency, simplicity and ease of use.
We also pay attention to cross checking of obtained data against known reference values (see **unit tests** section)
In present state we focus only on first order processes such as:

*single impact ionization (using full Lotz cross sections [[Lotz1](https://doi.org/10.1007/BF01325928), [Lotz2](https://doi.org/10.1007/BF01392963)] and FAC ionization potentials). This approach gives systemativ underestimation of cross-sectios for high-Z (Z=50+) very highly charged ions such as Bi 82+ due to complex relativistic effects.
Even general relativistic distorted wave calculations do not catch the difference unless fine effects such as Mdller interaction is included. We recommend for relevant cases
to consult [Moores and Reed](https://dx.doi.org/10.1103/PhysRevA.51.R9) and if needed introduce correction factors to Lotz function

*radiative recombination (using Kim and Pratt approximation [KimPratt](https://doi.org/10.1103/PhysRevA.27.2913))

*charge exchange (using Mueller-Salzborn approximation [MuellerSalzborn](https://https://www.sciencedirect.com/science/article/abs/pii/0375960177906727?via%3Dihub)

By the extent of included processes this toolkit is similar to widely used CBSIM by R. Becker [[Becker1](https://dx.doi.org/10.1088/1742-6596/58/1/102)],
but expands it and allows users not familiar with Fortran to understand and customize it.

The expansion compared to CBSIM includes use of full Lotz formula and availability of all elements.
For expandability and customization reasons we provide isolated data-set in human-redable JSON format covering essential parameters of elements such as:
*ionization potentials calculated with Flexible Atomic Code (FAC by [Gu](https://doi.org/10.1139/p07-197)) by [Mertzig](https://project-ionpotentials.web.cern.ch/project-Ionpotentials/) at CERN. 
*populaions of subshells calculated with Flexible Atomic Code (FAC by [Gu](https://doi.org/10.1139/p07-197)) by [Mertzig](https://project-ionpotentials.web.cern.ch/project-Ionpotentials/).
*Lotz coefficients for various shells based on publication by Lotz[[Lotz2](https://doi.org/10.1007/BF01392963)]

We omit higher order processes such as double ionization, double charge exchange, ionization heatig, 
not complete overlap of ion and electron beams in Electron Beam Ion Sources (EBIS).
We also omit such phenomena as gas cooling and ion-ion energy exchange as well as resonant phenomena such as Dielectronic Recombination.
As all universally used cross section formulas have error bars in the +40/-30 % it is of marginal use to tune second order effects.
The benefit may come for more specialized cases, where cross section information is better defined. 

Presently there is no plan to incorporate these processes in the future, for more feature-rich simulations we recommend to watch for development of ebisim,
where some of it is realized (such as Dielectronic recombination) and some might come in the future. For those who want to develop comprehensive model including all related processes we recommend to have a look at  published works of [Kalagin](https://doi.org/10.1088/0963-0252/7/4/002), [Penetrante](https://doi.org/10.1103/PhysRevA.43.4861) and [Currell and Fussmann](https://doi.org/10.1109/TPS.2005.860072).

#How to use

##What is included
The toolkit includes several essential components such as:
*elements.json - file with elements data

*dev folder contains raw data from FAC simulations and a python script to bundle them into json, not required for regular use

*screenshots folder conatins screen shots of user interface options

*csd.py - a file with basic functions such as calculating interaction cross sections or generating plot templates

*reqirements - a file with dependencies. This file also includes dependencies of optional UI's such as Panel and streamlit

*simulation.py - an example simulation in pure python code without any user interface

*CSD_notebook_online.ipynb - Jupyter notebook for interactive simulation no specific UI. Can be used without any python installation using Binder link at the top.

*CSD_notebook_app.ipynb - Jupter notebook which provides either rich user controls in the notebook or a deployable web application.
Can be tested without any python installation using Binder link at the top.

*streamlit_demo.py - a python script that provides rich user UI based on streamlit package see below.

*test_func_pytest.py - a collection of unit test checking toolkit integrity and comparing cross section functions to known reference values. Run tests if modified anything.


##Dependencies.

For proper use it is required to install the following packages
*numpy - for basic array hadlig
*scipy - for ODE integration
*json - for parsing element data
*bokeh - for creating plots
*pytest - for running unit test assuring toolkit integrity and checking against literature reference values

*panel - one of the UI alternatives, optional
*streamlit - second UI alternative, optional

##Installation

 in your Python installation create a virtual environment to avoid conflicts of libraries with the existig installations using venv
 venv will create a virtual Python installation in the env folder
 on Linux and MacOS
>> python3 -m venv env
On Windows
>> py -m venv env


Activate new environmet
on Linux and MacOS
>> source env/bin/activate

On Windows
>> .\env\Scripts\activate

with activated virtual environment install dependencies in the virtual environment by

>> pip install -r requirements.txt

To run notebook with Panel app having UI in the notebook use it as is with Jupyter
To run notebook with Panel app as a web application change commenting of the last string from using method servable() to use show()
To run notebook app as a web application accessible from outside of localhost start  Panel with proper permissions such as whitelisting of acceptable request origins or allowing them for all such as

>>

Caution! While Panel claims to not allow execution of external code its level of security is not exactly designed to face exposure to the Internet,
but rather to stay within comfort of protected internal networks inhabited by good mannered users.

user interface example is given on the screenshot below

![bokeh app screenshot](/screenshots/Bokeh_app_screenshot.png | width=800)



To run streamlit_demo.py first install streamlit (not in reqquirements.txt, tested on streamlit 0.49) use

>> pip install streamlit

>>streamlit run streamlit_demo.py 

user interface example is given on the screenshot below

![bokeh app screenshot](/screenshots/streamlit_app_screenshot.png | width=800)


##Core functionality
functions and data structures in CSD.py

**Element dictionary**. Element information related to ionization process is stored in elements.json file
For simulation json file is parsed and information about a unique element is extracted based on element name as a key.
Element information is contained in a dictioary of dictionnaries organized in the following way:
{charge state:{'subshell':{"E": subshell ionization energy, "p": subshell population, "a": Lotz coefficient 'a' in 1E-14 sq cm units, "b": Lotz coefficient 'b', "c": Lotz coefficient 'c'}}}. Subshells with non-zero orbital momentum are divided to + and - due to minor difference in the ionization energy.
Ionization energies are calculated using FAC by [Mertzig](https://project-ionpotentials.web.cern.ch/project-Ionpotentials/). Populations of subshells are calculated using FAC code by [Mertzig](https://project-ionpotentials.web.cern.ch/project-Ionpotentials/). Lotz coefficients for subshells are taken from [[Lotz2](https://doi.org/10.1007/BF01392963)], for charge states above 4 universal values of a=4.5 b=0 c=0 used according to [[Lotz2](https://doi.org/10.1007/BF01392963)]. Charge states vary from neutral (0) to charge state with 1 left electron (last). Thus length of this dictionary is equal to nuclear charge and may be used as its proxy.
For ease of handling charge state key is converted from string format as provided by json parsing to integer.


**cx_sm_cs**(i,k, IP)
calculates Charge eXchange (CX) cross-section of an ion with charge state i to pick up k electrons from a neutral target atom with ionization potential IP.
calculation uses classical Mueller and Salzborn approximation. In their original work Mueller and Salzborn specify +/- 30% error bar
CX cross section of neutral atom is =0 for ease of vectorization.

**rr_pk_cs**(elem,i, e_e)
calculates Radiative Recombination cross section for element characterized by elem dictionary, in charge state i for electron energy e_e
Calculation uses Pratt and Kim approximate formula. The fromula requires some data on population of subshells. This information is provided by
auxiliary funtion shell_stat(Elem,i)
RR cross section of neutral atom is =0 for ease of vectorization.

**shell_stat**(elem,i)
for element described by element disctionary elem in charge state i returns a list with three values
value number 0 - principal quantum number of the last filled shell
value number 1 - total number of states in the last filled shell
value number 2 - number of filled states i that shell

**ei_lotz_cs**(elem,i, e_e)
Calculates Electro Impact ionization (EI) cross section for an element described in dictionary elem in charge state i impacted by an electron with energy e_e.
Calculation uses full Lotz formula with Lotz coefficients specific for each shell stored in Elem dictionary. 
In his original work Lotz specifies +/- 30-40% error bar
EI cross section of bare nucleous is =0 for ease of vectorization.

**csd_evolution**(y,t, rei,rrr,rcx)
Calculates Right Hand Side (RHS) for system of Ordinary Differential Equations (ODE) describing dynamics of Charge State Distribution (CSD).
takes as as arguments:
y - vector of charge states abundances
t- time
rei - vector of EI rates (not cross section!)
rrr - vector of RR rates (not cross section!)
rcx - vector of RCX rates (not cross section!)

returns values of time derivatives of charge state abundances at the given time.
This function is used in scipy routine for ODE integration. If modifying keep in mind that this function will be called on each time step,
vectorization and use of numpy arrays highly recommended for smooth UI for heavy ions with tens of charge states when matrixes get large.


**csd_base_figure**(add_legend=True)
returns a bokeh figure object with formattig preset for CSD display. Optional argument allows to enable and disable creation of empty legend and setting its format.
There are uit test aiming to verify proper creation of the plot template. These tests look at the bokeh figure object properties to make sure that the object is created properly. If properties such as axis titles will be changed those tests will fail. It will not have impact on performance, but may be misleading.

**cs_base_figure**(add_legend=True)
returns a bokeh figure object with formattig preset for CSD display. Optional argument allows to enable and disable creation of empty legend and setting its format.
There are uit test aiming to verify proper creation of the plot template. These tests look at the bokeh figure object properties to make sure that the object is created properly. If properties such as axis titles will be changed those tests will fail. It will not have impact on performance, but may be misleading.


##Unit tests included in the toolkit.

**test_hydrogen()** test correct importing from elements.json on an example of Hydrogen, test passed if correct ionization energy is provided by readout

**test_csd_plot()** test correct creation of dummy CSD plot, looks at bokeh plot attributes, test passed if log_axis_label is set to'time[s]'

**test_cs_plot()**  test correct creation of dummy Cross sections plot, looks at bokeh plot attributes, test passed if linear_axis_label is set to 'charge state'

**test_mo_ei_watanabe()** test error bars of Lotz cross section versus experimental data on example of H-like Mo from 
[Watanabe](https://doi.org/10.1088/0953-4075/35/24/311)  passed if error below 30% (error specified by Lotz, in present built error about 12%)

**test_ei_marrs()** test error bars of Lotz cross section versus experimental data on example of H-like Mo from [Marrs](https://doi.org/10.1103/PhysRevA.56.1338)
 passed if error below 30% (error specified by Lotz, in present built error about 13%)

**test_rr_marrs()** test correctness of RR cross sections versus experiemntal values for RR recombination of bare Mo to H-like Mo, based on [Marrs](https://doi.org/10.1103/PhysRevA.56.1338) experimental data, test passed if mean error below 30% ( in present built averaged error about 17%)

**test_w_rr_trzhaskovskaya()** test correctness of RR cross section versus sophisticated theoretical values by [Trzhaskovskaya](https://dx.doi.org/10.1016/j.adt.2007.09.002),
on example of Fe in charge tsates 8,16,24,26 for electron energies 2964, 9646, 15464, 31392, 50327 eV, test passed if average error over these 20 cases is below 30%
( in present built averaged error about 25%)

**test_cx_kravis()** test correctness of CX cross sections versus experimental data for Ar6+,Ar7+,Ar8+,Ar9+, Ar11+ in H2 reported by [Kravis](https://doi.org/10.1103/PhysRevA.52.1206). highest energy values from Kravis used for test to make comparison to Salzborn-Mueller comply with assumptions of SM model and the data they originally fitted. Test is passed if average error over test cases is below 30% ( in present built averaged error about 26%)


**test_csd_evolution()** test correctness of CSD evolution calculation based on simplified example, returned value of time derivatives is compared to a test answer.

**test_element_stat()** test shell stat function on example of Argon

**test_test_neutral_density()** test correct calculation of neutral gas density on example of 1 mbar of gas at 300 K

**test_ion_velosity()** test correct calculation of ion velocity in cm/s on example of Hydrogen ions at 100 eV temperature (p and D in natural abundance) 

**test_rates()** test correct calculation of reaction rates on example of He and 100 eV 100 A/cm2 electron beam






#References

[Becker](https://dx.doi.org/10.1088/1742-6596/58/1/102)

[Currell and Fussmann](https://doi.org/10.1109/TPS.2005.860072)

[Far-tech](https://www.far-tech.com/chaser.php)

[Gammino](https://arxiv.org/pdf/1410.7974.pdf)

[Gu](https://doi.org/10.1139/p07-197)

[Kalagin](https://doi.org/10.1088/0963-0252/7/4/002)

[KimPratt](https://doi.org/10.1103/PhysRevA.27.2913)

[Kravis](https://doi.org/10.1103/PhysRevA.52.1206)

[Lotz1](https://doi.org/10.1007/BF01325928)

[Lotz2](https://doi.org/10.1007/BF01392963)

[Marrs](https://doi.org/10.1103/PhysRevA.56.1338)

[Moores and Reed](https://dx.doi.org/10.1103/PhysRevA.51.R9)

[MuellerSalzborn](https://https://www.sciencedirect.com/science/article/abs/pii/0375960177906727?via%3Dihub)

[Pahl](https://github.com/HPLegion/ebisim)

[Penetrante](https://doi.org/10.1103/PhysRevA.43.4861)

[Trzhaskovskaya](https://dx.doi.org/10.1016/j.adt.2007.09.002)

[Watanabe](https://doi.org/10.1088/0953-4075/35/24/311)

[Zhao](http://dx.doi.org/10.1063/1.4934686)

[Zschornack](https://cds.cern.ch/record/1965922/files/CERN-2013-007-p165.pdf)



