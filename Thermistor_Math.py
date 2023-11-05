import numpy as np
import matplotlib.pyplot as plt

res = np.linspace(10, 100000)

# thermistor specs based on Amazon listing :(
T1 = 24.1+273.15 # calibration temp (25c)
R1 = 10500	# calibration resistance
B = 3381.6	# beta constant

# temp as a function of thermistor resistence
temp_res = B * (np.log(res / R1) + (B / T1))**-1 - 233.15  # temp in degrees C

# only want to plot for temp values less than 125 since that is upper range of thermistor readings probably
res_filtered = res[temp_res < 125]
temp_filtered = temp_res[temp_res < 125]

# now lets plot temp as a function of voltage for a voltage divider
V_in = 3.3 # assuming sys voltage from pico
R = 10000 # load resistor in circuit; subject to change, but lets start here
V_ADC = V_in*(R/(res_filtered + R)) # good range of voltages to plot over based on what we already know
R_th = ((V_in*R)/V_ADC)-R
temp_volt = B * (np.log(R_th/ R1) + (B / T1))**-1 - 273.15

# Create a figure with subplots
fig, (ax1, ax2) = plt.subplots(2, 1)

# Plot the upper subplot
ax1.plot(res_filtered, temp_filtered)
ax1.set_title(f'10K Thermistor Resistance vs Temperature \n for beta={B}')
ax1.set_xlabel('Thermistor Resistance, Ohms')
ax1.set_ylabel('Temperature, deg C')

# Plot the lower subplot
ax2.plot(V_ADC, temp_volt)
ax2.set_title(f'10K Thermistor Temperature vs ADC Voltage \n for beta={B} and 10K ohm Voltage Divider')
ax2.set_xlabel('ADC Voltage')
ax2.set_ylabel('Temperature, deg C')
plt.subplots_adjust(hspace=1)  # You can adjust the value to control the spacing between upper and lower plots
plt.show()
