import numpy as np



class Model:
	
	def __init__(self,Y,fun_model,g,theta,prior,varutile):
		self.donnees = Y
		self.g=g
		self.model=fun_model
		self.theta=theta
		self.prior=prior 
		self.varutile=varutile
	def param(self):
		return()
			
	def dens_norm(self,N,M,t):# calcule les w de 1 a M
		sol=np.zeros(M)
		for i in range(M):
			sol[i]=(1/np.sqrt(2*np.pi*self.theta['Sw']))*np.exp(-((N[i]-self.donnees[t])**2)/(2*self.theta['Sw']))
		return sol
		
	def Resample(self,w,Nbre_tirages):#w doivent etre normalises
		u=np.random.uniform(0,1)
		cnw = Nbre_tirages*np.cumsum(w)
		j=0
		Ind = np.empty(Nbre_tirages,dtype="int")
		for k in range(Nbre_tirages):
			while cnw[j]<u:
				j = j+1
			Ind[k] = j
			u = u + 1.
		return (Ind)
	
	def select(self,L,Ind):
		l=[]
		for i in Ind:
			l.append(L[i])
		return(l)		
		
	def FiltreParticulaire (self,M):
		N=[self.theta['N0']]*M
		W=np.zeros(M)
		L=0
	
		#Initialisation
		N=self.model(N,self.theta)
		W=self.dens_norm(N,M,0)
		L=np.log(np.mean(W))
		#heredite
		for i in range(1,len(self.donnees)):
			#resample
			Indices=self.Resample(W/sum(W),M)
			N=self.select(N,Indices)
			N=self.model(N,self.theta)
			W=self.dens_norm(N,M,i)
			L+=np.log(np.mean(W))
		return(L)

	def Metropolis_Hastings(self,N_FP,Nbre_It,Theta0,proposal,ratio):
		Theta=[list(Theta0.values())]*Nbre_It
		self.theta=Theta0
		T=len(self.donnees)
		
		Pi=self.FiltreParticulaire(N_FP)
		
		for i in range(1,Nbre_It):
			
			anc_theta=self.theta
			self.theta=proposal(anc_theta)
			Piprim=self.FiltreParticulaire(N_FP)
			u=np.random.uniform()
			#(self.prior(self.theta,T)/self.prior(anc_theta,T))*(Piprim/Pi)*ratio(self.theta,anc_theta)>u
			if ((self.prior(self.theta,T,self.varutile)/self.prior(anc_theta,T,self.varutile))*(np.exp(Piprim-Pi))*ratio(self.theta,anc_theta)>u):
				Theta[i]=list((self.theta).values())
				Pi=Piprim
			else:
				Theta[i]=Theta[i-1]
				self.theta=anc_theta
		return (Theta)		
				
		
	
	
		
		
		
		
		
		
		
		
		
		
		
		

