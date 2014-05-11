#!/usr/bin/python

from random import *
from Mapa import *
from Arma import *

"""Clase Agente para el programa psicos.
La descripcion de los elementos es la siguiente: 
Ident: el identificador numerico (unico) que se le asigna a cada agente; cabe mencionar que si el agente
es eliminado su identificador no se le asigna a ningun otro agente.

Coords: un arreglo de la forma [x,y] que ubica al agente dentro de las listas mapa y ejercito (para mas informacion
vease la clase psicos01).

Velmax: la velocidad maxima que puede alcanzar el agente.

Rango: como en cualquier ejercito, identifica a los agentes. Para motivos de este
progama existen 2 rangos: "lider" y "soldado". Se hizo asi esta distincion porque
dependiendo del rango del agente indica la capacidad de movimiento de este.
En el caso de un lider su movimiento estara dado por el algoritmo A*, mientras que para
un soldado su movimiento estara dado por las reglas de movimiento de la clase Agente
(vease metodo mover_soldado).

Bando: indica a que ejercito pertenece el agente. Hay dos disponibles: rojo y azul.

Status: indica el estado del agente (True si esta vivo, False si no).

Arma: el arma del agente (para mas informacion vease la clase Arma).

Personalidad: este es un arreglo que contiene informacion mas precisa del agente a continuacion se muestra
lo que contiene dicho arreglo:

El vector de personalidad esta conformado por = [def,att,num_attacks,rv,coh,vel,sep_min,blindaje,cover], donde:

def = defensa (vease el metodo pelear). 
att = ataque (vease el metodo pelear).
num_attacks = numero de ataques que puede hacer el agente (vease el metodo pelear).
rv = rango de vision (vease el metodo ver).
coh = cohesion (fuerza de atraccion entre los agentes, vease el metodo mover).
vel = velocidad (no confundir con el atributo velmax del Agente, vease el metodo mover).
sep_min = separacion  minima (vease el metodo mover).
blindaje = idem (vease el metodo pelear).
#############
mensaje = Buffer de comunicacion del agente
############ """

#AQUI NO SE PARA QUE SIRVE EL ATRIBUTO COVER DEL VECTOR DE PERSONALIDAD.

