import matplotlib.pyplot as plt

fig, ax1 = plt.subplots() # fig è la finestra mentre ax1 è il sistema di assi x con il suo asse y
ax2 = ax1.twinx() #   la funzione mi genera un secondo sistema di assi ma con un asse y indipendente 
line_plot2, = ax1.plot([1,2],[1,1], label='Temp [°C]', color= 'red') # disegna la prima curva sul primo asse posso 
# anche passaere dei valori che verranno poi spacchettati e trasformati in oggetti line 2d
plt.show()