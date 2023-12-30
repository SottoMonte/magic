from LOGIC import EXPRESSION,OR,AND,TARGET,TRANSFORM,TRANSFORMED,EQL,EACH
import LOGIC
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
#                               GRAMMAR
# --------------------------------------------------------------------------------------

# KEYWORD
KEYWORD_SET = { "SET","TUPLE","LIST","DICT","NATURAL","INTEGER","RATIONAL","REAL","COMPLEX","STRING","BOOL","BYTE","SECURE","TRUE","FALSE","OR","AND" }

# ALPHABET
LOWER = { "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z" }
UPPER = { "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z" } 
LETTER_SET = LOWER.union(UPPER)

# NUMERI
DIGIT = {"0","1","2","3","4","5","6","7","8","9"}

# LEXICAL

# SYNTAX
CLOSURE = { "\"","(",")","<",">","[","]","{","}" }
SEPARATOR_SET = { ",","|","::",":",";"," ","\n","" }
OTHER = { ".","...","?"}

SYMBOL = { }

ARITHMETIC = { "+","-","*","/","%","++","--" }
ASSIGNMENT = { "=",":=","+=","-=","*=","/=","%=","^=" }
COMPARISON = { "==","!=",">","<",">=","<=" }
LOGICAL = { "&&","||","!" }

OPERATOR_SET = LOGICAL.union(ASSIGNMENT,ARITHMETIC,COMPARISON)


# --------------------------------------------------------------------------------------
#                                ANALIZZATORE
# --------------------------------------------------------------------------------------
# INTERNI
OPERATOR = EXPRESSION('OPERATOR',EACH(EQL,TARGET,OPERATOR_SET))
KEYWORD = EXPRESSION('KEYWORD',EACH(EQL,TARGET,KEYWORD_SET))

SEPARATOR = EXPRESSION('SEPARATOR',EACH(EQL,TARGET,SEPARATOR_SET))
CLOSE = EXPRESSION('CLOSE',EACH(EQL,TARGET,CLOSURE))
LETTER = EXPRESSION('LETTER',EACH(EQL,TARGET,LETTER_SET))

IDENTIFIER = EXPRESSION('IDENTIFIER',OR(
    EACH(EQL,TARGET,LETTER_SET),
),TRANSFORM=TRANSFORM(SPLIT,TARGET,'::'))

BOOLEAN = EXPRESSION('BOOLEAN',EACH(EQL,TARGET,['FALSE','TRUE']))

# NUMERI

BINARY = EXPRESSION('BINARY',EACH(EQL,TARGET,['0','1']))
NATURAL = EXPRESSION('NATURAL',OR(EACH(EQL,[TARGET],['TRUE','FALSE'])))
INTEGER = EXPRESSION('INTEGER',OR(EACH(EQL,[TARGET],['TRUE','FALSE'])))
NUMBER = EXPRESSION('NUMBER',OR(LETTER,TRANSFORMED),TRANSFORM=TRANSFORM(SPLIT,TARGET,'::'),TRANSFORM2=TRANSFORM(EACH,EQL,TARGET,'::'))

# --------------------------------------------------------------------------------------
#                                SYNTAX
# --------------------------------------------------------------------------------------





# --------------------------------------------------------------------------------------
#                                TEST
# --------------------------------------------------------------------------------------

TEST = LOGIC.TEST(
    (OPERATOR,True,"=="),
    (IDENTIFIER,True,'NOMEVARIABILE'),
    (IDENTIFIER,False,'@NOMEVARASD12IABILE'),
    (IDENTIFIER,True,'NOMEVARIABILE::ALTRO'),
    (IDENTIFIER,True,'NOMEVARIABILE::ALTRO::ALTRO'),
    (IDENTIFIER,False,'::NOMEVARIABILE::ALTRO'),
    (IDENTIFIER,False,'NOMEVARIABILE::ALTRO::'),
    (BOOLEAN,True,'TRUE'),
    (BOOLEAN,True,'FALSE'),
    
)