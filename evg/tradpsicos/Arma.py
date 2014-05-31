#!/usr/bin/env python

from random import *

## Weapon class for PSICOS
class Arma:

  """The different elements of the weapon are:
	Bullets reserve: the number of bullets the agent has (thoose already loaded are not counted).

	Loader: the weapon loader's capacity , such as the number of bullets present in the loader, this will be seen in an array:
	[bullets_in_charger, loaders_capacity]

	Efficency: this number shows the weapon's accuracy, it simulates the well fucntioning of the weapon. 
	This is a number between 0 and 9, the closer it is to 9 the more efective the wepon is, while the closer
	it is to 0, the wepon is less efective
	"""


def __init__(self,balasreserva,cargador,efectividad):


      #When all the parametrs of the weapon are bigger than 0 (no efectiveness or bullet quantities negative) 
      #then thoose parameters are recieved""""
	if (efectividad>=0 and balasreserva>=0 and cargador[0]>=0 and cargador[1]>=0):
		self.balasreserva = balasreserva
		self.cargador = cargador
		self.efectividad = efectividad

	else:
        
       #When there is at least one parameter below 0, then default values are asigned to the wepon: 270 bullets, 
       #loader full capacity 30 bullets, and a random efectiveness between 0-9"""
		self.balasreserva = 270
		self.cargador = [30,30]
		self.efectividad = randint(0,9)

   
	#Method that returns the weapons efectiveness
def GetEfectividad(self):
	return self.efectividad

   #Method that returns the number of total bullets of the agent
def GetBalasReserva(self):
	return self.balasreserva

   #Method that returns the number of bullets in the loader
def GetBalasCargador(self):
	return self.cargador

   #Method for Shooting the wepon; every step just ONE bullet is fired  
def Disparo(self):
	self.cargador[0]-=1

   #Method for Reloading the weapon, when no bullets are left in the loader.
   #The agent performs no action if he has no bullets left in the loader and in the reserve 
   
def Recarga(self):

       #When the bullets in the reserve are more or the same number that the loaders capacity then loader is
       #Reloaded to its full capacity
       
	if self.balasreserva >= self.cargador[1] :
		self.cargador[0]=self.cargador[1]
		self.balasreserva-=cargador

	elif self.balasreserva < self.cargador[1] :
          #When reserve bullets are less than the loaders capacity then only the bullets left are loaded
		self.cargador[0]=self.balasreserva
		self.balasreserva=0

   #Method that shows when there are bullets left in the weapon (True if there are either in the loader or in the reserve
   #False if tehre are no bullets left)
   
def hayBalas(self):
	if self.balasreserva+self.cargador[0]>0:
		return "True"

	else:
		return "False"

   #Method that shows if Reloading is necesary, this means the loader is empty but the agent still has bullets in his reserve
def NecesarioRecargar(self):
	if self.cargador[0]==0 and self.balasreserva>0:
		return "True"

	else:
		return "False"

  
   #Method that prints weapon's characteristics in a string"""
def __str__(self):
	cadena = "Cargador: ["+str(self.cargador[0])+"/"+str(self.cargador[1])+"]. Balas de reserva: "+str(self.balasreserva)+". Total balas (reserva y en cargador): "+str(self.balasreserva+self.cargador[0])
	return cadena
