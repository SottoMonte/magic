import itertools
from typing import TypeAlias,NewType
from dataclasses import dataclass,asdict,astuple
import importlib
#from data import Metadato,SPLIT,VARIABLE

@dataclass(frozen=True)
class Metadata:
    type: str
    value: str
    identifier: str  
    cardinality: int
    required:bool = None

def VARIABLE(worker,typee,identifier,value,required=None):
    if hasattr(value,'__iter__'):
        return Metadata(typee,value,identifier,len(value),required)
    elif value == None:
        return Metadata(typee,value,identifier,0,required)
    else:
        return Metadata(typee,value,identifier,1,required)

def SPLIT(worker,target, SEPARATOR, LOCK=None, UNLOCK=None):
    if LOCK is not None and UNLOCK is not None:
        result, temp, block = [], [], 0
        for CHAR in target.value:
            if CHAR == LOCK:
                block += 1
            elif CHAR == UNLOCK:
                block -= 1
            elif CHAR == SEPARATOR and block == 0:
                result.append(temp)
                temp = []
            if CHAR != SEPARATOR:
                temp.append(CHAR)
        if len(temp) != 0:
            result.append(temp)
        return result
    else:
        return [stringa.strip() for stringa in target.value.split(SEPARATOR)]
'''
# Declarative-programming
# Functional-programming
# Logic programming
# Constraint programming
# Constraint logic programming
'''
TARGET = '@Target'
OUTPUT = tuple[bool, str, list]
# There are 2 nullary operations: Always true , Never true, unary falsum
Nullary = "Nullary"
# There are 2 unary operations: Unary identity , Unary negation
Unary = 'Unary'
# There are 16 possible truth functions of two binary variables, each operator has its own name.
Binary = 'Binary'
# x*y == y*x : proprieta binaria
Commutative = "Commutative"
# (x*y)*z == x*(y*z) : proprieta binaria
Associative = 'Associative'
# Sentece is 'today is sunday' e una informazione
Sentence = ''
# Model is possible world PW := {P=True,Q=False}
Model = ''
# Knowledge-base is a set of sentencs kwnow by knowledge-based agent
knowledge = 'Knowledge'

def swap_constant_to_variable(datawork,database):
    out = datawork.copy()
    for key in datawork:
        name = datawork[key]
        if type(name) == type(''):
            if name in database and name.startswith('@'):
                #print("???->",args[name],args,name)
                out[key] = database[datawork[key]]
    return out
'''
||| 
|||
'''
class DATUM:
    def __init__(self, identity, value=None, transformer=None, *args):
        self.identity = identity
        self.identifier = None
        self.value = value
        self.args = args
        self.transformer = transformer

    def __call__(self, worker, variables):
        transformed = {}
        if self.transformer:
            if self.value in variables:
                value = Metadata('string', variables[self.value], 'test', 1, None)
                transformed_data = self.transformer(worker, value, *self.args)
                if isinstance(transformed_data, Metadata):
                    transformed[self.identifier] = transformed_data.value
                else:
                    transformed[self.identifier] = transformed_data
                if self.identity and not self.identity(worker, transformed[self.identifier])[0]:
                    #worker.app.logger.error(f"Not passed Identity: {self.identity}:{transformed[self.identifier]}:{variables[self.value]}")
                    transformed[self.identifier] = None
            else:
                worker.app.logger.error(f"{self.value} is not in {variables}")
        else:
            worker.app.logger.error("No action assigned")
        return variables | transformed
