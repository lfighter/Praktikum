from table import makeTable
from bereich import bereich
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp

# ALLES---------------------------------------------------------------------------------


def betrag(x):
    return unp.sqrt(x**2)

vNull = 16594

# Vmessung------------------------------------------------------------------------------
Gang, timeForwards, timeBackwards = np.genfromtxt('scripts/Vmessung', unpack=True)
LaengeDerStrecke = 445

ForwardsV = []
for i in range(1, 11):
    ForwardsV.append(LaengeDerStrecke / unp.uarray(np.mean(timeForwards[Gang == i*6]), stats.sem(timeForwards[Gang == i*6])))
ForwardsV = np.array(ForwardsV)

BackwardsV = []
for i in range(1, 11):
    BackwardsV.append(LaengeDerStrecke / unp.uarray(np.mean(timeBackwards[Gang == i*6]), stats.sem(timeBackwards[Gang == i*6])))
BackwardsV = np.array(BackwardsV)

print(ForwardsV)
print(BackwardsV)


# Dopplereffektmessung------------------------------------------------------------------

Gang, frequenzForwards, frequenzBackwards = np.genfromtxt('scripts/dopllereffektmessung', unpack=True)
frequenzForwards[Gang==6] = frequenzForwards[Gang==6]/10
frequenzBackwards[Gang==6] = frequenzBackwards[Gang==6]/10

Forwards = []
for i in range(1, 11):
	Forwards.append(unp.uarray(np.mean(frequenzForwards[Gang==i*6]), stats.sem(frequenzForwards[Gang==i*6])))
Forwards = np.array(Forwards)

Backwards = []
for i in range(1, 11):
	Backwards.append(unp.uarray(np.mean(frequenzBackwards[Gang==i*6]), stats.sem(frequenzBackwards[Gang==i*6])))
Backwards = np.array(Backwards)

print(Forwards)
print(Backwards)

# DeltaVKursiv--------------------------------------------------------------------------
DeltaVForwards = []
for value in Forwards:
    DeltaVForwards.append(betrag(value-vNull))
DeltaVForwards = np.array(DeltaVForwards)

DeltaVBackwards = []
for value in Backwards:
    DeltaVBackwards.append(betrag(value-vNull))
DeltaVBackwards = np.array(DeltaVBackwards)

print(DeltaVForwards)
print(DeltaVBackwards)

# PlotVonDeltaVKursivGegenV-------------------------------------------------------------
ForwardsVNominal = []
ForwardsVStd = []
for value in ForwardsV:
    ForwardsVNominal.append(unp.nominal_values(value))
    ForwardsVStd.append(unp.std_devs(value))
ForwardsVNominal = np.array(ForwardsVNominal)
ForwardsVStd = np.array(ForwardsVStd)

BackwardsVNominal = []
BackwardsVStd = []
for value in BackwardsV:
    BackwardsVNominal.append(unp.nominal_values(value))
    BackwardsVStd.append(unp.std_devs(value))
BackwardsVNominal = np.array(BackwardsVNominal)
BackwardsVStd = np.array(BackwardsVStd)

VNominal = np.append(ForwardsVNominal, BackwardsVNominal)


DeltaVForwardsNominal = []
DeltaVForwardsStd = []
for value in DeltaVForwards:
    DeltaVForwardsNominal.append(unp.nominal_values(value))
    DeltaVForwardsStd.append(unp.std_devs(value))
DeltaVForwardsNominal = np.array(DeltaVForwardsNominal)
DeltaVForwardsStd = np.array(DeltaVForwardsStd)

DeltaVBackwardsNominal = []
DeltaVBackwardsStd = []
for value in DeltaVBackwards:
    DeltaVBackwardsNominal.append(unp.nominal_values(value))
    DeltaVBackwardsStd.append(unp.std_devs(value))
DeltaVBackwardsNominal = np.array(DeltaVBackwardsNominal)
DeltaVBackwardsStd = np.array(DeltaVBackwardsStd)

DeltaVNominal = np.append(DeltaVForwardsNominal, DeltaVBackwardsNominal)



def line(x, a):
    return a*x


params, covar = curve_fit(line, VNominal, DeltaVNominal, maxfev=1000)
print(params, covar, sep='\n')

t = np.linspace(0, ForwardsVNominal[-1]*1.03, 1000)
plt.cla()
plt.clf()
plt.plot(t, line(t, *params), 'b-', label='Fit')
plt.plot(ForwardsVNominal, DeltaVForwardsNominal, 'gx', label='Forwards')
plt.plot(BackwardsVNominal, DeltaVBackwardsNominal, 'rx', label='Backwards')
plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(0, t[-1])
plt.xlabel(r'v$/\si{\meter\per\second}$')
plt.ylabel(r'$\Delta \nu / \si{\hertz}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'VgegenDeltaV')

a = unp.uarray(params[0], np.sqrt(covar[0][0]))
print('vNull/c:', a)
print('c:', vNull/a)

# makeTable([x[0:int(len(x)/2)]*100, yd[0:int(len(yd)/2)]*1000], r'{'+namex+r'} & {'+namey+r'}', 'tabbeidseitig1', ['S[table-format=2.1]', 'S[table-format=1.2]'], ["%3.1f", "%3.2f"])


# a = unp.uarray(params[0], np.sqrt(covar[0][0]))

# Schallges-----------------------------------------------------------------------------

x, y = np.genfromtxt('scripts/Wellenlängenmessungundnormalfrequenz', unpack=True)

y = y - y[0]
wellenlaenge = unp.uarray(np.mean(y[1:]/x[1:]), stats.sem(y[1:]/x[1:]))
print('Wellenlänge:', wellenlaenge, 'mm')
print('1/Wellenlänge:', (1/wellenlaenge), '1/mm')
print('c:', wellenlaenge*vNull/1000, 'm/s')