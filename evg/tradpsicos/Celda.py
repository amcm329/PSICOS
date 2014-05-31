#!/usr/bin/env python


#Cell class for PSICOS
class Celda:

		"""The cell is the two state automaton were the agents move. Their elements are:
		
        Blindage: works fot the Fighting method, it will help the agent to protect himself and so to 
        increase survival probability when attacked by the enemy.
        
        Camouflage: prevents being seen by the enemy, will help the agent not to appear i the vision of the enemy.
        
        Mobility: catalizes the agents movement, depending on its value it will increase or decrease the agents hability to move.
        
        Occ: tells if the cell is ocupied or not.
        """


        #NO SE PARA QUE SIRVA EL TERRENO, BIEN PODEMOS QUEDARNOS SOLO CON LA MOVILIDAD:
		def __init__(self,x,y,blindaje,camuflaje,movilidad,terreno):
			self.coords = [x,y]
			self.blindaje=blindaje
			self.camuflaje=camuflaje
			self.movilidad=movilidad
			self.terreno=terreno
			self.occ="False"
############################ACB-13-2-13###############################################################################################################################


       
        #Metodos para  calcular el  peso de atravesar una  celda  dada, necesarios  para  aplicar el metodo Astar
        
        #Method for computing the weight for passing through a given cell, needed for aplying the Astar method '''
		def set_gscore(self,valor):
			self.gscore=valor

		def get_gscore(self):
			return self.gscore

		def set_hscore(self,valor):
			self.hscore=valor 

		def get_hscore(self):
			return self.hscore

		def set_fscore(self,valor):
			self.fscore=valor 

		def get_fscore(self):
			return self.fscore

#####################################################################################################################################################################