'''
||| Logic
||| - Un'espressione può essere costituita da constanti, variabili, expressioni, operatori e parentesi
'''
class EXPRESSION:
    '''
    ||| Inizializzazione: __init__
    ||| identifier: L'identificatore dell'espressione.
    ||| expression: L'espressione logica da valutare.
    ||| variables: Un dizionario che associa variabili ai loro valori.
    '''
    def __init__(self, identifier, expression, **variables):
        self.identifier = identifier
        self.expression = expression
        self.symbol = ':='
        self.variables = variables
    '''
    ||| Metodo: __str__
    ||| - Restituisce una stringa che rappresenta la formula logica.
    ||| - Se ci sono variabili, le elenca insieme alla formula.
    ||| - Altrimenti, restituisce solo la formula.
    '''
    # Returns string formula representing logical sentence.
    def __str__(self):
        # Q := A,B: (A==1) AND (B==A)
        if len(self.variables) == 0: var = None
        else: var = ",".join(self.variables)

        if var != None:
            return f"{self.identifier} {self.symbol} {var} : {str(self.expression)}"
        else:
            return f"{self.identifier} {self.symbol} {str(self.expression)}"    
    '''
    ||| Metodo: __call__
    ||| - Valuta l'espressione logica.
    ||| - Aggiorna le variabili con i loro valori.
    ||| - Applica eventuali trasformazioni alle variabili.
    ||| - Restituisce il risultato dell'espressione.
    '''
    def __call__(self, worker,unary=None,**variables)-> OUTPUT:
        #knowledge = dict()
        data = dict()
        data[TARGET] = unary
        data.update(variables)

        '''if isinstance(variables, dict):
            for key in variables:
                data['@'+key] = variables[key]
        else:
            data[TARGET] = unary'''

        for key in self.variables:
            datum = self.variables[key]
            datum.identifier = '@' + key
            data.update(datum(worker, data))
        #print(self.identifier,data)
        return self.expression(worker, data)

'''
||| AND: Logical conjunction ∧
||| commutative, associative
||| insieme = intersezione,
### In teoria dei reticoli, la congiunzione logica rappresenta il minimo comune multiplo.
||| false -> 1,1,data
||| true -> 1,N,data
'''
class AND:
    def __init__(self, *conjuncts):
        self.identifier = 'AND'
        self.conjuncts = conjuncts
        self.symbol = '∧'
        self.operation = Binary

    def __repr__(self):
        expressions = []
        for item in self.conjuncts:
            if isinstance(item, EXPRESSION):
                exp = '(' + str(item).split(':=')[1] + ')'
            else:
                exp = '(' + str(item) + ')'
            expressions.append(exp)
        return f' {self.symbol} '.join(expressions)

    def __call__(self, worker, variables) -> OUTPUT:
        tree = []
        branch = []
        for index, item in enumerate(self.conjuncts):
            boolean, identifier, stated = item(worker, variables)
            if not boolean:
                branch.append(stated)     
                tree.append((identifier,boolean))
                return OUTPUT((False, tuple((AND,tuple(tree))), tuple(branch)))
            else:
                branch.append(stated)     
                tree.append((identifier,boolean))
        
        return OUTPUT((True, tuple((AND,tuple(tree))), tuple(branch)))
'''
||| OR
'''
class OR:
    def __init__(self, *disjuncts):
        self.identifier = 'OR'
        self.disjuncts = disjuncts
        self.symbol = '∨'

    def __repr__(self):
        #disjunct_strings = [f"({str(d)})" for d in self.disjuncts]
        #return " ∨ ".join(disjunct_strings)
        expressions = []
        for item in self.disjuncts:
            if isinstance(item, EXPRESSION):
                exp = '(' + str(item).split(':=')[1] + ')'
            else:
                exp = '(' + str(item) + ')'
            expressions.append(exp)
        return f' {self.symbol} '.join(expressions)

    def __call__(self, worker, variables):
        #tuple([d.identifier for d in self.disjuncts])
        branch_faithless = []
        tre = []
        for index,item in enumerate(self.disjuncts):
            if isinstance(item, EXPRESSION):
                boolean, identifier, stated = item(worker, variables[TARGET],**variables)
            else:
                boolean, identifier, stated = item(worker, variables)
            if boolean: 
                branch_faithless.append(stated)     
                tre.append((identifier,boolean))
                #return OUTPUT((True, (stated[0],boolean,stated[2]), stated))
                return OUTPUT((True, tuple((OR,tuple(tre))), tuple(branch_faithless)))
            else:
                #faithless_states.setdefault(item.identifier, []).append(stated)
                branch_faithless.append(stated)     
                tre.append((identifier,boolean))
        
        return OUTPUT((False, tuple((OR,tuple(tre))), tuple(branch_faithless)))
'''
||| NOT
'''
class NOT:
    def __init__(self,operand):
        self.identifier = 'NOT'
        self.operand = operand
        self.symbol = '¬'
    def __call__(self,worker,args) -> OUTPUT:
        boolean,identifier,stated = self.operand(worker,args)
        return (not boolean,NOT,stated)
    def __repr__(self):
        return f"{self.symbol}({str(self.operand)})"
    
