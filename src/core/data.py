from dataclasses import dataclass,asdict,astuple
import dicttoxml
from logic import EXPRESSION,EQL,COUNT,ATTRIBUTE,TARGET,AND,TYPE,ALL,EQL_NOT
#import json
from enum import Enum

'''
# Declarative-programming
# Functional-programming
# LOGIC programming
# Constraint programming
# Constraint LOGIC programming
'''

'''
||| Un dato è caratterizzato da 3 proprietà fondamentali: tipo, cardinalità e valore.
'''

Events = Enum('Events', ['Modified', 'Created', 'Eliminated'])

    
Identity = EXPRESSION('Identity',EQL("1","1"))
Singleton = EXPRESSION('Identity',EQL("1","1"))
Data = EXPRESSION('Identity',EQL("1","1"))
Metadata = EXPRESSION('Identity',EQL("1","1"))
Recursion = EXPRESSION('Identity',EQL("1","1"))
PureFunction = EXPRESSION('Identity',EQL("1","1"))
Iterable = EXPRESSION('Iterable',EQL("1","1"))
Homogeneous = EXPRESSION('Homogeneous',EQL("1","1"))
Heterogeneous = EXPRESSION('Heterogeneous',EQL("1","1"))

Character = EXPRESSION('Character',AND(
    #ATTRIBUTE([TARGET],['__len__']),
    COUNT(TARGET,'',2)
))

String = EXPRESSION('String',AND(
    #LOGIC.ATTRIBUTE([LOGIC.TARGET],['__len__']),
    TYPE([TARGET],[""])
))

Iterable = EXPRESSION('Iterable',AND(
    ATTRIBUTE([TARGET],['__iter__']),
))

Empty = EXPRESSION('Empty',AND(
    ATTRIBUTE([TARGET],['__len__']),
    ALL(TARGET,[[],None])
))

Matter = EXPRESSION('Matter',AND(
    ALL(EQL_NOT,TARGET,[[],None])
))


@dataclass(frozen=True)
class Metadata:
    type: str
    value: str
    identifier: str  
    cardinality: int
    required:bool = None
    driver:str = None

def VARIABLE(worker,typee,identifier,value,required=None):
    if hasattr(value,'__iter__'):
        return Metadata(typee,value,identifier,len(value),required)
    elif value == None:
        return Metadata(typee,value,identifier,0,required)
    else:
        return Metadata(typee,value,identifier,1,required)
    
def CONSTANT(worker,typee,identifier,value,required=None):
    if hasattr(value,'__iter__'):
        return Metadata(typee,value,identifier,len(value),required)
    elif value == None:
        return Metadata(typee,value,identifier,0,required)
    else:
        return Metadata(typee,value,identifier,1,required)

def DATA(worker,typee,identifier,value,required=None):
    if hasattr(value,'__iter__'):
        return Metadata(typee,value,identifier,len(value),required)
    elif value == None:
        return Metadata(typee,value,identifier,0,required)
    else:
        return Metadata(typee,value,identifier,1,required)


def SET(worker,target,value):
    if hasattr(value,'__iter__'):
        return Metadata(target.typee,value,target.identifier,len(value),target.required)
    elif value == None:
        return Metadata(target.typee,value,target.identifier,0,target.required)
    else:
        return Metadata(target.typee,value,target.identifier,1,target.required)

def GET(worker,target):
    #return asdict(target)
    return target.value

def CAD(worker,target):
    return target.cardinality

def TYPE(worker,target):
    pass

def FIRST(worker,target):
    if hasattr(target.value,'__iter__'):
        if len(target.value) > 0:
            return target.value[0]
        else:
            return None
    else:
        return None

def LAST(worker,target):
    if hasattr(target.value,'__iter__'):
        if len(target.value) > 0:
            return target.value[-1]
        else:
            return None
    else:
        return None

def ELEMENT(worker,target,idx):
    #print(target)
    if hasattr(target.value,'__iter__'):
        if 0 <= idx < len(target.value):
            return target.value[idx] 
        elif - len(target.value) < idx <= -1:
            return target.value[idx]
        else:
            return None
    else:
        return None

def RANGE(worker,target,start,end=None):
    if hasattr(target.value,'__iter__'):
        if 0 <= start < len(target.value) and end != start:
            if end == None:
                return target.value[start:]
            else:
                return target.value[start:end]
        else:
            return []
    else:
        return None

def DIVISION(worker,target,SEPARATOR, LOCK=None, UNLOCK=None):
    new = []
    temp = []
        
    for x in target.value:
        if x == SEPARATOR:
            if len(temp) == 1:
                new.append(temp[0])
            else:
                new.append(temp.copy())
            temp.clear()
        else:
            temp.append(x)
    if len(temp) == 1:
        new.append(temp[0])
    else:
        new.append(temp.copy())
    return new

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

def UNION(worker,target,value):
    if hasattr(target.value,'__iter__'):
        return SET(worker,target,target.value + value)
    else:
        return SET(worker,target,target.value + value)

def DEL(worker,target,value):
    pass

def UNPACK(worker,target)->any:
        if hasattr(target.value,'__iter__'):
            if len(target.value) == 1:
                return target.value[0]
            else:return target.value
        else:
            return None
        
def PACK(worker,target)->any:
    return [target.value]

def NONE(worker,target):
    return target

def STRING(worker,target):
    return f"<{target.required}> {target.typee:<15.15}:{target.identifier:<25.25} := {target.cardinality}:{target.value}"

def XML(worker,target):
    return dicttoxml.dicttoxml(asdict(target), attr_type=False).decode()

def METADATA(*metadata):
    def decorator(function):
        async def wrapper(*args, **kwargs):
            print('ALL:',metadata)
            try:
                print('ARGS:',args)
                await function(*args)
            except Exception as e:
                print('Something went wrong.', e)
        return wrapper
    return decorator

def TUPLE(worker,string):
    stack = []
    risultato = []

    for char in string:
        if char == "(":
            stack.append(risultato)
            risultato = []
        elif char == ")":
            tupla_annidata = tuple(risultato)
            risultato = stack.pop()
            risultato.append(tupla_annidata)
        elif char == ",":
            risultato.append(int(char))

    return tuple(risultato)