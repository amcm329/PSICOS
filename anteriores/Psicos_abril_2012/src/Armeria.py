# !/usr/bin/python
# *- coding: utf-8 -*

from Arma import *

#Arma_yo(self,danho,efectividad,calibre,longitud_canon,peso,balasreserva,cargador,calentamientomax):
#Arma_Juan((self,calibre,numbalas,daño,balasronda,peso,longitudcanon)
class Armeria:

 def __init__(self):
        self.inventario = {}
       # Arma(0.5,,7.65,,0.63,,[7,7],,)
        self.inventario[Browing_1900] = Arma(,,,7,0.63,10.2)
        self.inventario[Hallrifle] = Arma(137.16,1,0.3,0.0,1,1,4.86,82.5)
        self.inventario[Mosquete_1809_Prusiano] = Arma(19.05,1,0.4,1,1,4,104.5)
        self.inventario[Coltrifle3] = Arma(1.4224,5,0.45,1,3.45,68.54)
        self.inventario[Winchester1866] = Arma(1.1176,30,0.5,1,4.2,58.5)
        self.inventario[LeMatRevolverRifle] = Arma(15.24,9,0.25,2,2.2,62.8)
        self.inventario[Henry1860] = Arma(1.1176,15,0.4,1,4,51)
        self.inventario[SpencerRifle] = Arma(1.3208,7,0.53,1,4.55,72)
        self.inventario[SchmidtRubinM1889] = Arma(0.75,12,0.74,1,4.45,78)


 def getArma(self,arma):
         return self.inventario[arma]

 def listadoArmas(self):
        cad = "Armas disponibles: "
        for i in self.inventario:
            cad += i + "\n"
        return cad