'''
||| IMPLICATION
'''
class IMPLICATION:
    def __init__(self,*args):
        self.identifier = 'IMPLICATION'
        self.items = args
        self.necessity = set({})
        self.symbol = '→'

'''
||| Consequence/Entailment
'''
class CONSEQUENCE:
    def __init__(self,*args):
        self.identifier = 'Consequence'
        self.items = args
        self.necessity = set({})
        self.symbol = '⊨'

'''
||| BICONDITIONAL
'''
class BICONDITIONAL:
    def __init__(self,*args):
        self.identifier = 'BICONDITIONAL'
        self.items = args
        self.necessity = set({})
        self.symbol = '↔'
'''
||| ALL
'''
class ALL:
    def __init__(self,set,*args):
        self.identifier = 'ALL'
        self.set = set
        self.items = args
        self.symbol = '∀'
    def __repr__(self):
        return f"per ogni {self.set} {self.items[0]}"
    def __call__(self, worker, variables) -> OUTPUT:
        liv_0 = []
        liv_1 = []

        tree = []

        if isinstance(self.set,dict):
            data = self.set
        else:
            data = swap_constant_to_variable({'set':self.set},variables)

        
        for x in data['set']:
            #print(data,x)
            for con in self.items:
                inn = variables
                inn['@x'] = x
                inn[TARGET] = x
                #print(con,self.items)
                #print(inn)
                if isinstance(con, EXPRESSION):
                    boolean, identifier, stated = con(worker, inn[TARGET],**inn)
                else:
                    boolean, identifier, stated = con(worker, inn[TARGET],**inn)
                if boolean:
                    tree.append((inn[TARGET],identifier,stated))
                else:
                    tree.append((inn[TARGET],identifier,stated))
                    pass
                liv_1.append(boolean)
            
            #faithless_identifiers.append(con.identifier)
            liv_0.append(any(liv_1))
            liv_1.clear()
        
        out_boolean = all(liv_0)
        if out_boolean:
            return OUTPUT((out_boolean,ALL,tuple(tree)))
        else:
            return OUTPUT((out_boolean,ALL,tuple(tree)))
        
class ATTRIBUTE:
    def __init__(self, targets,attributes):
        self.identifier = ATTRIBUTE.__name__
        self.targets = targets
        self.attributes = attributes
    def __str__(self):
        return 'str(self.ll).replace(TARGET,f"{self.count} in {self.target}")'
    def __call__(self, worker, variables):
        data = dict(variables)
        tor = []
        #for target in self.targets:
        if data[TARGET] != None:
            for target in data[TARGET]:
                for attribute in self.attributes:
                    tor.append(hasattr(target, attribute))
        else:
            return OUTPUT((False,self.identifier,data))
        

        return OUTPUT((all(tor),self.identifier,data))
    
class TYPE:
    def __init__(self, targets, types):
        self.identifier = TYPE.__name__
        self.targets = targets
        self.types = types
    def __str__(self):
        return 'str(self.ll).replace(TARGET,f"{self.count} in {self.target}")'
    def __call__(self, worker, variables):
        data = dict(variables)
        tor = []
        #for target in self.targets:
        if data[TARGET] != None:
            '''for target in data[TARGET]:
                for attribute in self.types:
                    if type(target) == type(attribute):
                        tor.append(True)
                    else:tor.append(False)'''
            for attribute in self.types:
                if type(data[TARGET]):
                    tor.append(True)
                else:tor.append(False)
        else:
            #print("FFF",target)
            OUTPUT((False,self.identifier,data))
        
        return OUTPUT((all(tor),self.identifier,data))
'''
||| SEQUENTIAL
'''
class SEQUENTIAL:
    def __init__(self, expression, target, compare):
        self.identifier = SEQUENTIAL.__name__
        #self.necessity = self.start([target,compare])
        self.target = target
        self.targets = compare
        self.expression = expression
        self.exem = expression(target,compare)

    def __repr__(self):
        return str(self.exem).replace(str(self.targets),f"$next in {self.targets}")
    
    def __call__(self, worker, variables):
        # Data job
        data = dict({'target':self.target,'check':self.targets})
        # Trasform data
        self.Varname(data,variables)
        # Do job
        for idx, target in enumerate(data['target']):
            expression = self.expression(str(type(target)),data['check'][idx])
            boolean,identifier,stated = expression(worker,data)
            if not boolean:return OUTPUT((False,self.identifier,stated))

        return OUTPUT((True,self.identifier,data))
