#!/usr/bin/env python


"""Clase Celda para el programa psicos"""
"""Cell class for PSICOS """
class Celda:

        """La celda es el automata de dos estados donde se mueven los agentes.
        Sus elementos son:

        Blindaje: este elemento sirve en particular en el metodo Pelear; el blindaje le ayudara al agente
        a protegerse y asi aumentar sus probabilidades de sobrevivir al ataque del enemigo.

        Camuflaje: este elemento se utiliza para evitar ser visto por el enemigo, es decir, el camuflaje le
        ayudara a un agente a evitar estar en la vision (vease la clase Agente) del enemigo.

        Movilidad: este elemento es utilizado como catalizador al momento de que el agente se mueva, es decir,
        dependiendo del valor facilitarara o dificultara el movimiento del agente.

        Occ: indica si la celda esta ocupada o no por un agente."""
		
		"""The cell is the two state automaton were the agents move. Their elements are:
		
        Blindage: works fot the Fighting method, it will help the agent to protect himself and so to 
        increase survival probability when attacked by the enemy.
        
        Camouflage: prevents being seen by the enemy, will help the agent not to appear i the vision of the enemy.
        
        Mobility: catalizes the agents movement, depending on its value it will increase or decrease the agents hability to move.
        
        Occ: tells if the cell is ocupied or not."""


        #NO SE PARA QUE SIRVA EL TERRENO, BIEN PODEMOS QUEDARNOS SOLO CON LA MOVILIDAD:
        def __init__(self,x,y,blindaje,camuflaje,movilidad,terreno):
		self.coords = [x,y]
		self.blindaje=blindaje
		self.camuflaje=camuflaje
		self.movilidad=movilidad
		self.terreno=terreno
		self.occ="False"
############################ACB-13-2-13###############################################################################################################################


        '''
        Metodos para  calcular el  peso de atravesar una  celda  dada, necesarios  para  aplicar el metodo Astar
        '''
        '''Method for computing the weight for passing through a given cell, needed for aplying the Astar method '''
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

