#!/usr/bin/env python

def readinterval(textfile,keyword1,keyword2):
	"""funcion para buscar en archivos de texto de gaussian
	   imprime la linea que presenta keyword"""
	try:
		infile=open(textfile,'r')
                cond=False
		while True:
			try:
				linea=infile.readline()
				if keyword1 in linea:
					cond=True

				if cond==True:
					print linea
				
				if keyword2 in linea:
					cond=False
			except EOFError:
				break
				
	except IOError:
		print 'error opening file'

if __name__=="__main__":
	readinterval("/home/otto/netlogo-4.1.3/models/Sample Models/Networks/salida.csv","LINKS","PLOTS")