'''
||| EQL:Logical equality
'''
class EQL:
    def __init__(self, left, right):
        self.identifier = EQL.__name__
        self.symbol = '=='
        self.operation = Binary
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.left} {self.symbol} {self.right}"
    
    def __call__(self, worker, variables):
        data = dict({'left':self.left,'right':self.right})
        data = swap_constant_to_variable(data,variables)
        boolean = data['left'] == data['right']
        tree_a = []

        f = (data['left'],self.symbol,data['right'])

        return OUTPUT((boolean,EQL,f))
'''
||| EQL_LESS
'''
class EQL_LESS:
    def __init__(self, left, right):
        self.identifier = EQL_LESS.__name__
        self.symbol = '<='
        self.operation = Binary
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.left} {self.symbol} {self.right}"
    
    def __call__(self, worker, variables):
        data = dict({'left':self.left,'right':self.right})
        data = swap_constant_to_variable(data,variables)
        boolean = data['left'] <= data['right']
        return OUTPUT((boolean,EQL_LESS,data))
'''
||| EQL_GREATER
'''
class EQL_GREATER:
    def __init__(self, left, right):
        self.identifier = EQL_GREATER.__name__
        self.symbol = '>='
        self.operation = Binary
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.left} {self.symbol} {self.right}"
    
    def __call__(self, worker, variables):
        data = dict({'left':self.left,'right':self.right})
        data = swap_constant_to_variable(data,variables)
        boolean = data['left'] >= data['right']
        return OUTPUT((boolean,EQL_GREATER,data))
'''
||| EQL_NOT
'''
class EQL_NOT:
    def __init__(self, left, right):
        self.identifier = EQL_NOT.__name__
        self.symbol = '≠'
        self.operation = Binary
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.left} {self.symbol} {self.right}"
    
    def __call__(self, worker, variables):
        data = dict({'left':self.left,'right':self.right})
        data = swap_constant_to_variable(data,variables)
        boolean = data['left'] != data['right']
        return OUTPUT((boolean,EQL_NOT,data))
'''
||| Count
'''
class COUNT:
    def __init__(self, target,count,counted,binary=EQL):
        self.identifier = COUNT.__name__
        
        self.target = target
        self.count = count
        self.counted = counted
        
        self.binary = binary
        self.ll = binary(TARGET,counted)
        self.symbol = 'Ʃ'
    
    def __str__(self):
        return str(self.ll).replace(TARGET,f"{self.count} in {self.target}")

    def __call__(self,worker, variables):
        data = dict({'target':self.target,'count':self.count,'counted':self.counted})
        data = swap_constant_to_variable(data,variables)
        
        

        if data['count'] == None:
            #print(len(data['target']),data['target'])
            targ = len(data['target'])
        else:
            if data['target'] == None:
                targ = 0
            else:
                targ = data['target'].count(data['count'])
        #print(targ,data,variables)
        expression = self.binary(targ,data['counted'])
        boolean,identifier,stated = expression(worker,None)

        #tree = (data['count'],'==',(data['target'],'#',data['count']))
        tree = ((data['target'],targ,data['count']),stated[1],stated[2])
        #tree = (data['count'],COUNT,data['target'])

        if boolean: return OUTPUT((True,(COUNT,True),stated))
        else: return OUTPUT((False,(COUNT,False),stated))
'''
||| INCLUSION
'''
class INCLUSION:
    def __init__(self,left_set,right_set):
        self.identifier = 'INCLUSION'
        self.right = right_set
        self.left = left_set
        self.symbol = '⊆'
        self.symbolNot = '⊈'
        self.symbol2Not = '⊄'
        self.symbol2 = '⊂'
    def __repr__(self):
        return f"{self.left} {self.symbol} {self.right}"
    def __call__(self, worker, variables):
        data = dict({'left':self.left,'right':self.right})
        data = swap_constant_to_variable(data,variables)
        output = (data['left'],self.symbol,data['right'])
        branch = []
        if isinstance(data['left'],type(None)):
            return OUTPUT((False, tuple((INCLUSION,False)), tuple(output)))
            #return OUTPUT((False,INCLUSION,data))
        for x in data['left']:
            result = any(item == x for item in data['right'])
            if not result:
                #print(x)
                #branch.append(stated)     
                #tre.append((identifier,boolean))
                #return OUTPUT((False, tuple((INCLUSION,False)), tuple(output)))
                return OUTPUT((False, tuple((INCLUSION,False)), tuple(output)))
        
        return OUTPUT((True, tuple((INCLUSION,True)), tuple(output)))
