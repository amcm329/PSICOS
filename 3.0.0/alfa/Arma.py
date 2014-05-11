#!/usr/bin/env python

from random import *

"""Clase Arma para el programa PSICOS"""
""" Weapon class for PSICOS"""
class Arma:

   """Los elementos del arma son:
  Balasreserva: el numero de balas de reserva que tendra el agente (sin contar las del cargador).

  Cargador: la capacidad del cargador que tendra el arma, asi como el numero de balas
  que se tiene actualmente en el cargador, esto se Vera en un arreglo de la siguiente forma:
  [balas_en_el_cargador,capacidad_del_cargador].

  Efectividad: numero que indica que tan buena es el arma, es decir, esto simula
  que el arma funcione correctamente, que no se atasque, etc.
  Para fines del programa este numero sera de 0-9, mientras mas se acerque a 9 significa que
  el arma sera mas efectiva, por otra parte mientras mas se acerque a 0 el arma sera menos efectiva."""
  
  """The different elements of the weapon are:
	Bullets reserve: the number of bullets the agent has (thoose already loaded are not counted).

	Loader: the weapon loader's capacity , such as the number of bullets present in the loader, this will be seen in an array:
	[bullets_in_charger, loaders_capacity]

	Efficency: this number shows the weapon's accuracy, it simulates the well fucntioning of the weapon. 
	This is a number between 0 and 9, the closer it is to 9 the more efective the wepon is, while the closer
	it is to 0, the wepon is less efective."""


   def __init__(self,balasreserva,cargador,efectividad):


      """Si todos los parametros del arma son mayores que 0 (no hay efectividades ni cantidades de balas
      negativas) entonces se pasan dichos parametros."""
      """When all the parametrs of the weapon are bigger than 0 (no efectiveness or bullet quantities negative) 
      then thoose parameters are recieved""""
      if (efectividad>=0 and balasreserva>=0 and cargador[0]>=0 and cargador[1]>=0):
        self.balasreserva = balasreserva
        self.cargador = cargador
        self.efectividad = efectividad

      else:
        """Aqui pasa que si al menos uno de los parametros es menor que 0, entonces se asignaran los valores
        predeterminados al arma: 270 balas de reserva, cargador lleno con capacidad para 30 balas, y la efectividad
        aleatoria entre 0-9."""
       """When there is at least one parameter below 0, then default values are asigned to the wepon: 270 bullets, 
       loader full capacity 30 bullets, and a random efectiveness between 0-9"""
        self.balasreserva = 270
        self.cargador = [30,30]
        self.efectividad = randint(0,9)

   """Metodo que devuelve la efectividad del arma."""
   """Method that returns the weapons efectiveness"""
   def GetEfectividad(self):
	return self.efectividad

   """Metodo que devuelve el numero de balas totales del agente."""
   """Method that returns the number of total bullets of the agent """
   def GetBalasReserva(self):
	return self.balasreserva

   """Metodo que devuelve el numero de balas en el cargador"""
   """Method that returns the number of bullets in the loader """
   def GetBalasCargador(self):
        return self.cargador

   """Metodo de Disparo del arma; cabe mencionar que se disparara solo UNA bala por turno."""
   """Method for Shooting the wepon; every step just ONE bullet is fired  """
   def Disparo(self):
        self.cargador[0]-=1

   """Metodo para Recargar el arma cuando ya no queden balas en el cargador.
   Si el agente ya no tiene balas (ni en el cargador ni sueltas), no se hace nada."""
   """Method for Reloading the weapon, when no bullets are left in the loader.
   The agent performs no action if he has no bullets left in the loader and in the reserve  """
   
   def Recarga(self):

       """Si las balas de reserva son mas o la misma cantidad que la capacidad del cargador entonces
       se Recarga el cargador completo."""
       """When the bullets in the reserve are more or the same number that the loaders capacity then loader ir
       Reloaded to its full capacity"""
       
       if self.balasreserva >= self.cargador[1] :
           self.cargador[0]=self.cargador[1]
           self.balasreserva-=cargador

       elif self.balasreserva < self.cargador[1] :

          """Si las balas de reserva son menos que la capacidad del cargador entonces se cargan solo
          las balas que quedan al cargador."""
          """When reserve bullets are less than the loaders capacity then only the bullets left are loaded """
          self.cargador[0]=self.balasreserva
          self.balasreserva=0

   """Metodo que indica si quedan balas en el arma (True si quedan balas ya sea en el cargador o de reserva,
   False si no le quedan mas balas)."""
   
   """Method that shows when there are bullets left in the weapon (True if there are either in the loader or in the reserve
   False if tehre are no bullets left) """
   
   def hayBalas(self):
       if self.balasreserva+self.cargador[0]>0:
           return "True"

       else:
          return "False"

   """Metodo que indica si es necesario que el arma sea Recargada, es decir, que se acaban las balas en el
   cargador y aun quedan balas de reserva."""
   """Method that shows if Reloading is necesary, this means the loader is empty but the agent still has bullets in his reserve"""
   def NecesarioRecargar(self):
      if self.cargador[0]==0 and self.balasreserva>0:
         return "True"

      else:
         return "False"

   """Metodo que imprime las caracteristicas del arma en una cadena."""
   """Method that prints weapon's characteristics in a string"""
   def __str__(self):
       cadena = "Cargador: ["+str(self.cargador[0])+"/"+str(self.cargador[1])+"]. Balas de reserva: "+str(self.balasreserva)+". Total balas (reserva y en cargador): "+str(self.balasreserva+self.cargador[0])
       return cadena
