import nest
import matplotlib.pyplot as plt
import nest.voltage_trace
import numpy as np
import datetime
# Settings
nest.ResetKernel()
nest.set_verbosity("M_WARNING")

# Create the NN grid
# Frame size of the event camera 320 x 240
res_x = 320
res_y = 240
scale = 0.1
neuron_number_x = int(res_x*scale)
neuron_number_y = int(res_y*scale)
positions = nest.spatial.grid(shape=[neuron_number_x, neuron_number_y],  # the number of rows and column in this grid ...
                              extent=[res_x, res_y],  # the size of the grid in mm
                              center=[res_x/2, res_y/2] # grid origin set to (1; 1) 
                              )
population= nest.Create('iaf_psc_exp', positions=positions)
ndict = {"I_e": 200.0, "tau_m": 20.0}
hpop = nest.Create("iaf_psc_alpha", 100, params=ndict)
vpop = nest.Create("iaf_psc_alpha", 100, params=ndict)

voltmeter = nest.Create('voltmeter')

spikerecorder = nest.Create("spike_recorder")

print(population[10].get('tau_m'))
#print(nest.PrintNodes())
# for j in range(len(population)-2):
#     print(nest.GetPosition(population[j]))
# Connect
nest.Connect(voltmeter, population)

nest.Connect(population, spikerecorder)

sigma = 0.05
receptive = lambda x, y, x0, y0: 900.0*np.exp(-sigma*((x - x0)**2 + (y - y0)**2))
x = res_x*0.9 # 3.0
y = 3.0
nest.Prepare()
print(datetime.datetime.now())
steps=200
delay=1.0
for i in range(steps):
    # TO-DO: Take the input from the camera
    x -= res_x/steps

    # Integrate the network
    for j in range(len(population)-2):
        neuron = population[j]
        pos = nest.GetPosition(neuron)
        neuron.set(I_e = receptive(x, y, pos[0], pos[1]))
    nest.Run(delay)

    # TO-DO: Take the output and control the robot

nest.Cleanup()

nest.voltage_trace.from_device(voltmeter)

print(datetime.datetime.now())
dSD = spikerecorder.get("events")
evs = dSD["senders"]
ts = dSD["times"]
plt.figure(2)
plt.plot(ts, evs, ".")
plt.axis([0, 200, 0, len(population)-1])
plt.show()