'''
|||EXISTS
'''
class EXISTS:
    def __init__(self,element,set):
        self.identifier = 'EXISTS'
        self.element = element
        self.set = set
        self.symbol = '∃'
        self.symbolNot = '∉'
    def __repr__(self):
        return f"{self.element} {self.symbol} {self.set}"
    def __call__(self, worker, variables):
        constants = dict({'element':self.element,'set':self.set})
        data = swap_constant_to_variable(constants,variables)
        
        if 'element' not in data:
            return OUTPUT((False, tuple((INCLUSION,False)), tuple(None,self.symbol,data['set'])))
        #print(data,variables)
        output = (data['element'],self.symbol,data['set'])
        for x in data['set']:
            if x == data['element']:return OUTPUT((True, tuple((MEMBERSHIP,True)), tuple(output)))
        #return OUTPUT((False,MEMBERSHIP,data))
        
        return OUTPUT((False, tuple((MEMBERSHIP,False)), tuple(output)))

'''
||| Membership
'''
class MEMBERSHIP:
    def __init__(self,element,set):
        self.identifier = 'MEMBERSHIP'
        self.element = element
        self.set = set
        self.symbol = '∈'
        self.symbolNot = '∉'
    def __repr__(self):
        return f"{self.element} {self.symbol} {self.set}"
    def __call__(self, worker, variables):
        constants = dict({'element':self.element,'set':self.set})
        data = swap_constant_to_variable(constants,variables)
        print(data)
        if 'element' not in data:
            return OUTPUT((False, tuple((INCLUSION,False)), tuple(None,self.symbol,data['set'])))
        #print(data,variables)
        output = (data['element'],self.symbol,data['set'])
        for x in data['set']:
            if x == data['element']:return OUTPUT((True, tuple((MEMBERSHIP,True)), tuple(output)))
        #return OUTPUT((False,MEMBERSHIP,data))
        
        return OUTPUT((False, tuple((MEMBERSHIP,False)), tuple(output)))
'''
||| ERROR
'''
def FAILED(data,failures,expression):
    splited = []
    tot = 0
    msg = str(expression)
    orr = SPLIT(None,VARIABLE(None,'STRING','FAILED::S',msg.split(':=')[1]),'∨','(',')')
    oand = SPLIT(None,VARIABLE(None,'STRING','FAILED::S',msg.split(':=')[1]),'∧','(',')')
    if len(orr) != 1:
        for x in orr:
            splited.append("".join(x))
    elif len(oand) != 1:
        for x in oand:
            splited.append("".join(x))
    #print(orr,oand,splited,'===>',failures,data)
    if hasattr(failures,'__len__'):
        for failure in failures:
            if failure in data:
                for idx,x in enumerate(data[failures]):
                    sub = splited[tot]
                    msg = msg.replace(sub,"\033[91m ("+STRING(failures,x)+') \033[0m')
                    '''if idx == len(splited) -1:
                        msg = msg.replace(sub,"\033[91m ("+STRING(failures,x)+') \033[0m')
                    else:
                        msg = msg.replace(sub," \033[92m ("+STRING(failures,x)+') \033[0m')'''
    else:
        print("=======>",failures,data)
        if failures in data:
            for idx,x in enumerate(data[failures]):
                for y in x:
                    sub = splited[y]
                    print("=======>",sub)
                
                    msg = msg.replace(sub,"\033[91m ("+STRING(failures,x[y])+') \033[0m')
                    #msg = msg.replace(sub," \033[92m ("+STRING(failures,x)+') \033[0m')

    return msg
'''
||| STRING
'''
def STRING(typ,data):
    #print(data,typ,'==',str(ALL))
    
    if str(typ) == "<class 'logic.EQL'>":
        return f"{data['left']} == {data['right']}"
    elif str(typ) == "<class 'logic.ALL'>":
        return f"per ogni x "
    elif str(typ) == "<class 'logic.INCLUSION'>":
        return f"{data['left']} ⊆ {data['right']}"
    elif str(typ) == "<class 'logic.MEMBERSHIP'>":
        return f"{data['element']} ∈ {data['set']}"
    else:
        return "NOT_IMPL"
            