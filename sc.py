import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve, minimize

# Constantes
Lk = 100e-6  # Inductancia de pérdida en Henrios
n = 4.938271604938271    # Relación de vueltas (puede ajustarse según el transformador específico)
Tres1 = 7e-6
Tres2 = 7e-6

# Ecuaciones a resolver
def equations(vars, Tres1, Tres2):
    CL, CH = vars
    eq1 = Tres1 - np.pi * np.sqrt((Lk * 2 * CL * n**2 * CH) / (CL + n**2 * CH))
    eq2 = Tres2 - np.pi * np.sqrt((2 * Lk * n**2 * CL * CH) / (CL + 2 * n**2 * CH))
    return [eq1, eq2]

# Valores iniciales para la optimización
initial_guess = [1e-7, 1e-7]  # Valores iniciales de CL y CH

# Función para calcular CL y CH con restricciones
def calculate_CL_CH_with_constraints(Tres1, Tres2):
    def objective(vars):
        return 0  # No importa el valor, solo nos interesa cumplir las restricciones

    constraints = [
        {'type': 'eq', 'fun': lambda vars: equations(vars, Tres1, Tres2)[0]},
        {'type': 'eq', 'fun': lambda vars: equations(vars, Tres1, Tres2)[1]},
        {'type': 'ineq', 'fun': lambda vars: vars[0]},  # CL >= 0
        {'type': 'ineq', 'fun': lambda vars: 100e-6 - vars[0]},  # CL <= 100e-6
        {'type': 'ineq', 'fun': lambda vars: vars[1]},  # CH >= 0
        {'type': 'ineq', 'fun': lambda vars: 100e-6 - vars[1]}   # CH <= 100e-6
    ]

    result = minimize(objective, initial_guess, constraints=constraints)
    return result.x if result.success else (None, None)

# Generar 40 valores de Tres entre 1e-6 y Tresmax
Tres1_values = np.linspace(1e-6, Tres1, 100)
Tres2_values = np.linspace(1e-6, Tres2, 100)

# Calcular CL y CH para cada par de valores de Tres1 y Tres2
data = []
for Tres1_val, Tres2_val in zip(Tres1_values, Tres2_values):
    CL, CH = calculate_CL_CH_with_constraints(Tres1_val, Tres2_val)
    data.append((Tres1_val, Tres2_val, CL, CH))

# Crear un DataFrame con los resultados
df = pd.DataFrame(data, columns=['Tres1', 'Tres2', 'CL', 'CH'])


# Graficar los resultados
plt.figure(figsize=(14, 6))

# Gráfico de CL vs Tres1 y Tres2
plt.subplot(1, 2, 1)
plt.plot(df['Tres1'], df['CL'], label='CL vs Tres1')
plt.plot(df['Tres2'], df['CL'], label='CL vs Tres2', linestyle='--')
plt.xlabel('Tres (s)')
plt.ylabel('CL (H)')
plt.title('CL vs Tres')
plt.legend()

# Gráfico de CH vs Tres1 y Tres2
plt.subplot(1, 2, 2)
plt.plot(df['Tres1'], df['CH'], label='CH vs Tres1')
plt.plot(df['Tres2'], df['CH'], label='CH vs Tres2', linestyle='--')
plt.xlabel('Tres (s)')
plt.ylabel('CH (H)')
plt.title('CH vs Tres')
plt.legend()

plt.tight_layout()
plt.show()
