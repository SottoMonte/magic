import sys
sys.path.append('src/core/')
import data
from logic import EXPRESSION,OR,AND,TARGET,EQL,EACH,COUNT,TRAN,EACH2
#import logic
#from DATA import ALPHA,SPLIT

import time

def SPLIT(TARGET:str, SEPARATOR, LOCK=None, UNLOCK=None):
    if LOCK is not None and UNLOCK is not None:
        result = []
        block = 0
        job = ""
        for CHAR in TARGET:
            job += CHAR
            if job.endswith(LOCK):
                block += 1
            elif job.endswith(UNLOCK):
                block -= 1
            elif job.endswith(SEPARATOR) and block == 0:
                result.append(job[:-len(SEPARATOR)].strip())
                job = ""
        if job != "":
            result.append(job.strip())
        return result
    else:
        return [stringa.strip() for stringa in TARGET.split(SEPARATOR)]

# --------------------------------------------------------------------------------------
#                               ALPHABET/DICTIONARY
# --------------------------------------------------------------------------------------

# KEYWORD
KEYWORD_SET = { "SET","TUPLE","LIST","DICT","NATURAL","INTEGER","RATIONAL","REAL","COMPLEX","STRING","BOOL",'BINARY',"BYTE","SECURE","TRUE","FALSE","OR","AND",'FUNCTION','ACTION','METHOD' }

# ALPHABET
LOWER = { "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z" }
UPPER = { "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z" } 
LETTER_SET = LOWER.union(UPPER)

# NUMERI
DIGIT = {"0","1","2","3","4","5","6","7","8","9"}

# LEXICAL

# SYNTAX
CLOSURE = { "\"","(",")","<",">","[","]","{","}","'", }
SEPARATOR_SET = { ",","|","::",":",";",'.','://',' ' }
SPECIAL_SET = {'\n','','\n\n','\\','_'}

SYMBOL = { }

ARITHMETIC = { "+","-","*","/","%","++","--" }
ASSIGNMENT = { "=",":=","+=","-=","*=","/=","%=","^=" }
COMPARISON = { "==","!=",">","<",">=","<=" }
LOGICAL = { "&&","||","!",'?' }

OPERATOR_SET = LOGICAL.union(ASSIGNMENT,ARITHMETIC,COMPARISON)


# --------------------------------------------------------------------------------------
#                                LEXICAL
# --------------------------------------------------------------------------------------
# INTERNI
OPERATOR = EXPRESSION('OPERATOR',EACH(EQL,TARGET,OPERATOR_SET))
KEYWORD = EXPRESSION('KEYWORD',EACH(EQL,TARGET,KEYWORD_SET))

SEPARATOR = EXPRESSION('SEPARATOR',EACH(EQL,TARGET,SEPARATOR_SET))
CLOSE = EXPRESSION('CLOSE',EACH(EQL,TARGET,CLOSURE))
LETTER = EXPRESSION('LETTER',EACH(EQL,TARGET,LETTER_SET))
SPECIAL = EXPRESSION('SPECIAL',EACH(EQL,TARGET,SPECIAL_SET))

#IDENTIFIER = EXPRESSION('IDENTIFIER',AND(EACH(EQL,TARGET,LETTER_SET|DIGIT),EACH(EQL,'id',LETTER_SET)),id=TRANSFORM(TARGET,'FIRST'))
IDENTIFIER = EXPRESSION('IDENTIFIER',AND(EACH(EQL,TARGET,LETTER_SET|DIGIT),EACH(EQL,'id',LETTER_SET)),id=data.variable(["<class 'str'>"],'id',TARGET,transform=data.variable.FIRST))

BOOLEAN = EXPRESSION('BOOLEAN',EACH(EQL,[TARGET],['FALSE','TRUE']))

