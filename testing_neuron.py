import nest
import matplotlib.pyplot as plt
import nest.voltage_trace
import numpy as np
nest.ResetKernel()

# Create the NN
neuron = nest.Create('iaf_psc_exp')
voltmeter = nest.Create('voltmeter')

spikerecorder = nest.Create("spike_recorder")


# Connect
nest.Connect(voltmeter, neuron)

nest.Connect(neuron, spikerecorder)


sigma = 1.0
x0 = 3.0
receptive = lambda x: 900.0*np.exp(-sigma*(x - x0)**2)
x = 0

for i in range(200):
    x += 0.05

    neuron.set(I_e = receptive(x))
    nest.Simulate(1.0)

nest.voltage_trace.from_device(voltmeter)

dSD = spikerecorder.get("events")
evs = dSD["senders"]
ts = dSD["times"]
plt.figure(2)
plt.plot(ts, evs, ".")
plt.show()