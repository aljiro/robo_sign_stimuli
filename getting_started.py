import nest
import nest.voltage_trace
import matplotlib.pyplot as plt
nest.ResetKernel()

neuron = nest.Create('iaf_psc_exp')

spikegenerator = nest.Create('spike_generator')
voltmeter = nest.Create('voltmeter')

spikegenerator.set(spike_times=[10.0, 50.0])

nest.Connect(spikegenerator, neuron, syn_spec={'weight': 1e3})
nest.Connect(voltmeter, neuron)

nest.Simulate(100.0)

nest.voltage_trace.from_device(voltmeter)
plt.show()
