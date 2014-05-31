#!/usr/bin/env python
# -*- coding:utf-8 -*-

#LISTA DE DESARROLLADORES.
#OHH 7/02/2013
#ACM 18/02/2013

from random import *
from Mapa import *
from Arma import *

#CREO QUE NO HAY DIFERENCIA ENTE EL USO DE , Y + EN LA CONCATENACION DE UNA CADENA, PERO SI ES
#IMPORTANTE EL USO DE STR() PARA QUE NO SALGAN LAS COSAS ESAS DE NONE.
#DE HECHO ESTA COSA ME DEJABA IMPRIMIR CON ,, Y SIN STR() PERO POR ESO SALIA NONE, HAY QUE EVITAR ESTO.


""" Agent class for PSICOS
This is the element description:

Ident: a unique numerical identifier asigned to every agent: when agents are killed thier identifiers are not asigned to any
other agent
Coords: an array [x,y] that locates the agent in the lists map and army (see psicos class01)
Velmax: the maximum speed an agent can reach
Side: shows the army that the agent belongs to: red or blue
Stautus: shows True if alive, False if dead
Weapon: the agents weapon (see Weapon class)
Personality: an array wich contains precise information about the agent, it has the following features;
Personality vector is composed by: [def,att,num_attacks,rv,coh,vel,sep_min,blindaje,cover]
blindaje = idem (vease el metodo Pelear). 
def=defense (see Fighting method)
att= attack (see Fighting method)
num_attacks= the number of attacks an agent can perform (seee fighting Method)
rv= vision radius (see Vision method)
coh= cohere (an atracting force between agents of the same side, see Moving method
vel= speed (diferent form the velmax attribute of the AGent, see Moving method)
sep_min= minimum separation (see Moving method)
blindaje=idem (see Fighting method).
"""


#AQUI NO SE PARA QUE SIRVE EL ATRIBUTO cover DEL VECTOR DE PERSONALIDAD.

class Agente:

        
        
	def __init__(self,ident,coords,velmax,bando,status,arma,personalidad):
        
		#Agent atributes are inicialized
		self.ident=ident
        #We take coords as an array [x,y]
		self.coords=coords
		self.velmax=velmax
		self.bando=bando
		self.personalidad=personalidad
		self.status=status
		self.vision={}
		#This is the agent's weapon 
		self.arma = arma