# NUMERI
BINARY = EXPRESSION('BINARY',EACH(EQL,TARGET,['0','1']))
NATURAL = EXPRESSION('NATURAL',EACH(EQL,TARGET,DIGIT))
INTEGER = EXPRESSION('INTEGER',EACH(EQL,TARGET,DIGIT))
RATIONAL = EXPRESSION('BINARY',EACH(EQL,TARGET,['0','1']))
REAL = EXPRESSION('BINARY',EACH(EQL,TARGET,['0','1']))
COMPLEX = EXPRESSION('BINARY',EACH(EQL,TARGET,['0','1']))

NUMBER = EXPRESSION('NUMBER',OR(NATURAL,INTEGER,BINARY))

STRING = EXPRESSION('STRING',AND(EQL('cc','"'),EQL('bb','"'),COUNT(TARGET,'"',2)),
            cc=data.variable(["<class 'str'>"],'cc',TARGET,transform=data.variable.FIRST),
            bb=data.variable(["<class 'str'>"],'bb',TARGET,transform=data.variable.LAST))

STRING_2 = EXPRESSION('STRING_2',AND(EQL('cc','"'),COUNT(TARGET,'"',1)),cc=data.variable(["<class 'str'>"],'cc',TARGET,transform=data.variable.FIRST))
# --------------------------------------------------------------------------------------
#                                SYNTAX
# --------------------------------------------------------------------------------------
#BINARY = EXPRESSION('BINARY',EACH(EQL,TARGET,['0','1']))

EXPRESSION_LINGUISTIC = EXPRESSION('LINGUISTIC',EACH(EQL,TARGET,['0','1']))
EXPRESSION_LOGIC = EXPRESSION('LOGIC',EACH(EQL,TARGET,['0','1']))
EXPRESSION_ALGEBRA = EXPRESSION('ALGEBRA',EACH(EQL,TARGET,['0','1']))
EXPRESSION_ARITHMETIC = EXPRESSION('ARITHMETIC',EACH(EQL,TARGET,['0','1']))

RECORD = EXPRESSION('RECORD',EACH(EQL,TARGET,['0','1']))
# SET := '{' and '}' or ;
SET = EXPRESSION('SET',EACH(EQL,TARGET,['0','1']))
# PAIR := '(' ')' or :
PAIR = EXPRESSION('PAIR',AND(KEYWORD,EQL('_1',':'),IDENTIFIER,
                             _0=(TARGET,TARGET,data.variable.ELEMENT,(0,),True),
                             _1=(TARGET,'_1',data.variable.ELEMENT,(1,),False),
                             _2=(TARGET,TARGET,data.variable.ELEMENT,(2,),False),
                             ))
# TUPLE := '(' ')' or ,
#EACH(EQL,'_...',['(',')'])
# TUPLE = EXPRESSION('TUPLE',AND(EQL('_first','('),EACH2(NUMBER,'_1:-1'),EQL('_last',')')))
TUPLE = EXPRESSION('TUPLE',AND(EQL('_primo','('),EACH2(NUMBER,'_...'),EQL('_ultimo',')'),
                               _0=(TARGET,'_primo',data.variable.FIRST,(),False),
                               _1=(TARGET,'_...',data.variable.RANGE,(1,-1),False),
                               _2=(TARGET,'_ultimo',data.variable.LAST,(),False),
                               ))
                    
