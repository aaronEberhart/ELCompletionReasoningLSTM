from Statement import *
from numpy import array
import numpy

"""
Completion rules:

(1) C ⊑ D,A ⊑ C                         ⊨ A ⊑ D    2

(2) C1 ⊓ C2 ⊑ D, A ⊑ C1, A ⊑ C2         ⊨ A ⊑ D    3
    uses Null
(3) C ⊑ ∃R.D, A ⊑ C                     ⊨ A ⊑ ∃R.D 2

(4) ∃R.C ⊑ D, A ⊑ ∃R.B, B ⊑ C           ⊨ A ⊑ D    3
    uses Null
(5) R ⊑ S, A ⊑ ∃R.B                     ⊨ A ⊑ ∃S.B 2

(6) R1 ∘ R2 ⊑ R, A ⊑ ∃R1.B, B ⊑ ∃R2.C   ⊨ A ⊑ ∃R.C 3

"""

class DependencyReducer:
    
    def __init__(self,kbTerms,*logs):
        self.kb = kbTerms
        self.rawlogs = [x for x in logs]
        self.donelogs = []
        self.reduceLogs()
        
    def reduceLogs(self):
        for iterLog in self.rawlogs:
            thisIter = []
            for logType in iterLog:
                thisType = []
                for log in logType:
                    removals = []
                    for term in log[2]:
                        types = self.determineType(term)
                        if not self.inKB(types,term):   
                            thing = self.fixTerm(types,term,thisType,thisIter)
                            if thing == None:
                                pass
                            log[2] = log[2] + thing
                            removals.append(term)             
                    for i in range(0,len(log[2])):
                        for j in range(i+1,len(log[2])):
                            if self.equals(self.determineType(log[2][i]),log[2][i],log[2][j]): 
                                del log[2][j]
                                break         
                    for term in removals:
                        log[2].remove(term)                    
                    thisType.append(log)
                thisIter.append(thisType)
            self.donelogs.append(thisIter)
        
    def determineType(self,term):
        if isinstance(term.antecedent,RoleChain): return 5
        elif isinstance(term.consequent,Role): return 4
        elif isinstance(term.antecedent,ConceptRole): return 3
        elif isinstance(term.consequent,ConceptRole): return 2
        elif isinstance(term.antecedent,ConceptStatement): return 1
        elif isinstance(term.antecedent,Concept): return 0
           
    def inKB(self,termType,term):
        if termType == 0 and term.antecedent.name == term.consequent.name: return True
        for x in self.kb[termType]:
            if self.equals(termType,term,x): return True
        return False

    def fixTerm(self,types,term,thisType,thisIter):
        for log in thisType:
            if self.equals(types,term,log[0]):
                return log[2]
        for logType in thisIter:
            for log in logType:
                if self.equals(types,term,log[0]):
                    return log[2]           
        for iterLog in self.donelogs:
            for logType in iterLog:
                for log in logType:
                    if self.equals(types,term,log[0]):
                        return log[2]
        print("NOOOOOOOOOOO")
    
    def equals(self,types,item1,item2):
        if types != self.determineType(item2): return False
        if types == 0:
            return item1.antecedent.name == item2.antecedent.name and item1.consequent.name == item2.consequent.name
        elif types == 1:
            return item1.antecedent.antecedent.name == item2.antecedent.antecedent.name and item1.antecedent.consequent.name == item2.antecedent.consequent.name and item1.consequent.name == item2.consequent.name
        elif types == 2:
            return item1.antecedent.name == item2.antecedent.name and item1.consequent.role.name == item2.consequent.role.name and item1.consequent.concept.name == item2.consequent.concept.name  
        elif types == 3:
            return item1.consequent.name == item2.consequent.name and item1.antecedent.role.name == item2.antecedent.role.name and item1.antecedent.concept.name == item2.antecedent.concept.name 
        elif types == 4:
            return item1.antecedent.name == item2.antecedent.name and item1.consequent.name == item2.consequent.name
        elif types == 5:
            return item1.antecedent.roles[0].name == item2.antecedent.roles[0].name and item1.antecedent.roles[1].name == item2.antecedent.roles[1].name and item1.consequent.name == item2.consequent.name        
    
    def toString(self,rules):
        return "\n".join(["{}: ({}){}".format(rule[0].toString(),str(rule[1]+1),",".join([x.toString() for x in rule[2]])) for rule in rules])
    
    def correctRange(self,log1,log2):
        return(max(log1,log2) if log1 != 0 and log2 != 0 else (log1 if log2 == 0 else (log2 if log1 == 0 else 0)))
        
    def supportVector(self,maxwid,maxlen,concepts,roles):
        supports = numpy.zeros((maxwid,maxlen))
        
        for i in range(len(self.donelogs)):
            step = []
            for col in self.donelogs[i]:
                for statement in col:
                    for dependency in statement[2]:
                        step.extend(dependency.toVector(concepts,roles))
            while len(step) < maxlen:
                step.extend(array([0,0,0,0]))
            if len(step) > len(supports[i]):
                return 0
            supports[i] = array(step)
        
        return supports
        
    def toVector(self,concepts,roles):
        
        ans = []
        vec = []
        maxa = 0
        maxv = 0
        for i in range(0,len(self.donelogs[0])):
            itera = []
            iterb = []
            if (i > len(self.donelogs[1])):
                print(self.kb.toString())
            for j in range(0,self.correctRange(len(self.donelogs[0]),len(self.donelogs[1]))):
                if j < len(self.donelogs[0][i]): itera = itera + [array(x.toVector(concepts,roles)) for x in self.donelogs[0][i][j][2]]
                if j < len(self.donelogs[1][i]): itera = itera + [array(x.toVector(concepts,roles)) for x in self.donelogs[1][i][j][2]]
                if j < len(self.donelogs[0][i]) and j < len(self.donelogs[1][i]):
                    iterb.append(array(self.donelogs[0][i][j][0].toVector(concepts,roles)))
                    iterb.append(array(self.donelogs[1][i][j][0].toVector(concepts,roles)))
                if j < len(self.donelogs[0][i]):
                    iterb.append(array(self.donelogs[0][i][j][0].toVector(concepts,roles)))
                if j < len(self.donelogs[1][i]):
                    iterb.append(array(self.donelogs[1][i][j][0].toVector(concepts,roles)))
            if len(itera) > maxv: maxv = len(itera)
            if len(iterb) > maxa: maxa = len(iterb)
            vec.append(itera)
            ans.append(iterb)   
        for i in range(0,len(self.donelogs[2])):
            itera = []
            iterb = []
            for j in range(0,len(self.donelogs[2][i])): 
                itera = itera + [array(x.toVector(concepts,roles)) for x in self.donelogs[2][i][j][2]]
                iterb.append(array(self.donelogs[2][i][j][0].toVector(concepts,roles)))
            if len(itera) > maxv: maxv = len(itera)
            if len(iterb) > maxa: maxa = len(iterb)
            vec.append(itera)
            ans.append(iterb)
        
        v = []
        a = []
        for i in range(0,len(vec)):
            itera = vec[i][0]
            for j in range(1,maxv):
                if j < len(vec[i]): itera = numpy.concatenate((itera,vec[i][j]),axis=None)
                else: itera = numpy.concatenate((itera,array([0.0,0.0,0.0,0.0])),axis=None)
            v.append(array(itera))
        for i in range(0,len(ans)):
            itera = ans[i][0]
            for j in range(1,maxa):
                if j < len(ans[i]): itera = numpy.concatenate((itera,ans[i][j]),axis=None)
                else: itera = numpy.concatenate((itera,array([0.0,0.0,0.0,0.0])),axis=None)
            a.append(array(itera))    
            
        
        return array(v),array(a)
    
