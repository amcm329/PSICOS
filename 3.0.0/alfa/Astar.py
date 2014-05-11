#!/usr/bin/env python
###ACB 18-02-2013#####

from Celda import *
from Mapa import *
'''
Implementacion del algoritmo A-estrella para  el programa PSICOS.El algoritmo  A-estrella es un algoritmo de  busqueda, 
que  consiste en disenar rutas ponderando el costo, mediante  una  funcion de  peso heuristico y una  metrica.
La funcion para  calcular  la distancia entre  dos  nodos  es basicamente la distancia del taxista. 

'''

'''A-star algorithm for PSICOS. This is a searching algorithm, it desings paths by evaluating it's cost, through and 
heuristic weight function and a metric. The distance between two nodes is computed using the Taxicab Metric '''

def distancia_nodos(pos,obj):

    distx=abs(pos.x-obj.x)
    disty=abs(pos.y-obj.y)
    return [distx+disty]

def D(celda):
     l=[] 
     for i in celda.vecinos:
         l.append(i.gscore)
     return min(l)

 ###Funcion de peso g###

def g(inicio,pos):
     """
     La funcion g calcula  el costo exacto de la distancia  recorrida desde el nodo inicial  a la posicion actual.
     """
     """ g function computes the exact cost from the starting node to the current position
     """
     return (pos.costo-inicio.costo)*distancia_nodos(inicio,pos)

 ###Funcion de peso heuristico h###

def h(pos,obj):
     """
     La funcion h es el calculo heuristico del paso de la  posicion  actual  al objetivo.
     """
     """h function computes the heuristics in the step from current position to objective
     """
     return D(pos)*(distancia_nodos(pos,obj))


 ###Peso promedio f###
def f(inicio,obj):
     """
    
     La funcion f calcula el peso dado por la distancia (taxicab) de la posicion inicial a la posicion actual, 
     dada por g y el costo heuristico desde la posicion al objetivo.
    
     """
     """ f function computes the weight given by the taxicab distance from intial postion to current position,
     given by g and the heuristic cost from current position to objective.
     """
     return g(inicio,obj)+h(inicio,obj)

def aestrella(inicio,obj):
    """
    El algoritmo Aestrella es una forma  sencilla de  buscar rutas de bajo costo.
    En nuestro caso necesitamos  que los agentes  puedan reconocer elterreno, 
    es decir leer mapas y trazar rutas.
    El algoritmo  consiste  en preguntar  en la  vecindad por cual nodo es menos costoso pasar
    """
    """
    A-star algorithm is a simple way of searching for low cost paths.
    In our problem we need the agents to recognize the terrain,
    this means reading maps and drawing paths.
    The algorithm asks for the lowest cost node for moving
    """
    nodos_abiertos=[inicio]
    nodos_cerrados=[]
    lista1=[]
    for cel in nodos_abiertos:
        lista1.append(cel.costo)
    m=min(lista1)
    for j in nodos_abiertos:
        j.set_gscore(g(inicio,j))
        j.set_hscore(h(j,obj))
        j.set_fscore(f(inicio,obj))
        if j.fscore==m:
            if j==obj:
                print'terminado'
                nodos_cerrados.append(j)
            else:
                nodos_abiertos.append(j)
                for k in j.vecinos:
                    if k in nodos_cerrados :
                        gk=k.gscore
                        gk1=k.get_gscore()
                        if gk1<=gk:
                            k.set_gscore=gk1
                            j=k
                        else:
                            pass
                    elif k in nodos_abiertos:
                        gk=k.gscore
                        gk1=k.get_gscore
                        if gk1<=gk:
                            k.set_gscore=gk1
                            j=k
                        else:
                            pass
                        
                    else:
                        nodos_abiertos.append(k)
                        k.set_gscore()
        else:
            pass
    ruta=[]    
    for u in nodos_cerrados:
        lnc=len(nodos_cerrados)
        for v in range(lnc):
            ruta.insert(v,nodos_cerrados[lnc-v])
    return ruta
