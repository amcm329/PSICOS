#!/usr/bin/env python

from Agente import *
from Mapa import *
from Arma import *
from random import *

#Nota: poner """-----""" despues de cualquier "else" porque si no entonces no jala el programa

"""Programa de agentes autonomos para combate (PSICOS).

Version 3.0
Fecha 14/11/2011

El funcionamiento del programa es a grandes rasgos es el siguiente:
1.-Se tienen dos "mapas" (diccionarios) por separado: uno solo del terreno (que a su vez esta formado por Celdas)
y otro solo del ejercito(a su vez formado por Agentes). Cabe mencionar que ambos mapas son complementarios,
por ejemplo: supongamos que en el mapa de terreno la posicion (x,y) esta ocupada (atributo occ de la clase Celda),
entonces en el mapa del ejercito debera existir un agente cuyas coordenadas (el atributo coords de la clase Agente)
sean precisamente x & y.
Cabe mencionar que en cuanto a soldados se refiere existen dos bandos: rojo y azul.
2.-Se inicializan los valores de ambos mapas y comienza "la batalla".
3.-La batalla es un ciclo donde por cada iteracion, cada soldado de cada bando ejecutara las acciones de ver,moverse y pelear en ese orden.
Nota: en la accion de pelear es cuando un soldado elimina a otro, para lograr esta eliminacion simplemente al atributo status
del soldado eliminado se le pone en False.
4.-Finalmente la batalla termina cuando se haya terminado el ciclo.
"""

""""Aqui se crea un mapa de 10x10 con valores aleatorios."""
mapa = Mapa (10,10,-1,-1,-1,-1);

"""Aqui se inserta el numero de soldados tanto rojos como azules."""
num_red=input("inserta el numero de soldados rojos ")
num_blu=input("inserta el numero de  soldados azules ")

"""Se declaran contadores para el id. de cada soldado y para llevar el conteo de soldados rojos y azules
al momento de agregarlos a la lista (este conteo esta dado por las variables r y a respectivamente).
Las variables cadena_a y cadena_r son solo para imprimir los agentes que pertenecen a los bandos rojo y azul."""
id=0
r=0
a=0
cadena_r="Agentes rojos: "
cadena_a="Agentes azules: "

"""Se definen los vectores de personalidad para los agentes rojos (personalidad_r), y los azules (personalidad_a)."""
personalidad_r = {"def":1,"att":10,"num_attacks":6,"rv":9,"coh":6,"vel":7,"sep_min":8,"blindaje":9,"cover":10}
personalidad_a = {"def":1,"att":2,"num_attacks":6,"rv":9,"coh":6,"vel":7,"sep_min":8,"blindaje":9,"cover":10}

"""En este for se crean los soldados del bando rojo para meterse en el diccionario ejercito."""
for i in range(0,mapa.getXmax()):
	for j in range(0,mapa.getYmax()):
                if mapa.getCelda(i,j).getEstado()!="True" and r!=num_red:
                    cadena_r+= str(id) + ","
                    #Aqui tuve que hacer la comparacion de getEstado con la cadena "False" y no con el valor False
                    #porque con la primera me funciono el codigo
                    agente_rojo = Agente(id,i,j,4,"soldado","rojo","True",Arma (1,[2,9],randint(0,9)),personalidad_r)
                    mapa.setAgente(i,j,agente_rojo)
                    mapa.getCelda(i,j).setEstado("True")
                    r+=1
                    id+=1

"""En este for se crean los soldados del bando azul para meterse en el diccionario ejercito."""
for i in range(0,mapa.getXmax()):
	for j in range(0,mapa.getYmax()):
            if mapa.getCelda(i,j).getEstado()!="True" and a!=num_blu:
                cadena_a+= str(id) + ","
                #Aqui tuve que hacer la comparacion de getEstado con la cadena "False" y no con el valor False
                #porque con la primera me funciono el codigo
                agente_azul = Agente(id,i,j,5,"soldado","azul","True",Arma (1,[2,9],randint(0,9)),personalidad_a)
                mapa.setAgente(i,j,agente_azul)
                mapa.getCelda(i,j).setEstado("True")
                a+=1
                id+=1

"""Se imprimen los agentes que pertenecen a los bandos rojo y azul."""
print cadena_r
print cadena_a

"""Ciclo del programa (del cual se habla en el punto 3 de la descripcion del funcionamiento)."""

"""Estas son los valores de inicio (t) y termino (tmax) de la guerra, tambien se imprime el mapa de
ocupaciones militares como un "antes" de toda la guerra."""
t=0
tmax=5

print "\n"
print "%%%%%%%%%%%%%%%%Inicio de la guerra%%%%%%%%%%%%%%%%\n"

print mapa.__str__()

"""Aqui se hace un ciclo de acuerdo con los valores de inicio y termino, es decir, mientras
que t<=tmax se ejecutara el while que emula una batalla por iteracion."""
while t<=tmax:

        print "########Batalla: "+str(t)+"##########"
        
        """Dado que el ejercito es un diccionario, para evitar que siempre se accedan a los mismos elementos
        secuencialmente se desordena la lista de elementos del diccionario, la lista se obtiene mediante la
        funcion items(); y entonces se procede a hacer las operaciones necesarias para cada agente."""
        lista_ejercito = mapa.ejercito.items()
        shuffle(lista_ejercito)

        """Aqui se le da tratamiento a las "actividades" que tienen que llevar a cabo los agentes."""
        for i in range (0,len(lista_ejercito)):
                  """Si el agente esta vivo (si su atributo status es True) entonces podra ver, moverse y pelear."""
                  soldado = lista_ejercito[i]
                  """Si la ocupacion en el ejercito en una celda dada no esta vacia."""

                  if soldado[1]!="":
                     if mapa.estaVivo(soldado[1]) == "True":
                         #soldado[1].imprimeAgente()
                         soldado[1].ver(mapa)
                         #soldado[1].imprimeVision()
                         soldado[1].pelear(mapa)
                         print "--------------------------------------------------------------------------------"
                         #i.mover() #PREGUNTAR A OTTO DEL METODO MOVER, SI ES EQUIVALENTE AL MOVER_COVER

        """Se imprime el mapa solo con la informacion importante de un agente
        (id,bando,status), donde:
        bando es rojo o azul.
        status es True(el agente vive), False (el agente muere)
        esto es para ver el antes y despues de cada batalla."""
        print mapa.__str__()
        print mapa.imprimeMuertos()

        t+=1

print "\n"
print "%%%%%%%%%%%%%%%%%%%Fin de la guerra.%%%%%%%%%%%%%%%%%%%%"