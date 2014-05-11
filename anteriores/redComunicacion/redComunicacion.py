#!/usr/bin/env python

from math import *
from Mapa import *
from Agente import *

#Clase "redComunicacion" implementa una red de comunicaciones entre los agentes para que se les puedan pasar informacion
class redComunicacion:


    #Metodo init para la red de comunicaciones, no necesitamos nada ya que la red no depende de nadie, para darle un uso a la red hay que ponerle
    #a cada ejercito su propia red de comunicaciones, esta manera de implementacion es flexible, ya que podemos tener varias redes de comunicacion
    #por cada ejercito asi que si hay unidades especiales que no necesitan comunicarse con otras unidades que no sean su tipo simplemente creamos una red
    #exclusiva para ese tipo de unidad
    def __init__(self):
        
        self.agentes = [] #Aqui almacenamos a los agentes que se encuentran dentro de la red de comunicacion
        self.numAgentes = 0 #Numero de agentes que forman parte de la red
        self.lider = None #Se puede indicar un "lider" este agente podra ver en cualquier momento toda la informacion que se transmite en la red

    #Metodo addAgente
    #Agregamos a un nuevo agente a la red de comunicaciones para que pueda intercambiar informacion con otros agentes
    def addAgente(self,agente):
        
        #Verificamos si el agente ya forma parte de esta red de comunicaciones
        if self.agentes.contains(agente):
            print("El agente " + str(agente.getId()) + " ya esta dentro de la red de comunicaciones.\n")
            exit
        else:
            self.agentes.add(agente) #Agregamos el agente a la red de comunicaciones
            self.numAgentes = self.numAgentes + 1 #Incrementamos el numero de agentes en la red

        
    #Metodo para eliminar a un agente de la red de comunicaciones
    #Si el agente muere lo quitamos de la red ya que este no es util
    def removeAgente(self,agente):
        
        if self.agentes.contains(agente):
            self.agentes.delitem(agente)
            self.numAgentes = self.numAgentes - 1
        else:
            print("El agente " + str(agente.getId()) + " no esta en la red de comunicaciones\n")

    #Metodo broadcast
    #Este metodo se utiliza si se quiere hacer un "broadcast" a toda la red de comunicaciones, podemos pensar en alguna tabla de descriptores de mensaje
    def broadcast(self,mensaje):

        for i in range (0,self.numAgentes):
            agentes[i].mensaje = mensaje


    #Metodo sendMessage
    #Este metodo siver para enviar mensajes de un agente "a" a un agente "b"
    def sendMessage(self,agenteA,agenteB):

        if self.agentes.contains(agenteA) and self.agnetes.contains(agenteB):
            agenteB.vision.extend(agenteA.vision) #Al agente "b" le agregamos la vision que tiene el agente "a"
            agenteB.vision = self.eliminaRepetidos(agenteB.vision) #Dado que extendimos la vision del agente "b" con lo que veia el agente "a" puede que haya celdas repetidas asi que eliminamos esase repetidas


    #Metodo eliminaRepetidos
    #Este metodo sirve para eliminar los elmentos repetidos de una lista
    def eliminaRepetidos(self,lista):
        nva = []
        checa = 0
        nva.append(lista[0])
        for  i in range (0,len(lista)):
            for j in range (0,len(nva)):
                if lista[i] == nva[j]:
                    checa = 1
            if checa == 0:
                nva.append(lista[i])
            checa = 0
        return nva
                