#creo que el hecho de que sea {} se basa en que se definio al mapa asi: {}
#investigar como van las listas en python y la diferencia entre usar {} y []
    
        
        def ImprimeAgente(self):
			
			""" This method prints the agent's characteristics
			"""
			print "id.: ",str(self.ident), "; bando: ",str(self.bando),"; coords: ",str(self.coords),"; vel. max.: ",str(self.velmax),"; status: ",str(self.status),"; personalidad: ",str(self.personalidad)
			
        
        
	def Ver(self,mapa):
			
			"""Agent's Method for Seeing, the vision list will be filled with Cells in a range bounded 
			by the "rv" atribute of the personality array
			"""
			contador = 0;
            
            #The following four values show the range in wich the vision list is filled, there are minimum and maximum ranges
            #for the x-axis and the y-axis. This values are respective to the agent's position (x,y coordinates) for example 
            #the "rv" range of vision
			rangoxmin = self.coords[0]-self.personalidad["rv"]
			rangoxmax = self.coords[0]+self.personalidad["rv"]
			rangoymin = self.coords[1]-self.personalidad["rv"]
			rangoymax = self.coords[1]+self.personalidad["rv"]

			for x in range (rangoxmin,rangoxmax):
				for y in range (rangoymin,rangoymax):

                     #If the agent's vision range is an accepted value in the map, then the elements the agent can "See"
                     #will be added to the vision list, including the positions (the vision is a cell list)

                     #La primera parte del if (de izquierda a derecha) es para asegurar que la vision no se pase
                     #del rango inferior, mientras que la segunda parte es para asegurar que la vision no se pase
                     #del rango superior (los parentesis en el if fueron solo para distinguir las condiciones
                     #logicas, no tienen otro efecto).
					if (x >= 0 and y >= 0) and (x<mapa.dimentions[0] and y<mapa.dimentions[1]):
						#Aqui entra en juego el atributo camuflaje de la celda (vease clase Celda),
                        #mientras mayor sea el valor del camuflaje mayor facilidad tendra el agente de NO
                        #ser visto, en particular (que tiene un valor de 0-10) si es mayor o igual a 5
                        #entonces la celda en cuestion NO sera agregada a la vision del agente que esta "mirando".
                        #Tampoco se agregan celdas vacias en la vision del agente.
                        #Como dato adicional NO se agrega en la vision del agente la celda en la que se encuentra sin importar
                        #el valor de su camuflaje.
						if mapa.getCelda(x,y).camuflaje < 6  and mapa.getCelda(x,y).coords != self.coords and mapa.getAgente(x,y) != "":
							self.vision[contador] = mapa.getCelda(x,y)
							contador +=1

        def ImprimeVision(self):
			        
			        """ This method prints what the agent is able to see through "Seeing" Method (just the terrain). 
			        The agent sees all the nonempty cells in its vision, except the one he's located in
					"""

				print "El agente ",str(self.ident),"ve las celdas: "
				for i in range(0,len(self.vision)):
               
				#This part shows the cell in wich the agent is located 
					if self.vision[i].GetCoords()!=self.coords:
						print str(self.vision[i].__str__()) #Cada elemendo de la lista vision es una Celda.

        
        def Pelear(self,mapa):
				
			"""Method were the agent fights, he will take an agent in its vision range (Method See), if it is an enemy he will
			try to kill him with his weapon (see Arm class). While attacking the agent will use the attributes "num_attacks", "att" of
			it's personality vector  and it's weapon. The agent attacked will use the atributes "def" and "blindage of it's 
			personality to avoid being killed
			"""
			
			print "Turno de pelea del agente: ",str(self.ident)
    
			#If the agent's vision is null, or equivalent, this is if the vision list has no cells (Method see), that means
			#the agent has no neighboors and then the program passes to the else in line 216"""
			if len(self.vision)>0:

               #Agent's vision list is disordered (Method See), for the agent to select a random Objective"""
				shuffle(self.vision)
				soldier = ""
				target = ""
				target_cell = ""

               ############################ACM-18-02-2013########################
               #He modificado el metodo Pelear ya que el ejercito, mapa (que contiene solo Celdas)
               #y lista de muertos las habia metido en una clase (llamada Mapa.py) que se puede ver
               #como un supermapa.        
               #Además al metodo Pelear se le ha añadido la opcion de que, al momento de utilizar
               #la visión no pare de buscar hasta que se haya encontrado un enemigo.        
               #Lo que se hace es entonces iterar sobre la lista de vision hasta encontrar una celda cuyo ocupante sea un enemigo,
               #en caso de no encontrarse alguno entonces se regresa una referencia vacía y no se entra al método.
               #Dado que la visión ahora es un diccionario, por eso se debe pedir el elemento 1 de cada celda, porque
               #de un diccionario sólo se puede devolver sus elementos con "items", y eso regresa tuplas del estilo
               #llave-contenido
               
				for cell in self.vision.items():
					soldier = mapa.getAgente(cell[1].coords[0],cell[1].coords[1])
					if soldier != "":
						if soldier.bando != self.bando:
							target = soldier
							target_cell = cell[1]
							break

               ############################ACM-18-02-2013########################     
               
               #When target is not null (the agent knows target must an enemy) and the agent attacked has bullets then he attacks""""
				if target != "" and self.arma.hayBalas()=="True":
					print "El agente ",str(self.ident)," va a atacar al agente ",str(target.ident)
					oportunidad = 1

					#Esta es la forma en que se calcula el ataque y la defensa, pero se puede cambiar por lo que
					#Otto diga.
					ataque = self.personalidad["att"]  + self.arma.GetEfectividad()
					defensa = target.personalidad["def"] + target.personalidad["blindaje"] + target_cell.blindaje
                  
					while (not (oportunidad == self.personalidad["num_attacks"] + 1)) and self.arma.hayBalas()=="True":

                    #If agent has bullets in the magazine (Arm class) then he will shoot.
                    #If he has no bullets in the magazine but he still has some bullets, then he will Reload the weapon, he will
                    #loose one turn for shooting the enemy
                    #If the agent has no bullets left, he will do nothing and he will loose all his further oportunities for attacking"""
                     
                     
						print "Oportunidad (",str(oportunidad),"/",str(self.personalidad["num_attacks"]),"):"
						print "Municion restante: ",self.arma.__str__()

						if self.arma.hayBalas()=="False":
							oportunidad = self.personalidad["num_attacks"]+1
							print "El agente ",str(self.ident),"ya no tiene balas y pierde sus oportunidades."

						if self.arma.NecesarioRecargar()=="True":
							self.arma.Recarga()
							#Agent losses a chance while Reloading
							oportunidad+=1
							print "El agente ",str(self.ident)," Recarga su arma y pierde una oportunidad."
                       
						else:
                        
                        #Shoot is made, this works this way: a random number between 0 and the absolute value of the attack minus 
                        #defense; if this is less than the attrition then he shots, if he has bullets, else he does nothing."""
                        
							self.arma.Disparo()
							aleatorio = randint(0,abs(ataque-defensa))
							print "El agente ",str(self.ident)," dispara al agente ",str(target.ident),"."
                       
                        #Esta se supone que es la condicion para que el agente mate a su enemigo, pero bien se puede
                        #cambiar por la que diga Otto.
                        
                        #The agent shots the enemy and kills him
							if aleatorio < (abs(ataque-defensa)/2):
                          
                           #Then the killing agent method of the Map class is called, it errases the Agent of the map and 
                           #puts him in the dead map, in the same cell where he died
								mapa.eliminaAgente(target,target_cell)
								print "El agente ",str(self.ident)," ha eliminado al agente ",str(target.ident)
								break

							else:
								print "El agente ",str(self.ident)," falla."
                           
								#If the agent misses the shot oportunities counter increases by 1 
								oportunidad+=1
					else:		
						if target == "":
							print "El agente ",str(self.ident)," no tiene con quien pelear."

						else:
						#Mesages are printed in three cases: 1. Agent has no bullets left, Target is an agent of its side
						#or Target has been errased"""
							if self.arma.hayBalas()=="False":
								print "El agente ",str(self.ident)," ya no tiene mas balas."

							if target.status!="True":
								print "El Objetivo ",str(target.ident)," ya ha sido eliminado"

				else:
					print "El agente ",str(self.ident)," no tiene enemigos visibles."


        #----------A PARTIR DE AQUI LE TOCA A OTTO; CREO QUE ESO DE GENERA LISTA BOIDS YA NO ES NECESARIO---------------------------------------------------
 
