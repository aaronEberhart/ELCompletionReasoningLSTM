from Statement import *

"""
Completion rules:

(1) C ⊑ D,A ⊑ C                         |= A ⊑ D

(2) C1 ⊓ C2 ⊑ D, A ⊑ C1, A ⊑ C2         |= A ⊑ D

(3) C ⊑ ∃R.D, A ⊑ C                     |= A ⊑ ∃R.D

(4) ∃R.C ⊑ D, A ⊑ ∃R.B, B ⊑ C           |= A ⊑ D

(5) R ⊑ S, A ⊑ ∃R.B                     |= A ⊑ ∃S.B

(6) R1 ∘ R2 ⊑ R, A ⊑ ∃R1.B, B ⊑ ∃R2.C   |= A ⊑ ∃R.C

"""

class ReasonER:
	
	def __init__(self,genERator,showSteps=False):
		self.hasRun = False
		self.syntheticData = genERator
		self.showSteps = showSteps
		if not self.syntheticData.hasRun:
			self.syntheticData.genERate()
		self.newCType1 = []
		self.knownCType1 = []
		self.numKnownCType1 = 0
		self.newCType3 = []
		self.knownCType3 = []
		self.numKnownCType3 = 0
		self.log = "" if not showSteps else "Reasoner Steps"
	
	def ERason(self):
		if self.hasRun: return
		
		self.trySolveRules(0)
		
		i = 1
		while self.hasGrown():
			self.trySolveRules(i)
			i = i + 1
		 
		self.knownCType1.sort(key=lambda x: (x.antecedent.name, x.consequent.name))
		self.knownCType3.sort(key=lambda x: (x.antecedent.name, x.consequent.role.name, x.consequent.concept.name))
		
		self.hasRun = True
			
	def trySolveRules(self,i):
		self.solveRule1()
		self.solveRule2()
		self.solveRule3()
		self.solveRule4()
		self.solveRule5()
		self.solveRule6()
		self.pruneNewRules(i)
		
	def pruneNewRules(self,i):
		c1Known = self.knownCType1 + self.syntheticData.CType1
		c3Known = self.knownCType3 + self.syntheticData.CType3
		for rule in self.newCType1:
			if not self.alreadyKnown(c1Known,rule):
				if self.showSteps: self.log = self.log + "\nLearned {} in loop {}".format(rule.toString(),i)
				self.knownCType1.append(rule)
				c1Known.append(rule)
		for rule in self.newCType3:
			if not self.alreadyKnown(c3Known,rule):
				if self.showSteps: self.log = self.log + "\nLearned {} in loop {}".format(rule.toString(),i)
				self.knownCType3.append(rule)
				c3Known.append(rule)
		self.newCType1 = []
		self.newCType3 = []
	
	def hasGrown(self):
		if len(self.knownCType1) == self.numKnownCType1 and len(self.knownCType3) == self.numKnownCType3: return False
		self.numKnownCType1 = len(self.knownCType1)
		self.numKnownCType3 = len(self.knownCType3)
		return True
	
	def solveRule1(self):
		""" C ⊑ D,A ⊑ C |= A ⊑ D """
		candidates = self.syntheticData.CType1 + self.knownCType1
		
		for candidate1 in candidates:
			for candidate2 in list(filter(lambda x: candidate1.antecedent.name == x.consequent.name,candidates)):
			
				if candidate2.antecedent.name == candidate1.consequent.name: continue
				
				cs = ConceptStatement(0,True,candidate2.antecedent,candidate1.consequent)
				cs.complete('⊑')
				self.newCType1.append(cs)
	
	def solveRule2(self):
		""" C1 ⊓ C2 ⊑ D, A ⊑ C1, A ⊑ C2 |= A ⊑ D """
		candidates = self.syntheticData.CTypeNull + self.syntheticData.CType1 + self.knownCType1
		
		for conjunction in self.syntheticData.CType2:
			for candidate1 in list(filter(lambda x: conjunction.antecedent.antecedent.name == x.consequent.name,candidates)):
				for candidate2 in list(filter(lambda x: conjunction.antecedent.consequent.name == x.consequent.name and x.antecedent.name == candidate1.antecedent.name,candidates)):
					
					if candidate1.antecedent.name == conjunction.consequent.name: continue
					
					cs = ConceptStatement(0,True,candidate1.antecedent,conjunction.consequent)
					cs.complete('⊑')					
					self.newCType1.append(cs)
	
	def solveRule3(self):
		""" C ⊑ ∃R.D, A ⊑ C |= A ⊑ ∃R.D """
		type1Candidates = self.syntheticData.CType1 + self.knownCType1
		type3Candidates = self.syntheticData.CType3 + self.knownCType3
		
		for candidate1 in type3Candidates:
			for candidate2 in list(filter(lambda x: candidate1.antecedent.name == x.consequent.name,type1Candidates)):
				
				cs = ConceptStatement(0,True,candidate2.antecedent,candidate1.consequent)
				cs.complete('⊑')				
				self.newCType3.append(cs)
	
	def solveRule4(self):
		""" ∃R.C ⊑ D, A ⊑ ∃R.B, B ⊑ C |= A ⊑ D """
		type1Candidates = self.syntheticData.CTypeNull + self.syntheticData.CType1 + self.knownCType1
		type3Candidates = self.syntheticData.CType3 + self.knownCType3		
		
		for candidate1 in self.syntheticData.CType4:
			for candidate2 in list(filter(lambda x: candidate1.antecedent.concept.name == x.consequent.name,type1Candidates)):
				for candidate3 in list(filter(lambda x: x.consequent.concept.name == candidate2.antecedent.name,type3Candidates)):
					
					if candidate3.antecedent.name == candidate1.consequent.name: continue
					
					cs = ConceptStatement(0,True,Concept(candidate3.antecedent.name,[0]),Concept(candidate1.consequent.name,[0]))
					cs.complete('⊑')					
					self.newCType1.append(cs)
	
	def solveRule5(self):
		""" R ⊑ S, A ⊑ ∃R.B |= A ⊑ ∃S.B """
		type3Candidates = self.syntheticData.CType3 + self.knownCType3
		
		for roleStatement in self.syntheticData.roleSubs:
			for matchingConceptStatement in list(filter(lambda x: roleStatement.antecedent.name == x.consequent.role.name,type3Candidates)):
				
				cs = ConceptStatement(0,True,matchingConceptStatement.antecedent,ConceptRole('e',roleStatement.consequent,matchingConceptStatement.consequent.concept))
				cs.complete('⊑')				
				self.newCType3.append(cs)
	
	def solveRule6(self):
		""" R1 ∘ R2 ⊑ R, A ⊑ ∃R1.B, B ⊑ ∃R2.C |= A ⊑ ∃R.C """
		type3Candidates = self.syntheticData.CType3 + self.knownCType3
		
		for roleChain in self.syntheticData.roleChains:
			for matchingConceptStatement1 in list(filter(lambda x: roleChain.antecedent.roles[0].name == x.consequent.role.name,type3Candidates)):
				for matchingConceptStatement2 in list(filter(lambda x: x.antecedent.name == matchingConceptStatement1.consequent.concept.name and roleChain.antecedent.roles[1].name == x.consequent.role.name,type3Candidates)):
					
					cs = ConceptStatement(0,True,matchingConceptStatement1.antecedent,ConceptRole('e',Role(roleChain.consequent.name,[0,1]),matchingConceptStatement2.consequent.concept))
					cs.complete('⊑')					
					self.newCType3.append(cs)
					
	def alreadyKnown(self,statements,s):
		return any(x.equals(s) for x in statements)
	
	def getLog(self):
		return self.log
	
	def toString(self):
		ret = "\nExtended KB"
		for statement in self.knownCType1:
			ret = ret + "\n" + statement.toString()
		for statement in self.knownCType3:
			ret = ret + "\n" + statement.toString()
		return ret
	
	def toFunctionalSyntax(self,IRI):
		s = "Prefix(:="+IRI+")\nPrefix(owl:=<http://www.w3.org/2002/07/owl#>)\nOntology( "+IRI+"\n\n"
		for i in range(0,self.syntheticData.conceptNamespace):
			s = s + "Declaration( Class( :C" +  str(i) + " ) )\n"
		for i in range(0,self.syntheticData.roleNamespace):
			s = s + "Declaration( ObjectProperty( :R" + str(i)   + " ) )\n";
		s = s + "\n" + self.syntheticData.toFunctionalSyntax()
		for statement in self.knownCType1:
			s = s + "\n" + statement.toFunctionalSyntax()
		for statement in self.knownCType3:
			s = s + "\n" + statement.toFunctionalSyntax()
		return s + "\n\n)"		
	
	def getStatistics(self):
		
		uniqueConceptNames = []
		allConceptNames = 0
		uniqueRoleNames = []
		allRoleNames = 0
		
		for statement in self.knownCType1:
			if statement.antecedent.name not in uniqueConceptNames: uniqueConceptNames.append(statement.antecedent.name)
			if statement.consequent.name not in uniqueConceptNames: uniqueConceptNames.append(statement.consequent.name)
			allConceptNames = allConceptNames + 2
		for statement in self.knownCType3:
			if statement.antecedent.name not in uniqueConceptNames: uniqueConceptNames.append(statement.antecedent.name)
			if statement.consequent.concept.name not in uniqueConceptNames: uniqueConceptNames.append(statement.consequent.concept.name)
			if statement.consequent.role.name not in uniqueRoleNames: uniqueRoleNames.append(statement.consequent.role.name)
			allConceptNames = allConceptNames + 2
			allRoleNames = allRoleNames + 1
			
		return [["both",["unique",len(uniqueConceptNames)+len(uniqueRoleNames)],["all",allConceptNames+allRoleNames]],["concept",["unique",len(uniqueConceptNames)],["all",allConceptNames]],["role",["unique",len(uniqueRoleNames)],["all",allRoleNames]]]
	