from VersionClass import Model
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import scipy.stats


#ENSAE
#chemin='//paradis/eleves/MAMESTOY/Bureau/projet Chopin/data.txt'

#maison
chemin='C:/Users/Matteo/Desktop/Projet Chopin/Projet_Git/Projet-Space-State-Model/Data.txt'


def prior(theta,t,Vu):
	L=sc.stats.norm.pdf(theta['b0']*Vu['b0'])
	L*=sc.stats.norm.pdf(theta['b1']*Vu['b1'])
	L*=sc.stats.norm.pdf(theta['b2']*Vu['b2'])
	L*=sc.stats.norm.pdf(theta['b3']*Vu['b3'])
	L*=sc.stats.norm.pdf(theta['b5']*Vu['b5'])
	L*=sc.stats.norm.pdf(theta['b6']*Vu['b6'])
	L*=sc.stats.norm.pdf(theta['b7']*Vu['b7'])
	L*=sc.stats.invgamma(0.5*t,(t-2)/10).pdf(theta['Seps']*Vu['Seps'])
	L*=sc.stats.invgamma(0.5*t,(t-2)/10).pdf(theta['Sw']*Vu['Sw'])
	if (Vu['b4']==0):
		return(L)
	else:
		L*=sc.stats.gamma(1,10).pdf(theta['b4']*Vu['b4'])
		return (L)








def g(x):
	return(x)


# b4 positive represents the population size at which the per-individual birth rate is half of what it would be if mating was not limited

#Modele
def FunM4(N,theta):
	def f (x):
		return(x*np.exp(theta['b5']+theta['b6']*x+theta['b7']*x**2+np.random.normal(0,theta['Seps'])))
	return (list(map(f,N)))
	
	
	
#Donnees
Y=np.loadtxt(chemin)


#Theta

Theta={}
Theta['N0']=1.2
Theta['Seps']=12
Theta['Sw']=12
Theta['b0']=0.1
Theta['b1']=0.1
Theta['b2']=-1
Theta['b3']=1
Theta['b5']=0
Theta['b6']=0
Theta['b7']=0
Theta['b4']=10


#Variables Utiles

Vu={}
Vu['N0']=1
Vu['Seps']=1
Vu['Sw']=1
Vu['b0']=0
Vu['b1']=0
Vu['b2']=0
Vu['b3']=0
Vu['b5']=1
Vu['b6']=1
Vu['b7']=1
Vu['b4']=0





M4=Model(Y,FunM4,g,Theta,prior,Vu)


#Proposal Brownien
#********************************************************************************************



Var=np.identity(11)/10000




def p4(thet):
	
	t=list(thet.values())
	t=t+np.random.multivariate_normal(np.zeros(11),Var)
	return (dict(zip(thet.keys(),t)))
	
	
def ratio4(a,b):
	return(1)
	


sol=M4.Metropolis_Hastings(100,20,Theta,p4,ratio4)
sol=np.asarray(sol)
plt.plot(sol[:,0])
plt.show()