import math
from scipy import stats
import numpy as np

##Manage function for geometric things
class VectorTools:

	def __init__(self):
		pass

	##Norme d'un vecteur
	##@param u The vector
	##@return the norme of the vector
	def norme(self, u):
		return math.sqrt(u[0] * u[0] + u[1] * u[1])

	##Déterminant
	##@param u First vector
	##@param v second vector
	##return the determinant of u and v
	def det(self, u, v):
		return u[0] * v[1]-u[1] * v[0]

	##Produit scalaire
	##@param u First vector
	##@param v second vector
	##return the ps of u and v
	def ps(self, u, v):
		return u[0] * v[0] + u[1] * v[1]

	##Vecteur unitaire
	##@param u The vector
	##@return the vecteur unitaire of the vector
	def unitaire(self, u):
		"""vecteur unitaire"""
		return u[0] / self.norme(u), u[1] / self.norme(u)

	##Calcul du symétrique de P par rapport à la droite (AB)
	##@param A first point for (AB)
	##@param B second point for (AB)
	##@param P the vector to get the symetric
	##@return symétrique de P par rapport à la droite (AB)
	def getSymCoord(self, A, B, P):
		""""""
		V = (B[0]-A[0], B[1]-A[1])
		U = (P[0]-A[0], P[1]-A[1])
		u = self.unitaire(U)
		v = self.unitaire(V)
		cost = self.ps(u, v)
		sint = self.det(u, v)
		cos2t = cost * cost-sint * sint #trigo
		sin2t = 2 * sint * cost #trigo
		return [cos2t * U[0]-sin2t * U[1] + A[0], sin2t * U[0] + cos2t * U[1] + A[1]]

	##Calcul du géocentre d'un automate
	##@param L les positions des points
	##@return the geocentre of the automata
	def geo_centre(self, L):  #L liste de listes
		x=0
		y=0
		for i in L:
			x += i[0]
			y += i[1]
		return [x/len(L),y/len(L)]   #on pourra prendre int() si on veut des entiers

	##Set position following circle
	##@param L The listof poiints to replace
	##@param r the radisu of the circle
	##@return Replaced points
	def pos_circle(self, L, r):
		cg=self.geo_centre(L)
		n=len(L)
		alpha=2*math.pi/n
		beta=alpha/2
		if n%2 == 0:                 #cas paire
			k=0
			for i in L:
				i[0] = math.cos(beta+k*alpha)*r+cg[0]
				i[1] = math.sin(beta+k*alpha)*r+cg[1]
				k += 1
		else:                       #cas impaire
			k=0
			for i in L:
				i[0] = math.cos(math.pi/2+k*alpha)*r+cg[0]
				i[1] = math.sin(math.pi/2+k*alpha)*r+cg[1]
				k += 1
		return L

	##Arondie x
	##@param x
	##@return 0 or one following x
	def arond(self, x):                   #x in [0,1]
		if x < 0.5:
			return 0
		else:
			return 1

	##Don't really know what this do ...
	def pos_grid(self, L,r):
		for i in L:
			i[0] = i[0] - i[0] % r + arond((i[0] % r)/r) * r
			i[1] = i[1] - i[1] % r + arond((i[1] % r)/r) * r

	##Calcul la moyenne
	def moy(self, L,e):
		s = 0
		for i in L:
			s += L[e]
		return s / len(L)

	###Definit une droite
	def drt(self, a,b,x):
	    return a * x + b


	def disso(self, L):
		x = []
		y = []
		for i in L:
			x.append(i[0])
			y.append(i[1])
		return x,y

	def pos_line(self, L,v,c):
		if v <= 1:                  #0: vertical, 1: horizontal
			m = moy(L,v)
			for i in L:
				i[v] = m
		elif v in [2,4]:              #2: \, 4: /    Attention: on conserve l'abscisse
			c = self.geo_centre(L)       #le "0,0" du repÃ¨re
			for i in L:
				i[1] = drt(v - 3, 0, i[0]-c[0]) + c[1]
		elif v == 3:                 #3: droite definie par l'utilisateur (coef. directeur)
			c = self.geo_centre(L)
			for i in L:
				i[1] = drt(c, 0, i[0]-c[0]) + c[1]
		else:                       #5: droite mediane (regression linÃ©aire)
			xy = self.disso(L)
			d = stats.linregress(xy[0], xy[1])
			for i in L:
				i[1] = drt(d[0], d[1], i[0])

	def min_max(self, L,p):
		m = L[0][p]
		pm = 0
		M = L[0][p]
		pM = 0
		for i in range(len(L)):
			if L[i][p] > M:
				M = L[i][p]
				pM = i
			if L[i][p] < m:
				m = L[i][p]
				pm = i
			return [[m,pm],[M,pM]]

	##Make the projection of point follwoing a droite
	##@param topleftpoint of droite
	##@param downrightpoint of droite
	##@param point the point to get the projection
	##@return the projection of point following the droite
	def projectLine(self, topleftpoint, downrightpoint, point):
		x = np.array(point)

		u = np.array(topleftpoint)
		v = np.array(downrightpoint)

		n = v - u
		div = math.sqrt(sum(p*p for p in n.tolist()))#Frobenius norm

		if(int(div) == 0):
			div = 1

		n = n/int(div)

		P = u + n*np.dot(x - u, n)
		P = P.tolist()
		return P
