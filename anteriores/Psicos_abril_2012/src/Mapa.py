#!/usr/bin/env python

from Celda import *
from Agente import *
from random import *

#IMPORTANTE: AQUI ACORDARSE DE QUE PARA INICIALIZAR EL DICCIONARIO
#EL VALOR QUE ESTA DENTRO DE CORCHETES EN ejercito[(i,j)], ES DECIR,
#EL VALOR (i,j) ES LA KEY PARA EL DICCIONARIO.

"""Clase Mapa para el programa psicos
El mapa es el diccionario complementario del diccionario ejercito (vease la clase psicos01).
Este diccionario contiene solo celdas.

Muertos: diccionario donde se guardan todos los agentes que han "muerto" en la celda."""

class Mapa:

	def __init__(self,x,y,camuflaje,blindaje,movilidad,terreno):
		self.x=x
		self.y=y

                """Este es el diccionario del mapa."""
		self.mapa={}

                """Este es el diccionario del ejercito"""
                self.ejercito={}

                """Este es el diccionario de los muertos"""
                self.muertos={}

                """Aqui se inicializan los valores del dicionario mapa."""
                self.inicializa(camuflaje,blindaje,movilidad,terreno)


	"""Este metodo corresponde a la inicializacion del mapa."""
	def inicializa(self,camuflaje,blindaje,movilidad,terreno):

                for i in range(0,self.x):
			for j in range(0,self.y):
                             """En esta parte si el mapa tiene todos los parametros distintos de -1 entonces
                             las celdas se cargan con los valores especificados"""
                             if camuflaje != -1 and blindaje != -1 and movilidad != -1 and terreno!=-1:
				self.mapa[(i,j)]=Celda(i,j,camuflaje,blindaje,movilidad,terreno)
                                self.ejercito[(i,j)]=""
                                self.muertos[(i,j)]=[]

			     else:
                                """En esta parte si el mapa tiene al menos un parametro igual a -1, entonces las 
                                celdas se cargan con los valores que se tienen por defecto."""
                                self.mapa[(i,j)]=Celda(i,j,randint(0,9),randint(0,9),randint(0,9),randint(0,9))
                                self.ejercito[(i,j)]=""
                                self.muertos[(i,j)]=[]
                                #AQUI VER QUE NO NECESARIAMENTE TOMARAN LOS VALORES 0-9 PARA LOS PARAMETROS POR DEFAULT.


        """Metodo que regresa el tamano (en el eje x) del mapa."""
	def getXmax(self):
		return self.x

        """Metodo que regresa el tamano (en el eje y) del mapa."""
	def getYmax(self):
		return self.y

	def setCelda(self,x,y,valor):
		self.mapa[(x,y)] = valor

	def getCelda(self,x,y):
		return self.mapa[(x,y)]

        def setAgente(self,x,y,valor):
                self.ejercito[(x,y)] = valor

        def setMuerto(self,x,y,valor):
                self.muertos[(x,y)].append(valor)

        def getMuertosEnCelda(self,x,y):
                return self.muertos[(x,y)]

        def getAgente(self,x,y):
		return self.ejercito[(x,y)]

        def eliminaAgente(self,agente,celda):
                celda.setEstado("False")
                agente.setStatus("False")
                self.setCelda(celda.getX(),celda.getY(),celda)
                self.setAgente(celda.getX(),celda.getY(),"")
                self.setMuerto(celda.getX(),celda.getY(),agente)

        def mueveAgente(self,celda_origen,celda_destino):
            agente = self.getAgente(celda_origen.getX(),celda_origen.getY())
            self.setAgente(celda_origen.getX(),celda_origen.getY(),"")
            agente.setX(celda_destino.getX())
            agente.setY(celda_destino.getY())
            self.setAgente(celda_destino.getX(),celda_destino.getY(),agente)

        def estaVivo(self,agente):
            for i in range(0,self.getXmax()):
                for j in range(0,self.getYmax()):
                    celda = self.getMuertosEnCelda(i,j)
                    for muerto in celda:
                        if muerto.getId() == agente.getId():
                           return "False"

            return "True"

        """Metodo que imprime el id,bando y status de cada uno  de los miembros del ejercito
        de acuerdo a laposicion que ocupan.
        Si la celda esta ocupada por un miembro rojo vivo aparecera "rojo", de lo contrario
        aparecera "azul".
        Si se trata de un miembro vivo se pondra "vivo" en su status, si es lo contrario
        aparecera la palabra "muerto"."""
	def __str__(self):
		cadena = ""
		for i in range(0,self.x):
			for j in range(0,self.y):
                            """Si la cadena NO esta vacia entonces se imprime el agente."""
                            if self.ejercito[(i,j)]!="":
                                """Si el agente esta vivo se pone lo siguiente:"""
                                cadena += str(self.ejercito[(i,j)].getId()) + "," + str(self.ejercito[(i,j)].getBando()) + "\t"
                
                            else:
                                """Si la cadena esta vacia se pone "vacio". """
                                cadena+="vacio" + "\t"

                        cadena += "\n"

                return cadena

        def imprimeMuertos(self):
            cadena = ""
            celda = ""
            for i in range(0,self.getXmax()):
		   for j in range(0,self.getYmax()):
                       celda = self.getMuertosEnCelda(i,j)
        
                       if len(celda)>0:
                          cadena += "Muertos en la celda ("+str(i)+","+str(j)+"):\n"
                          for agente in celda:
                              cadena += "["+str(agente.getId())+"-"+str(agente.getBando())+"]. "
                          cadena += "\n"

            return cadena

        ######ACB-13-2-13##########
        '''
	
	Este  metodo llena  la  lista de vecinos  de cada  celda se  usara  en el metodo  mover_lider para llenar  la lista de celdas  vecinas en una  vecindad de Moore 
	'''
        def get_Vecinos(self,x,y):
		for r in range(2):
			for s in range(2):
				self.mapa[(x,y)].vecinos.append(self.mapa[(x+r,y+s)])
				
	        return self.mapa[(x,y)].vecinos
	    
###############################################################
