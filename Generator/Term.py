class Term:
	
	def __init__(self,t):
		self.checkTerm(t)
		self.term = t
	
	def getTerm(self):
		return self.term
	
	def setTerm(self,t):
		self.term = t
	
	def toString(self):
		return str(self.term)
	
	def equals(self,other):
		return self.term == other.getTerm()
	
	def checkTerm(self,t):
		if not isinstance(t,(int,float,complex,str,bool)): raise Exception("Invalid Term")
	
class Terms:
	
	def __init__(self,args):
		self.checkTerms(args)
		self.terms = [Term(term) for term in args]
	
	def checkTerms(self,terms):
		if not isinstance(terms,list): raise Exception("Invalid Terms")
	
	def toString(self):
		ret = ""
		for i in range(0, len(self.terms)):
			ret = ret + self.terms[i].toString()
			if i != len(self.terms) - 1:
				ret = ret + ","
		return ret
	
	def getTerms(self):
		return self.terms
	
	def getTerm(self,i):
		return self.terms[i].getTerm()
	
	def setTerm(self,i,term):
		x = Term(term)
		self.terms[i] = x
	
	def len(self):
		return len(self.terms)
	
	def equals(self,other):
		if self.len() != other.len(): return False
		for i in range(0,self.len()):
			if not self.getTerm(i) == other.getTerm(i):
				return False
		return True