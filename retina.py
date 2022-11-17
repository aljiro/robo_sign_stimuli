import nest
import matplotlib.pyplot as plt

neuron = nest.Create("iaf_psc_alpha")

print(neuron.get('I_e'))

