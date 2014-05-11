#!/usr/bin/env python
# -*- coding:utf-8 -*-

#LISTA DE DESARROLLADORES
#ACB 13/02/2013
#ACM 18/02/2013

from Celda import *
from Agente import *
from random import *

#IMPORTANTE: AQUI ACORDARSE DE QUE PARA INICIALIZAR EL DICCIONARIO
#EL VALOR QUE ESTA DENTRO DE CORCHETES EN ejercito[(i,j)], ES DECIR,
#EL VALOR (i,j) ES LA KEY PARA EL DICCIONARIO.

"""Clase Mapa para el programa PSICOS
Este consiste en un supermapa que contiene los 3 submapas siguientes:

Mapa: aquí están las celdas con sus propiedades.

Ejército: aquí están los agentes únicamente.

Muertos: diccionario donde se guardan todos los agentes que han "muerto" en la celda."""

"""Map class for PSICOS
This is a supermap wich contains the 3 following submaps:

Map: contains the cells and its propierties

Army: contains just the agents

Cassualties: a dictionary in wich we store the agents that have been killed in the cell"""

class Mapa:

	def __init__(self,x,y,camuflaje,blindaje,movilidad,terreno):
		self.dimentions = [x,y]

                """Este es el diccionario del mapa."""
                """This is the map dictionary """
		self.mapa={}

                """Este es el diccionario del ejercito"""
                """ This is the army dictionary"""
                self.ejercito={}

                """Este es el diccionario de los muertos"""
                """ This is the cassualties dictionary"""
                self.muertos={}

                """Aqui se inicializan los valores del dicionario mapa."""
                   """ Values of the map dictionary are initialized"""
                self.inicializa(camuflaje,blindaje,movilidad,terreno)


	"""Este metodo corresponde a la inicializacion del mapa."""
	"""This method belongs to map intialization """
	def inicializa(self,camuflaje,blindaje,movilidad,terreno):

                for i in range(0,self.dimentions[0]):
			for j in range(0,self.dimentions[1]):
                             """En esta parte si el mapa tiene todos los parametros distintos de -1 entonces
                             las celdas se cargan con los valores especificados"""
                             """ If the map has every parameter different of -1 
                             then cells are loaded with specific values"""                       
                             if camuflaje != -1 and blindaje != -1 and movilidad != -1 and terreno!=-1:
				self.mapa[(i,j)]=Celda(i,j,camuflaje,blindaje,movilidad,terreno)
                                self.ejercito[(i,j)]=""
                                self.muertos[(i,j)]=[]

			     else:
                                """En esta parte si el mapa tiene al menos un parametro igual a -1, entonces las 
                                celdas se cargan con los valores que se tienen por defecto."""
                                """ If map has at least one parameter equal to -1 then 
                                cells are loaded with default values"""
                                self.mapa[(i,j)]=Celda(i,j,randint(0,9),randint(0,9),randint(0,9),randint(0,9))
                                self.ejercito[(i,j)]=""
                                self.muertos[(i,j)]=[]
                                #AQUI VER QUE NO NECESARIAMENTE TOMARAN LOS VALORES 0-9 PARA LOS PARAMETROS POR DEFAULT.


        
        ############ACM-18-2-13########################################################
        #Como se puede apreciar, esta clase consiste en un SuperMapa que contiene el mapa (con Celdas), el ejército y la lista de muertos.
        #Aquí están implementadas las funciones correspondientes a estas 3, por ejemplo la de eliminaAgente y la de mueveAgente.                        
       	def getCelda(self,x,y):
		return self.mapa[(x,y)]

		def setCelda(self,x,y,valor):
		self.mapa[(x,y)] = valor

        def getAgente(self,x,y):
		return self.ejercito[(x,y)]        

        def setAgente(self,x,y,valor):
                self.ejercito[(x,y)] = valor

        def setMuerto(self,x,y,valor):
                self.muertos[(x,y)].append(valor)

        def getMuertosEnCelda(self,x,y):
                return self.muertos[(x,y)]

        def eliminaAgente(self,agente,celda):
                celda.occ = "False"
                agente.status = "False"
                self.setCelda(celda.coords[0],celda.coords[1],celda)
                self.setAgente(celda.coords[0],celda.coords[1],"")
                self.setMuerto(celda.coords[0],celda.coords[1],agente)


        def mueveAgente(self,celda_origen,celda_destino):
            agente = self.getAgente(celda_origen.coords[0],celda_origen.coords[1])
            self.setAgente(celda_origen.coords[0],celda_origen.coords[1],"")
            agente.coords[0] = celda_destino.coords[0]
            agente.coords[1] = celda_destino.coords[1]
            self.setAgente(celda_destino.coords[0],celda_destino.coords[1],agente)


        def estaVivo(self,agente):
            for i in range(0,self.dimentions[0]):
                for j in range(0,self.dimentions[1]):
                    celda = self.getMuertosEnCelda(i,j)
                    for muerto in celda:
                        if muerto.ident == agente.ident:
                           return "False"

            return "True"
          

        ############ACM-18-02-2013########################################################

       	                

        ############ACB-13-2-13########################################################
        '''
	Este  metodo llena  la  lista de vecinos  de cada  celda se  usara  en el metodo  mover_lider para llenar  la lista de celdas  vecinas en una  vecindad de Moore 
	'''
	''' This method fills de neighbors list of each cell, it will be used in the lider_move method to fill the cell lists with a Moore neighborhood'''
        def get_Vecinos(self,x,y):
		for r in range(2):
			for s in range(2):
				self.mapa[(x,y)].vecinos.append(self.mapa[(x+r,y+s)])
				
	        return self.mapa[(x,y)].vecinos
	    
        ################################################################################

        """Metodo que imprime el id,bando y status de cada uno  de los miembros del ejercito
        de acuerdo a laposicion que ocupan.
        Si la celda esta ocupada por un miembro rojo vivo aparecera "rojo", de lo contrario
        aparecera "azul".
        Si se trata de un miembro vivo se pondra "vivo" en su status, si es lo contrario
        aparecera la palabra "muerto"."""
        """This method prints the id, side and status of each of the members of the army, refering to its position
        If the cell is occupied by a living red memeber it will show "red", if not it will show "blue"
        If the memeber is alive it will show "alive" in status, if not it will show "dead" """
	def __str__(self):
		cadena = ""
		for i in range(0,self.dimentions[0]):
			for j in range(0,self.dimentions[1]):
                            """Si la cadena NO esta vacia entonces se imprime el agente."""
                            """IF the string if NOT empty then print the agent """
                            if self.ejercito[(i,j)]!="":
                                """Si el agente esta vivo se pone lo siguiente:"""
                                """If the agent is alive prints the following: """
                                cadena += str(self.ejercito[(i,j)].ident) + "," + str(self.ejercito[(i,j)].bando) + "\t"
                
                            else:
                                """Si la cadena esta vacia se pone "vacio". """
                                """If the string if empty it gives "empty"""
                                cadena+="vacio" + "\t"

                        cadena += "\n"

                return cadena

        def imprimeMuertos(self):
            cadena = ""
            celda = ""
            for i in range(0,self.dimentions[0]):
		   for j in range(0,self.dimentions[1]):
                       celda = self.getMuertosEnCelda(i,j)
        
                       if len(celda)>0:
                          cadena += "Muertos en la celda ("+str(i)+","+str(j)+"):\n"
                          for agente in celda:
                              cadena += "["+str(agente.ident)+"-"+str(agente.bando)+"]. "
                          cadena += "\n"

            return cadena
