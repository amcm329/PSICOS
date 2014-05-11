#!/usr/bin/env python

from random import *

"""Clase Arma para el programa psicos"""
class Arma:

   """Se describen los elementos del arma:
  Balasreserva: el numero de balas de reserva que tendra el agente (sin contar las del cargador).

  Cargador: la capacidad del cargador que tendra el arma, asi como el numero de balas
  que se tiene actualmente en el cargador, esto se vera en un arreglo de la siguiente forma:
  [balas_en_el_cargador,capacidad_del_cargador].

  Efectividad: numero que indica que tan buena es el arma, es decir, esto simula
  que el arma funcione correctamente, que no se atasque, etc.
  Para fines del programa este numero sera de 0-9, mientras mas se acerque a 9 significa que
  el arma sera mas efectiva, por otra parte mientras mas se acerque a 0 el arma sera menos efectiva."""

   def __init__(self,balasreserva,cargador,efectividad):


      """Si todos los parametros del arma son mayores que 0 (no hay efectividades ni cantidades de balas
      negativas) entonces se pasan dichos parametros."""
      if (efectividad>=0 and balasreserva>=0 and cargador[0]>=0 and cargador[1]>=0):
        self.balasreserva = balasreserva
        self.cargador = cargador
        self.efectividad = efectividad

      else:
        """Aqui pasa que si al menos uno de los parametros es menor que 0, entonces se asignaran los valores
        predeterminados al arma: 270 balas de reserva, cargador lleno con capacidad para 30 balas, y la efectividad
        aleatoria entre 0-9."""
        self.balasreserva = 270
        self.cargador = [30,30]
        self.efectividad = randint(0,9)

   """Metodo que devuelve la efectividad del arma."""
   def getEfectividad(self):
	return self.efectividad

   """Metodo que devuelve el numero de balas totales del agente."""
   def getBalasReserva(self):
	return self.balasreserva

   """Metodo que devuelve el numero de balas en el cargador"""
   def getBalasCargador(self):
        return self.cargador

   """Metodo de disparo del arma; cabe mencionar que se disparara UNA bala por vez."""
   def disparo(self):
        self.cargador[0]-=1

   """Metodo para recargar el arma cuando ya no queden balas en el cargador.
   Si el agente ya no tiene balas (ni en el cargador ni sueltas), no se hace nada."""
   def recarga(self):

       """Si las balas de reserva son mas o la misma cantidad que la capacidad del cargador entonces
       se recarga el cargador completo."""
       if self.balasreserva >= self.cargador[1] :
           self.cargador[0]=self.cargador[1]
           self.balasreserva-=cargador

       elif self.balasreserva < self.cargador[1] :

          """Si las balas de reserva son menos que la capacidad del cargador entonces se cargan solo
          las balas que quedan al cargador."""
          self.cargador[0]=self.balasreserva
          self.balasreserva=0

   """Metodo que indica si quedan balas en el arma (True si quedan balas ya sea en el cargador o de reserva,
   False si no le quedan mas balas)."""
   def hayBalas(self):
       if self.balasreserva+self.cargador[0]>0:
           return "True"

       else:
          return "False"

   """Metodo que indica si es necesario que el arma sea recargada, es decir, que se acaban las balas en el
   cargador y aun quedan balas de reserva."""
   def necesarioRecargar(self):
      if self.cargador[0]==0 and self.balasreserva>0:
         return "True"

      else:
         return "False"

   """Metodo que imprime las caracteristicas del arma en una cadena."""
   def __str__(self):
       cadena = "Cargador: ["+str(self.cargador[0])+"/"+str(self.cargador[1])+"]. Balas de reserva: "+str(self.balasreserva)+". Total balas (reserva y en cargador): "+str(self.balasreserva+self.cargador[0])
       return cadena