################################OHH#######################################################
#el metodo mover sera la suma en coordenadas de los metodos siguientes.
	def mover(self,mapa):

		def Cohesion(self): #mantiene la cohesion (los acerca)
			pc=array([0,0]) #funcion de numpy
			n=0 #contador de boids en mapa_int
			for x in range(-self.personalidad["rv"], self.personalidad["rv"]):
				for y in range(-self.personalidad["rv"], self.personalidad["rv"]):
					if (self.mapa_int[x,y]==self.mapa_int[0,0]):
						continue
					elif (self.mapa_int[x,y]["occ"]==True):
						n+=1
						pc=pc+array([x,y])
			pc=pc/n
			return ((pc-self.coords)/self.personalidad["coh"])

		def Separacion(self): #mantiene una separacion minima (los aleja).
			c=array([0,0])
			for x in range(-self.personalidad["rv"], self.personalidad["rv"]):
				for y in range(-self.personalidad["rv"], self.personalidad["rv"]):
					if (self.mapa_int[x,y]==self.mapa_int[0,0]):
						continue
					elif (self.mapa_int[x,y]["occ"]==True):
						if abs(self.coords-self.mapa_int[x,y])<self.personalidad["sep_min"]:
							c=c-(self.coords-self.mapa_int[x,y])
			return c

		def MatchVelocity(self): #empareja la vel del boid con las de los demas boids.
			pv=array([0,0])
			for x in range(-self.personalidad["rv"], self.personalidad["rv"]):
				for y in range(-self.personalidad["rv"], self.personalidad  ["rv"]):
					if (self.mapa_int[x,y]==self.mapa_int[0,0]):
						continue
				for boid in self.listaboids:
					pv=pv+boid.vel
					pv=pv/n-1
					dif=(pv-self.vel)/self.personalidad["vel"]
			return dif
	

		def Objetivo(self):#va hacia al Objetivo, se atrae hacia el Objetivo.
			 dif=self.obj-self.coords
			 dif=dif/self.pers["obj"]
			 return dif

		def Fronteras(self,xmin,xmax,ymin,ymax): #te aleja de las Fronteras.
			if self.coords[0] < (5+xmin):
				self.vel[0]=self.vel[0]+1
			elif self.coords[0] > (xmax-5):
				self.vel[0]=self.vel[0]-1
			if self.coords[1] < (5+ymin):
				self.vel[1]=self.vel[1]+1
			elif self.coords[1] > (ymax-5):
				self.vel[1]=self.vel[1]-1
	
		def MoveCover(self): #te mueves a donde haya mas blindaje.
			d=[0,0]
			for x in range(-self.personalidad["rv"], self.personalidad["rv"]):
				for y in range(-self.personalidad["rv"], self.personalidad["rv"]):
					if (self.vision[x,y]["blindaje"]>=self.personalidad["blindaje"]):
						d=self.vision[x,y]-self.coords
						d=d/self.personalidad["cover"]
						break
			return d
		mov[1]=Cohesion[1] + Separacion[1] + MatchVelocity[1]+Objetivo[1]+Fronteras[1]+MoveCover[1]
		mov[0]=Cohesion[1] + Separacion[1] + MatchVelocity[1]+Objetivo[1]+Fronteras[1]+MoveCover[1]
		return mov
        #################################OHH#############################


#########################ACB 20-03-13######################

"""
M\'etodo de movimiento para  el lider, usando la ruta  calculada  por el  algortimo A*.

Para este  caso, se  utilizará  una  ruta  definida  por el algoritmo, pero  sólo se  utilizará  en una  cantidad  pequeña  de pasos, despues de la  cual, el lider  tendr\'a  que  detenerse y calcular  nuevamente  la  ruta.
"""
from Astar import *
def MoverLider(self, mapa):
	ruta=aestrella(self.coords,obj)
	for  i in range(8):
		for j in range(2):
			mov[j]=ruta[i][j]+self.vel[j]
                
###############################ACB#################
