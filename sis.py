#AC del modelo SIS con una retícula de 100 por 100
#Al inicio aparecen 10 individuos infectados sobre la retícula
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
from operator import itemgetter

'''Vecindad de Moore'''
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
'''Conjunto de Estados { 0 vacío, 1 susceptible, 2 infectado }'''
E, S, I = 0, 1, 2 
'''usamos un color para cada celda, observe que hay que agregar uno más a la lista
con la intención de que el mapa de colores reconozca los tres que deseamos'''
colors_list = ["gray", "green", "gray","red" ]
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3]
norm = colors.BoundaryNorm(bounds, cmap.N)
'''se especifican la densidad inicial de individuos infectados,
así como p, la probabilidad de que un infectado contagie a un susceptible
q la probabilidad de que un infectado se recupere y pase a susceptible.
las lista universeList contiene los estados de cada una de las celdas de la retícula, 
es un arreglo de 102 por 102, en donde la orilla no juega un papel en la dinámica.
La lista RES es el registro del número de de susceptibles e infectados, 
que se cuentan con la variable oneCount y twoCount, respectivamente '''
density = 0.001
universeList,RES = [],[]
oneCount = 0
twoCount = 0
cellCountX, cellCountY = 102, 102
p=0.2
q=0.5
'''Inicialización de la retícula'''
def initialize():
	global currentTimeStep, universeList, RES
	currentTimeStep=0
	'''Se llena de celdas vacías la retícula, incluida la orilla (línea 40),
	luego con 10 mil susceptibles (línea 41) y se ubican a los infectados de manera aleatoria
	de manera que sean tantos como lo especifica la densidad (density) (líneas 42 y 43 )''' 
	universeList  = np.zeros((cellCountX, cellCountY))
	universeList[1:cellCountY-1, 1:cellCountX-1]  = np.ones((cellCountX-2, cellCountY-2))
	universeList[1:cellCountY-1, 1:cellCountX-1] = np.random.randint(1, 3, size=(cellCountY-2, cellCountX-2))
	universeList[1:cellCountY-1, 1:cellCountX-1] = (np.random.random(size=(cellCountY-2, cellCountX-2)) <= density)+1
	'''se cuenta cuántos susceptibles e infectados hay en la configuración inicial'''
	twoCount = np.count_nonzero(universeList==2)
	oneCount = np.count_nonzero(universeList==1)
	RES.append([currentTimeStep,oneCount,twoCount])

'''actualización de la retícula'''
def update(universeList):
	global X1, currentTimeStep, RES
	'''creamos una retícula espejo de la reticula universeList'''
	X1 = np.zeros((cellCountX, cellCountY))
	'''se incrementa el número de iteración'''
	currentTimeStep += 1
	'''recorrido de la retícula en donde se aplica la regla de evolución'''
	for ix in range (1,cellCountX-1):
		for iy in range (1,cellCountY-1):
			if universeList[iy,ix] == E:
				continue
			elif universeList[iy,ix]==I:
				X1[iy,ix] = I
				if np.random.random() <= q:
					X1[iy,ix] = S
			else:
				X1[iy,ix] = S
				for dx,dy in neighbourhood:
					if universeList[iy+dy,ix+dx] == I and np.random.random() <= p:
						X1[iy,ix] = I
						break
	'''actualización del número de susceptibles e infectados al tiempo currentTimeStep'''
	twoCount = np.count_nonzero(X1==2)
	oneCount = np.count_nonzero(X1==1)
	RES.append([currentTimeStep,oneCount,twoCount])
	print(currentTimeStep)
	return X1

# la funcion de animación produce una instantánea de la retícula por unidad de tiempo
def animate(i):
    im.set_data(animate.universeList)
    animate.universeList = update(animate.universeList)

'''se llama a la función de inicialización de la retícula'''
initialize()
'''se crea la imagen de la retícula'''
fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(universeList, cmap=cmap, norm=norm)#, interpolation='nearest')
'''a la función de animación se le manda la retícula universeList'''
animate.universeList = universeList
interval = 100
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=300)
plt.show()
'''se crean las gráficas de la propagación'''
plt.plot(list(map(itemgetter(0),RES)),list(map(itemgetter(1),RES)),'-g', label='Susceptibles') 
plt.plot(list(map(itemgetter(0),RES)),list(map(itemgetter(2),RES)),'-r', label='Infectados')
plt.xlabel('días')
plt.ylabel('Individuos')
plt.grid(True, linestyle='--', linewidth=0.4)
plt.legend(loc=0)
plt.xticks(np.arange(0, 120, step=10))
plt.xlim((0, 120))    
plt.title( 'AC del modelo S-I-S con ' r'$ \beta = 0.2$' ' , ' r'$ \gamma = 0.5$')
plt.show()

