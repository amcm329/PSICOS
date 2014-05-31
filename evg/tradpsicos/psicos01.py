#!/usr/bin/env python

from Agente import *
from Mapa import *
from Arma import *
from random import *

#Nota: poner """-----""" despues de cualquier "else" porque si no entonces no jala el programa


"""Program Simulation for COmbat and Society
Version 3.0
Date 14/11/2011

The program works this way:

1.- We have two diferent maps (dictionaries): the first one is the terrain (wich is subdivided in cells) and the second one 
is the army (agents). Both maps are complementary, for instance, supose that the position (x,y) of the map is ocuppied 
(occ atribute of the Cell class) then the army map must have an agent whoose coordinates (the coord atribute of the Agent class) 
are x & y.
There are soldiers of two armies: red and blue.
2.- Values of both maps must be initialized to start the battle.
3.- The battle is a cycle, for every iteration each soldier of both sides will execute the rutines of vision, movement and fighting, in this order.
Note: It is in the fighting rutine were one soldier may kill another soldier, to accomplish soldier elimination status atribute changes to False.
4. The battle ends when the cycle is completed 
"""

#A 10x10 map is created, with random values
mapa = Mapa (10,10,-1,-1,-1,-1);

#Inserts the number of red and blue soldiers 
num_red=input("inserta el numero de soldados rojos ")
num_blu=input("inserta el numero de  soldados azules ")


"""
Counters are declared for each soldiers id, and to count red and blue soldiers when they are added to the list
(we compute this numbers by using the r and a variables). The variables string_a and string_r are just for printing the agents who
belong to each side (red and blue)
"""

id=0
r=0
a=0
cadena_r="Agentes rojos: "
cadena_a="Agentes azules: "

#Personality vectors are defined for the red agents (personality_r) and the blue agents (personality_a)
personalidad_r = {"def":1,"att":10,"num_attacks":6,"rv":9,"coh":6,"vel":7,"sep_min":8,"blindaje":9,"cover":10}
personalidad_a = {"def":1,"att":2,"num_attacks":6,"rv":9,"coh":6,"vel":7,"sep_min":8,"blindaje":9,"cover":10}

#Red side soldiers are created by adding them to the army dictionary

for i in range(0,mapa.dimentions[0]):
	for j in range(0,mapa.dimentions[1]):
                if mapa.getCelda(i,j).occ != "True" and r != num_red:
                    cadena_r+= str(id) + ","
                    #Aqui tuve que hacer la comparacion de getEstado con la cadena "False" y no con el valor False
                    #porque con la primera me funciono el codigo
                    agente_rojo = Agente(id,[i,j],4,"rojo","True",Arma (1,[2,9],randint(0,9)),personalidad_r)
                    mapa.setAgente(i,j,agente_rojo)
                    mapa.getCelda(i,j).occ = "True"
                    r+=1
                    id+=1

#Blue side soldiers are created by adding them to the army dictionary"""
for i in range(0,mapa.dimentions[0]):
	for j in range(0,mapa.dimentions[1]):
            if mapa.getCelda(i,j).occ != "True" and a != num_blu:
                cadena_a+= str(id) + ","
                #Aqui tuve que hacer la comparacion de getEstado con la cadena "False" y no con el valor False
                #porque con la primera me funciono el codigo
                agente_azul = Agente(id,[i,j],5,"azul","True",Arma (1,[2,9],randint(0,9)),personalidad_a)
                mapa.setAgente(i,j,agente_azul)
                mapa.getCelda(i,j).occ = "True"
                a+=1
                id+=1

# Prints agents of the blue and red army """
print cadena_r
print cadena_a

#This is the program cycle we discuss in point 3 of the general description"""

#This are the inital value (t) and the final value (tmax) of the battle, a preview of the ocupation map is 
#printed as a intial status of the battle"""

t=0
tmax=5

print "\n"
print "%%%%%%%%%%%%%%%%Inicio de la guerra%%%%%%%%%%%%%%%%\n"

print mapa.__str__()


#A cycle is generated according to the inital and final values, this is when t<=tmax the while will run emulate a battle
#for each iteration

while t<=tmax:

        print "########Batalla: "+str(t)+"##########"
        

        #As the army is a dictionary, to avoid a sequential repeting acces to the same elements, the element list is disordered,
        #the list is obtained by the function items (); and then the needed operations for every agent are performed

        lista_ejercito = mapa.ejercito.items()
        shuffle(lista_ejercito)

        
        # Here we deal with the "activities" that agents must perform
        for i in range (0,len(lista_ejercito)):
                  
                  #If the agent is alive (atribute status is True) then he can see, move and fight 
                  soldado = lista_ejercito[i]
                  
				  #If army ocpuation in one cell is not empty 
                  if soldado[1]!="":
                     if mapa.estaVivo(soldado[1]) == "True":
                         #soldado[1].imprimeAgente()
                         soldado[1].Ver(mapa)
                         #soldado[1].imprimeVision()
                         soldado[1].Pelear(mapa)
                         print "--------------------------------------------------------------------------------"
                         #i.mover() #PREGUNTAR A OTTO DEL METODO MOVER, SI ES EQUIVALENTE AL MOVER_COVER


        #A map with only the relevant information of an agent is printed (id, side, status):
        #side is either red or blue
        #status is True (agent alive) or False (agent dead) In orther to see before and after of every battle
        
        print mapa.__str__()
        print mapa.imprimeMuertos()

        t+=1

print "\n"
print "%%%%%%%%%%%%%%%%%%%Fin de la guerra.%%%%%%%%%%%%%%%%%%%%"
