# Import necessary libraries
import xmlrpc.client as xml  # For XML-RPC server communication
import matplotlib.pyplot as plt  # For plotting graphs
import numpy as np  # For numerical operations

# Connect to the PLECS XML-RPC server
model = 'simulation_modif'  # Define the model name
file_type = '.plecs'  # Define the file type
plecs = xml.Server('http://localhost:1080/RPC2').plecs  # Create a server object

# Set the plotting style
plt.style.use('seaborn-v0_8-deep')  # Use a specific style for the plots

# Simulate the model and retrieve values and time
values = plecs.simulate(model)['Values']  # Get simulation values
time = plecs.simulate(model)['Time']  # Get simulation time

# Plot trigger signals over time
plt.figure(figsize=(10,5))
plt.plot(time,values[2],linewidth=2, label='Señal de disparo $S_U$')  # Upper trigger signal
plt.plot(time,values[3],linewidth=2, label='Señal de disparo $S_L$')  # Lower trigger signal
plt.xlabel('Tiempo (s)')
plt.ylabel('Tensión de disparo (V)')
plt.title('Señales de disparo en función del tiempo')
plt.legend()
plt.xlim(0,0.00004)
plt.grid(True)
plt.savefig('disparo.pdf')  # Save the plot as a PDF file

# Plot primary and secondary winding voltages over time
plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
plt.plot(time,values[4],linewidth=2)  # Primary winding voltage
plt.ylabel('Tensión (V)')
plt.xlabel('Tiempo (s)')
plt.title('Tensión del devanado primario en función del tiempo')
plt.grid(True)
plt.xlim(1.0860e-1,1.0865e-1)
plt.subplot(2,1,2)
plt.plot(time,values[6],linewidth=2)  # Secondary winding voltage
plt.ylabel('Tensión (V)')
plt.xlabel('Tiempo (s)')
plt.title('Tensión del devanado secundario en función del tiempo')
plt.grid(True)
plt.xlim(1.0860e-1,1.0865e-1)
plt.savefig('tensiones_transformador.pdf')  # Save the plot as a PDF file

plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
plt.plot(time,values[5],linewidth=2)
plt.ylabel('Corriente (A)')
plt.xlabel('Tiempo (s)')
plt.title('Corriente en el devanado primario en función del tiempo')
plt.grid(True)
plt.xlim(8.14e-3,8.2e-3)
plt.subplot(2,1,2)
plt.plot(time,values[7],linewidth=2)
plt.ylabel('Corriente (A)')
plt.xlabel('Tiempo (s)')
plt.title('Corriente en el devanado secundario en función del tiempo')
plt.grid(True)
plt.xlim(8.14e-3,8.2e-3)
plt.savefig('corrientes_transformador.pdf')

plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
plt.plot(time,values[0],linewidth=2)
plt.ylabel('Tensión (V)')
plt.xlabel('Tiempo (s)')
plt.title('Tensión de salida para $R_o=100\Omega$')
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(time,values[1],linewidth=2)
plt.ylabel('Corriente (A)')
plt.xlabel('Tiempo (s)')
plt.title('Corriente de salida para $R_o=100\Omega$')
plt.grid(True)
plt.savefig('informe/informe_TFI/img/salida_100.pdf')

plt.figure(figsize=(10,5))
plt.plot(time,values[0],linewidth=2)
plt.ylabel('Tensión (A)')
plt.xlabel('Tiempo (s)')
plt.title('Transitorio de tensión de salida para $R_o=100\Omega$')
plt.grid(True)
plt.xlim(0,4e-3)
plt.savefig('informe/informe_TFI/img/transitorio.pdf')

voltage = np.array(values[0])
current = np.array(values[1])

plt.figure(figsize=(10,5))
plt.plot(time,voltage*current,linewidth=2)
plt.ylabel('Potencia (W)')
plt.xlabel('Tiempo (s)')
plt.title('Potencia de salida para $R_o=100\Omega$')
plt.grid(True)
plt.savefig('informe/informe_TFI/img/potencia.pdf')