# LIST := '[' ']' or ,
LIST = EXPRESSION('LIST',EACH(EQL,TARGET,['0','1']))
# MATRIX := '[' ']' or ,
MATRIX = EXPRESSION('MATRIX',EACH(EQL,TARGET,['0','1']))
# VECTOR := '[' ']' or ,
VECTOR = EXPRESSION('VECTOR',EACH(EQL,TARGET,['0','1']))
# DICTIONARY := '{' ... PAIR ... '}' or ;
DICTIONARY = EXPRESSION('DICTIONARY',EACH(EQL,TARGET,['0','1']))
# OBJECT := []KEYWORD:IDENTIFIER
OBJECT = EXPRESSION('OBJECT',EACH(EQL,TARGET,['0','1']))
# TREE := 2 | 2 / 1 | 2 -> 0  1 / 1:0 | 1 -> 0
TREE = EXPRESSION('TREE',EACH(EQL,TARGET,['0','1']))
# GRAPH := A:B,C,D|B:C|C:D|D:A
GRAPH = EXPRESSION('GRAPH',EACH(EQL,TARGET,['0','1']))
# STACK := <0-1-2-3-4-5-6-7-8-9>
STACK = EXPRESSION('STACK',EACH(EQL,TARGET,['0','1']))
# QUEUE := <9-8-7-6-5-4-3-2-1-0>
QUEUE = EXPRESSION('QUEUE',EACH(EQL,TARGET,['0','1']))
# ALL DATA
# NUMBER,STRING,BOOLEAN,IDENTIFIER,TUPLE
DATA = EXPRESSION('NUMBER',OR(NUMBER,STRING,BOOLEAN,IDENTIFIER,TUPLE))

#INSTRUCTION_CALL = EXPRESSION('CALL',AND(IDENTIFIER,'_0',TARGET),TRAN(TUPLE,'_1:',TARGET),_0=TARGET))
INSTRUCTION_CALL = EXPRESSION('CALL',AND(IDENTIFIER,TUPLE,_0=(TARGET,TARGET,data.variable.FIRST,(),False),_1=(TARGET,TARGET,data.variable.RANGE,(1,),False)))

#INSTRUCTION_ALLOCATION = EXPRESSION('ALLOCATION', AND(TRAN(PAIR,'_0:3',TARGET),EQL(':=',"_3"),TRAN(DATA,'_4:',TARGET)))
INSTRUCTION_ALLOCATION = EXPRESSION('ALLOCATION', AND(PAIR,EQL(':=','_3'),DATA,
                                                      _0=(TARGET,TARGET,data.variable.RANGE,(0,3,),False),
                                                      _1=(TARGET,'_3',data.variable.ELEMENT,(3,),False),
                                                      _2=(TARGET,TARGET,data.variable.RANGE,(4,),False),
                                                    ))

INSTRUCTION_DEALLOCATE = EXPRESSION('DEALLOCATE', AND(EQL('DEAL','_0'),TRAN(DATA,'_1',TARGET)))

INSTRUCTION_ASSIGNMENT = EXPRESSION('ASSIGNMENT', AND(TRAN(IDENTIFIER,'_0',TARGET),EQL('=',"_1"),TRAN(DATA,'_2',TARGET)))

INSTRUCTION_JOB = EXPRESSION('JOB',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_SYSTEM = EXPRESSION('SYSTEM',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_INPUT = EXPRESSION('INPUT',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_OUTPUT = EXPRESSION('OUTPUT',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_RETURN = EXPRESSION('RETURN',AND(EQL('RETURN',TARGET),TRAN(DATA,'_token1',TARGET)))
INSTRUCTION_WAIT = EXPRESSION('WAIT',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_NEXT = EXPRESSION('NEXT',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_LOCK = EXPRESSION('LOCK',EACH(EQL,TARGET,['0','1']))

INSTRUCTION_COMPARISON = EXPRESSION('JOB',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_CONVERSION = EXPRESSION('CONVERSION',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_CONCATENATION = EXPRESSION('CONCATENATION',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_ITERATION = EXPRESSION('ITERATION',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_INCREASE_DECREASE = EXPRESSION('JOB',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_SELECTION = EXPRESSION('SELECTION',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_LOGICAL = EXPRESSION('LOGICAL',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_ARITHMETIC = EXPRESSION('ARITHMETIC',EACH(EQL,TARGET,['0','1']))
INSTRUCTION_ALGEBRAIC = EXPRESSION('ALGEBRAIC',EACH(EQL,TARGET,['0','1']))