
#

#



import numpy

import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

from stratos import Processor



#--- Estos son los parametros de entrada para la funcion:

PATH_DATA = "/dfsmount/miguel/MIP-2/RUNS/00-00-00/OUT/"

FILE_PREF = "run_"

xpos = 14452.3

ypos = 28617.4

zpos = 29517.4

radius = 150





#--- Number of snapshots to read

n_snapshots = 15



#--- We are using StratOS in streaming mode so we must provide an array with parameters:

params = []

for i in range(n_snapshots):  #--- Note that we are increasing the snapshot number by 10 (i*10). At the end we should do all 150 snapshots

    snapshot_i = PATH_DATA + FILE_PREF + str(i*10).zfill(3)

    params_i = [snapshot_i, xpos, ypos, zpos, radius]

    params.append(params_i)





print "Starting StratOS..."

job = Processor(verbosity="debug")

#--- Fabiola: aqui es donde se llama a StratOS, revisa como se ejecuta StratOS en modo streaming, en este caso es:

#   ejecutable, lista de placemarkers con el tipo de dato, arreglo con parametros. Esto seria mas o menos el equivalente a MAP.

job.template_stream("/dfsmount/miguel/MIP-2/RUNS/snap_sample_tophat_particles %f% %c% %c% %c% %c%", params)

print "   Ready with StratOS"



#--- Streaming es asincrono asi que le decimos a StratOS que se espere hasta que todos los procesos acaben para continuar. Esto seria

#    equivalente a reduce, al menos una parte.

job.wait();

profile = job.get_results();



#--- Esta es para que veas como estan los datos. Cada elemento de profile contiene el numero de ejecucion de StratOS y despues una lista de

#    posiciones x,y,z para cada particula. 



print "Number of snapshots:", len(profile)

for w in range(len(profile)):

    print profile[w]

    print '---------------------'





#--- Aqui vamos a guardar todas las particulas de todos los snapshots, lo que queremos en lugar de esto es un arreglo bidimensional (o algo parecido)

#    que contenga arreglos de particulas de cada snapshots ordenados segun el numero de snapshot.

x = []

y = []

z = []

for w in range(len(profile)):

    lines = profile[w].split("\n")



    for i in range(len(lines)-1):  #--- OJO fix -1, last element is empty!!!

        

        if i == 0:

            line_i = lines[i].split(":")

            part_i = line_i[1].split(",")

        else:

            line_i = lines[i]

            part_i = line_i.split(",")



        #--- Append particles to array, only for testing

        xyz = [float(v) for v in part_i]

        x.append(xyz[0]-xpos+w*4000)  #--- damos un incremento en x para desplegar los snapshots de forma separada

        y.append(xyz[1]-ypos)

        z.append(xyz[2]-zpos)





#--- Plot particles

plt.scatter(x,y,color='blue',s=5,edgecolor='none')

plt.show()





print "   Ready plotting"