# Calculate and print the settling time
index_40 = np.where(voltage > 40)[0][0]  # Find the index where voltage exceeds 40V
value_90 = 0.9 * 400  # Calculate 90% of 400V
for i in range(index_40, len(voltage)):
    if all(voltage[i:] >= value_90):
        indice_90_por_ciento = i  # Find the index where voltage stabilizes at 90% of 400V
        break
tiempo_establecimiento = time[indice_90_por_ciento] - time[index_40]  # Calculate settling time
print(f"El tiempo de establecimiento es {tiempo_establecimiento} segundos.")  # Print the settling time

# Simulate the model for different load resistances and plot the average output voltage and current
resistance = np.linspace(100,50000,100)  # Define a range of load resistances
v_mean = []  # List to store average voltages
i_mean = []  # List to store average currents

import time as t  # Import time module for sleep function

for r in resistance:
    plecs.set(model+'/Ro','R',str(r))  # Set the load resistance
    values = plecs.simulate(model)['Values']  # Simulate the model
    half = len(values[0])//2  # Find the midpoint of the simulation
    half_values = values[0][half:]  # Consider values after the midpoint
    v_mean.append(np.mean(half_values))  # Calculate and store the average voltage
    i_mean.append(np.mean(values[1][half:]))  # Calculate and store the average current
    t.sleep(1e-3)  # Short pause between simulations

# Plot the average output voltage and current as a function of load resistance
plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
plt.plot(resistance,v_mean,linewidth=2)  # Plot average voltage
plt.ylabel('Tensión (V)')
plt.xlabel('Resistencia de carga ($\Omega$)')
plt.title('Tensión media de salida en función de la resistencia de carga')
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(resistance,i_mean,linewidth=2)  # Plot average current
plt.ylabel('Corriente (A)')
plt.xlabel('Resistencia de carga ($\Omega$)')
plt.title('Corriente media de salida en función de la resistencia de carga')
plt.grid(True)
plt.savefig('informe/informe_TFI/img/salida_regulacion.pdf')  # Save the plot as a PDF file

plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
plt.plot(time,values[8],linewidth=2)
plt.ylabel('Tensión (V)')
plt.xlabel('Tiempo (s)')
plt.title('$V_{CE}$ para IGBT en función del tiempo')
plt.grid(True)
plt.xlim(1.0860e-1,1.0865e-1)
plt.subplot(2,1,2)
plt.plot(time,values[9],linewidth=2)
plt.ylabel('Corriente (A)')
plt.xlabel('Tiempo (s)')
plt.title('$I_{C}$ para IGBT en función del tiempo')
plt.grid(True)
plt.xlim(1.0860e-1,1.0865e-1)
plt.savefig('informe/informe_TFI/img/signal_IGBT.pdf')

plt.figure(figsize=(10,5))
plt.plot(time,values[11],linewidth=2)
plt.ylabel('Corriente (A)')
plt.xlabel('Tiempo (s)')
plt.title('Corriente en el diodo snubber')
plt.grid(True)
plt.xlim(2.75e-1,2.753e-1)
plt.savefig('informe/informe_TFI/img/diodo_snubber.pdf')

plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
plt.plot(time,values[13],linewidth=2)
plt.ylabel('Tensión (V)')
plt.xlabel('Tiempo (s)')
plt.title('$V_{D}$ para diodo de salida en función del tiempo')
plt.grid(True)
plt.xlim(1.0860e-1,1.0865e-1)
plt.subplot(2,1,2)
plt.plot(time,values[12],linewidth=2)
plt.ylabel('Corriente (A)')
plt.xlabel('Tiempo (s)')
plt.title('$I_{F(av)}$ para diodo de salida en función del tiempo')
plt.grid(True)
plt.xlim(1.0860e-1,1.0865e-1)
plt.savefig('informe/informe_TFI/img/diodo_salida.pdf')