class Agente:

        """Se inicializan los atributos del Agente."""
	def __init__(self,ident,x,y,velmax,rango,bando,status,arma,personalidad):
                self.ident=ident

                """Coords se tomara como un arreglo [x,y]."""
                self.x=x
                self.y=y
                self.velmax=velmax
                self.rango=rango
		self.bando=bando
		self.personalidad=personalidad
		self.status=status
		self.vision=[]

                """Esta es el arma del agente"""
                self.arma = arma

	##############################
		"""Modificado por Juan para la parte de la red de comunicaciones"""
		self.mensaje = ""
	##############################

        def getId(self):
            return self.ident

        def getRango(self):
            return self.rango

        def getVelMax(self):
            return self.velmax

        def getX(self):
            return self.x

        def getY(self):
            return self.y

        def setX(self,valor):
            self.x=valor

        def setY(self,valor):
            self.y=valor

        def getBando(self):
            return self.bando

        def getStatus(self):
            return self.status

        def setStatus(self,valor):
            self.status = valor

        def limpiaVision(self):
            self.vision = []

        """Metodo que imprime las caracteristicas del agente."""
        def imprimeCaracAgente(self):
            print "id.: " + str(self.getId()) + "; rango: " + str(self.getRango()) + "; bando: " + str(self.getBando()) + "; coords: " +"(" + str(self.getX()) + "," + str(self.getY()) + ")" + "; vel. max.: " + str(self.getVelMax()) + "; status: " + str(self.getStatus()) + "; personalidad: " + str(self.personalidad)

        """Metodo del Agente para ver, esto es, la lista vision se llenara con Celdas en un rango
        limitado por el atributo "rv" del array de parsonalidad."""
	def ver(self,mapa):
            
            """Los siguientes 4 valores indican el rango en que se ira llenando la vision del agente, como
            su nombre lo indica son rangos minimos y maximos tanto para el eje x como para el eje y. Notamos ademas
            que tofdos estos valores dependen tanto de la posicion del agente (en coordenadas x,y) como del rango
            de vision "rv" """
            rangoxmin = self.getX()-self.personalidad["rv"]
            rangoxmax = self.getX()+self.personalidad["rv"]
            rangoymin = self.getY()-self.personalidad["rv"]
            rangoymax = self.getY()+self.personalidad["rv"]

            for x in range (rangoxmin,rangoxmax):
                for y in range (rangoymin,rangoymax):
                     """Si el rango de vision del agente es valido en el mapa, entonces los elementos que pueda 
                     "ver" el agente se iran agregando a su vision, incluyendo el lugar donde esta parado
                     (recordemos que la vision es una lista de celdas)"""

                     #La primera parte del if (de izquierda a derecha) es para asegurar que la vision no se pase
                     #del rango inferior, mientras que la segunda parte es para asegurar que la vision no se pase
                     #del rango superior (los parentesis en el if fueron solo para distinguir las condiciones
                     #logicas, no tienen otro efecto).
                     if (x >= 0 and y >= 0) and (x<mapa.getXmax() and y<mapa.getYmax()):

                        #Aqui entra en juego el atributo camuflaje de la celda (vease clase Celda),
                        #mientras mayor sea el valor del camuflaje mayor facilidad tendra el agente de NO
                        #ser visto, en particular (que tiene un valor de 0-10) si es mayor o igual a 5
                        #entonces la celda en cuestion NO sera agregada a la vision del agente que esta "mirando".
                        #Tampoco se agregan celdas vacias en la vision del agente.
                        #Como dato adicional NO se agrega en la vision del agente la celda en la que se encuentra sin importar
                        #el valor de su camuflaje.
                        if mapa.getCelda(x,y).getCamuflaje() < 6  and (mapa.getCelda(x,y).getX()!=self.getX() and mapa.getCelda(x,y).getY()!=self.getY()) and mapa.getAgente(x,y)!="":
                            print "Camuflaje: " + str(mapa.getCelda(x,y).getCamuflaje()) + "celda: (" + str(mapa.getCelda(x,y).getX())+","+str(mapa.getCelda(x,y).getY())+")"
                            self.vision.append(mapa.getCelda(x,y))

        """Metodo en el que se imprime lo que el agente ve mediante el metodo ver (solo el terreno).
        Nota: el agente ve todas las celdas pertinentes NO vacias, excepto en la que esta parado, osease
        la propia."""
        def imprimeVision(self):
            print "El agente " + str(self.getId()) + "ve las celdas: "
            for i in range(0,len(self.vision)):
               """Esta parte es para indicar cual es la celda en la que esta parado el agente."""
               if self.vision[i].getX()!=self.getX() and self.vision[i].getY()!=self.getY():
                  print str(self.vision[i].__str__()) #Cada elemendo de la lista vision es una Celda.

        """Metodo donde el agente pelea, esto es que va a tomar un agente de su vision (vease metodo ver), y
        si este resulta ser del bando enemigo lo va a tratar de eliminar con ayuda de su arma (vease la clase
        Arma); para esto el agente que ataca va a utilizar de su personalidad los atributos "num_attacks", "att",
        y su arma con las caracteristicas correspondientes; por otra parte el agente que va a ser atacado va a
        utilizar los atributos "def" y "blindaje "de su personalidad, esto para evitar que sea eliminado."""
        def pelear(self,mapa):
           print "Turno de pelea del agente: " + str(self.getId()) + "-"+ str(self.getBando())
           
           """Si la vision del agente es nula, o equivalente a decir si la lista vision
           no tiene celdas (vease el metodo ver) significa que el agente NO tiene adyacencias
           y entonces se pasa al else de la linea 216."""
           if len(self.vision)>0:

               """Se "desordena" la lista vision (vease el metodo ver) del agente para que sea mas facil
               elegir un objetivo al azar."""
               shuffle(self.vision)

               for i in self.vision:
                   mapa.getAgente(i.getX(),i.getY()).imprimeCaracAgente()

               print (".-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")

               """"Se inicializa el valor terreno_objetivo al primer elemento de la lista vision y se crea una variable
               que sera el enemigo con el que se va a pelear (llamada target),asi como la referencia al enemigo
               en el mapa (referencia_mapa) por si el agente llega a eliminar a su enemigo."""
               terreno_objetivo = self.vision[randint(0,len(self.vision))-1]
               
               """Importante este paso para que no se tengan celdas "viejas" de batallas anteriores
               y qu apunten a algo vacio."""
               self.limpiaVision()

               """Se busca en el diccionario ejercito (vease clase psicos01) la referencia al agente que tenga las mismas coordenadas
               (atributo coords) que las coordenadas (atributo ubicacion de la clase Celda) de tereno_enemigo.
               Nota: cabe mencionar que como se busca en un diccionario la busqueda es constante por lo que no hay que
               hacer ningun tipo de ciclado para encontrar la referencia deseada."""
               objetivo = mapa.getAgente(terreno_objetivo.getX(),terreno_objetivo.getY())
               print objetivo.imprimeCaracAgente()

               """Se busca en el diccionario mapa (vease clase psicos01) la referencia a la celda que tenga las mismas
               coordenadas (atributo coords) que las coordenadas (atributo coords de la clase Celda) de tereno_enemigo.
               Nota: cabe mencionar que como se busca en un diccionario la busqueda es constante por lo que no hay que
               hacer ningun tipo de ciclado para encontrar la referencia deseada."""
               referencia_mapa = mapa.getCelda(terreno_objetivo.getX(),terreno_objetivo.getY())
                    
               #aqui preguntar si el target tiene que ser forzosamente del mismo bando
               """Si el bando del target es distinto al del agente que pelea, el target esta vivo y el
               agente que pelea tiene balas (ya sea en el cargador o de reserva o ambas) entonces el agente
               que pelea atacara al enemigo."""
               if self.getBando()!=objetivo.getBando() and objetivo.getStatus()=="True" and self.arma.hayBalas()=="True":
                  print "El agente " + str(self.getId()) + " va a atacar al agente " + str(objetivo.getId())

                  oportunidad = 1

                  #Esta es la forma en que se calcula el ataque y la defensa, pero se puede cambiar por lo que
                  #Otto diga.
                  ataque = self.personalidad["att"]  + self.arma.getEfectividad()
                  defensa = objetivo.personalidad["def"] + objetivo.personalidad["blindaje"] + terreno_objetivo.getBlindaje()
                  
                  while (not (oportunidad == self.personalidad["num_attacks"] + 1)) and self.arma.hayBalas()=="True":

                     """Si el agente tiene balas en el cargador(vease la clase Arma) entonces procedera
                     a hacer el disparo.
                     Si no tiene balas en el cargador pero aun le quedan balas "sueltas" entonces procedera
                     a recargar el arma, pero en la recarga se le ira una oportunidad al agente
                     de eliminar a su contrincante.
                     Si el agente ya no tiene balas "sueltas" ni en el cargador no se hace nada
                     y el agente que ataca pierde sus oportunidades."""
                     print "Oportunidad (" + str(oportunidad) + "/" + str(self.personalidad["num_attacks"]) +"):"
                     print "Municion restante: " + self.arma.__str__()

                     if self.arma.hayBalas()=="False":
                        oportunidad = self.personalidad["num_attacks"]+1
                        print "El agente " + str(self.getId()) + "ya no tiene balas y pierde sus oportunidades."

                     if self.arma.necesarioRecargar()=="True":
                        self.arma.recarga()
                        """Si el agente recarga su arma pierde una oportunidad."""
                        oportunidad+=1
                        print "El agente " + str(self.getId()) + " recarga su arma y pierde una oportunidad."
                       
                     else:
                        """Aqui se hace el disparo; este funciona de la siguiente manera: se toma un numero aleatorio
                        entre 0 y el valor formado por el valor absoluto del ataque menos la defensa;
                        si es menor que la efectividad entonces se procede a realizar UN disparo, siempre y
                        cuando se tengan balas, de lo contario no se hace nada."""
                        self.arma.disparo()
                        aleatorio = randint(0,abs(ataque-defensa))
                        print "El agente " + str(self.getId()) + " dispara al agente " + str(objetivo.getId()) + "."
                       
                        #Esta se supone que es la condicion para que el agente mate a su enemigo, pero bien se puede
                        #cambiar por la que diga Otto.
                        """Aqui el agente le dispara al enemigo y lo logra eliminar."""
                        if aleatorio < (abs((ataque-defensa)/2)):
                          
                           """Aqui simplemente se manda llamar al metodo eliminaAgente (vease la clase Mapa); asi mismo el contador de oportunidades
                           de una vez se actualiza al maximo para garantizar que no se vuelva a entrar en esta
                           parte del disparo, puesto que ya se elimino al enemigo."""
                           mapa.eliminaAgente(objetivo,referencia_mapa)
                           oportunidad = self.personalidad["num_attacks"]+1
                           print "El agente " + str(self.getId()) + " ha eliminado al agente " + str(objetivo.getId())+"."

                        else:
                           print "El agente " + str(self.getId()) + " falla."
                           """Si el agente falla en el tiro se incrementa el contador de oportunidades"""
                           oportunidad+=1
    
               else:

                    """Aqui se imprimen los mensajes en caso de que el agente ya no tenga mas balas,
                    o el objetivo del agente sea del mismo bando o el objetivo ya haya sido eliminado"""
                    if self.arma.hayBalas()=="False":
                      print "El agente " + str(self.getId()) + " ya no tiene mas balas."

                    if self.getBando()==objetivo.getBando():
                      print "El objetivo del agente " + str(self.getId()) + " es el agente " + str(objetivo.getId()) + " del mismo bando"
           else:
              print "El agente " + str(self.getId()) + " no tiene enemigos visibles."



        """Para el metodo mover consideremos lo siguiente:
        Este dependera del rango del agente.
        Para el caso de un soldado el metodo mover sera la suma en coordenadas de
        las reglas de movimiento.
        Para el caso de un lider, el metodo mover sera la aplicacion del algoritmo
        aestrella."""
        def mover(self,mapa):
            if self.getRango()=="lider":
               mover_lider(mapa)

            elif self.getRango()=="soldado":
               mover_soldado(mapa)


        def mover_lider(mapa):
            return 0


        def mover_soldado(mapa):
            coords_finales  = [0,0]
            celda_origen = mapa.getCelda(self.getX(),self.getY())

            if mapa.getAgente(coords_finales.getX(),coords_finales.getY()) == "":
               celda_destino = mapa.getCelda(coords_finales.getX(),coords_finales.getY())
               mapa.mueveAgente(celda_origen,celda_destino)
               print "El agente: " + str(self.getId()) + "se ha movido de: (" + str(celda_origen.getX()) + "," + str(celda_origen.getY()) + ") a: (" + str(celda_destino.getX()) +"," + str(celda_destino.getY()) + ")."

            else:
                print "El agente " + str(self.getId()) + "no se movio. La celda (" + str(celda_destino.getX()) +"," + str(celda_destino.getY()) + ") esta ocupada."


        """Regla 1: mantiene la cohesion entre los agentes de un mismo bando (los acerca)."""
        def rule1(self,mapa):
	    """Se inicializa el centro de masa del grupo de agentes a [0,0]"""
            centro_masa=[0,0]
	    rule1=[0,0]

	    """Se revisa que la vision de cada agente no este vacia"""
	    if len(self.vision)>0:
	       for i in range(0,len(self.vision)):
                   terreno = self.vision[i]

                   """Nota: aqui para lo unico que sirve el boid es para asegurarse que la regla 1 se aplique exclusivamente
                   entre agentes de un mismo bando, ya que por cuestiones de diseno la vision de un agente consta solo
                   de celdas que indican el terreno, no de agentes.
                   Posteriormente para los ifs se pueden usar indistintamente las coordenadas de terreno o de boid
                   pues coinciden."""
                   boid = mapa.getAgente(terreno.getX(),terreno.getY())

		   if terreno.getX()!=self.getX() and terreno.getY()!=self.getY() and self.getBando()==boid.getBando():
                      """Como se necesita mantener cohesion entre agentes DEL MISMO BANDO entonces se pide
                      el agente que se encuentre en una posicion de terreno dada (esto esta en la variable terreno),
                      ya que la vision solo contiene celdas y asi se busca el agente asociado la variable terreno.
                      Luego se busca que el agente (boid) sea del mismo bando que el agente en cuestion para mantener cohesion
                      entre estos y no entre agentes de bandos contrarios.
                      Nota: no hay que preocuparse por referencias nulas (vision con celdas vacias), pues estas ya se
                      contemplan en el metodo ver."""

                      """Se calculan las coordenadas del centro de masa de los boids"""
                      centro_masa[0]+=self.terreno.getX()
		      centro_masa[1]+=self.terreno.getY()

               """Se dividen la diferencia de las coordenadas menos el centro de
               masa entre la tendencia a ir al centro de masa"""
	       rule1[0]=(centro_masa[0]-self.getX())/self.personalidad["coh"]
	       rule1[1]=(centro_masa[1]-self.getY())/self.personalidad["coh"]

               print "La regla 1: " + str(rule1)

            return rule1


        """Regla 2: mantiene una separacion minima entre los agentes (los aleja entre si)."""
	def rule2(self):
	    sep = [0,0]
	    rule2 = [0,0]

            """Se revisa que la vision de cada agente no este vacia"""
	    if len(self.vision)>0:
		   for i in range(0,len(self.vision)):
                       terreno = self.vision[i]

                       """Nota: aqui para lo unico que sirve el boid es para asegurarse que la regla 2 se aplique exclusivamente
                       entre agentes de un mismo bando, ya que por cuestiones de diseno la vision de un agente consta solo
                       de celdas que indican el terreno, no de agentes.
                       Posteriormente para los ifs se pueden usar indistintamente las coordenadas de terreno o de boid
                       pues coinciden."""
                       boid = mapa.getAgente(terreno.getX(),terreno.getY())

		       if terreno.getX()!=self.getX() and terreno.getY()!=self.getY() and self.getBando()==boid.getBando():
			    """Aqui se implementan los criterios de separacion minima."""
			    if abs(self.getX()-terreno.getX())<self.personalidad["sep_min"]:
				  """Distancia de separacion"""
				  sep[0]=sep[0]-(self.getX()-terreno.getX())

                            if abs(self.getY()-terreno.getY())<self.personalidad["sep_min"]:
				  sep[1]=sep[1]-(self.getY()-terreno.getY())


                   #No existe atributo sep
		   rule2[0] = sep[0]/self.personalidad["sep_min"]
		   rule2[1] = sep[1]/self.personalidad["sep_min"]
		   
                   print "La regla 2: " + str(rule2)

            return rule2

        """Regla 3: empareja la vel del agente con las de los demas agentes de su bando."""
	def rule3(self,mapa): 
	    pv=[0,0]
	    if len(self.vision)>0:
	       for i in range(0,len(self.vision)):
		   target = mapa.getAgente(self.vision[i].getX(),self.vision[i].getY())

		   if self.getX()!=target.getX() and self.getY()!=target.getY():
		      for x in range(0,2):

                          """Se revisa que los agentes sean del mismpo bando."""
			  if self.getBando()==target.getBando(): 
			     pv[x]=pv[x]+target.personalidad["vel"] #poner una velocidad
			     pv[x]=pv[x]/len(vision)
			     dif[x]=(pv[x]-self.vel[x])/self.personalidad["vel"]
	    return dif

	def objetivo(self):#va hacia al objetivo
		 dif=[0,0]
		 for i in range(0,2):
			dif[i]=self.obj[i]-self.coords[i]
			dif[i]=dif[i]*self.pers["obj"]
		 return dif

	def fronteras(self,xmin,xmax,ymin,ymax): #te aleja de las fronteras.
		if self.coords[0] < (5+xmin):
			self.vel[0]=self.vel[0]+1
		elif self.coords[0] > (xmax-5):
			self.vel[0]=self.vel[0]-1
		if self.coords[1] < (5+ymin):
			self.vel[1]=self.vel[1]+1
		elif self.coords[1] > (ymax-5):
			self.vel[1]=self.vel[1]-1

	#def move_cover(self): #te mueves a donde haya mas blindaje.
		#d=[0,0]
		#for x in range(-self.personalidad["rv"], self.personalidad["rv"]):
			#for y in range(-self.personalidad["rv"], self.personalidad["rv"]):
				#if (self.vision[x,y]["blindaje"]>=self.personalidad["blindaje"]):
					#d=self.vision[x,y]-self.coords
					#d=d/self.personalidad["cover"]
					#break
		#return d
