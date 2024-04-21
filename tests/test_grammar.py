import sys
sys.path.append('src/core/')
sys.path.append('src/analyzer/')
import logic
import grammar
import data
import worker as WORKER
import application
import asyncio

# --------------------------------------------------------------------------------------
#                                TEST
# --------------------------------------------------------------------------------------

'''
TEST = (
    (False,grammar.TUPLE,[]),
    (False,grammar.TUPLE,['intero', '100']),
    (True,grammar.TUPLE,['(',')']),
    (True,grammar.TUPLE,['(','100',')']),
    (False,grammar.TUPLE,['(','100',',',')']),
    (True,grammar.TUPLE,['(','100',',','200',',','300',')']),
    (False,grammar.TUPLE,['(', 'x', 'a', 'y', ')']),
    (False,grammar.TUPLE,['(','100',';','200',';','300',')']),
    (True,grammar.LIST,['[','100',',','200',']']),
    (True,grammar.VECTOR,['[','100',']']),
    (True,grammar.MATRIX,['[','100',']']),
    (True,grammar.DICTIONARY,['{','intero',':','100','}']),
    (True,grammar.DICTIONARY,['{','aaa',':','100',';','bbb',':','100','}']),
    (False,grammar.DICTIONARY,['{','aaa',':','100','bbb','100','}']),
    (False,grammar.DICTIONARY,['{','intero','100','}']),
    (False,grammar.DICTIONARY,['{','intero',';','100','}']),
    (True,grammar.NUMBER,'1234567890'),
    (True,grammar.NUMBER,'0101101110'),
    (True,grammar.IDENTIFIER,'varname'),
    (True,grammar.IDENTIFIER,'Varname'),
    (False,grammar.IDENTIFIER,'1Varname'),
    (False,grammar.IDENTIFIER,''),
    #(False,grammar.STRING,None),
    (True,grammar.STRING,'"Questa è una Stringa"'),
    (False,grammar.STRING,'"Questa è una Stringa'),
    (False,grammar.STRING,'Questa è una Stringa"'),
    (True,grammar.INSTRUCTION_CALL,['varname','(','1',')']),
    (False,grammar.INSTRUCTION_CALL,['varname','(','1']),
    (False,grammar.INSTRUCTION_CALL,['varname','(']),
    (False,grammar.INSTRUCTION_CALL,['varname','1']),
    (False,grammar.INSTRUCTION_CALL,['varname']),
    (True,grammar.PAIR,['STRING',':','varname2']),
    (False,grammar.PAIR,['STRING',':=','varname2']),
    (False,grammar.PAIR,['',':','a']),
    (False,grammar.INSTRUCTION_ALLOCATION,['STRING',':','varname',':=']),
    (False,grammar.INSTRUCTION_ALLOCATION,['STRING',':','varname',':=','(','1']),
    (True,grammar.INSTRUCTION_ALLOCATION,['STRING',':','varname',':=','(','1',',','2',',','3',')']),
    (True,grammar.INSTRUCTION_ALLOCATION,['STRING',':','varname',':=','(','1',')']),
    (True,grammar.INSTRUCTION_ALLOCATION,['STRING',':','varname',':=','TRUE']),
    (True,grammar.INSTRUCTION_ALLOCATION,['STRING',':','varname',':=','"Stringa"']),
    (True,grammar.INSTRUCTION_ALLOCATION,['STRING',':','varname',':=','1234567890']),
    (False,grammar.INSTRUCTION_ASSIGNMENT,None),
    (False,grammar.INSTRUCTION_ASSIGNMENT,['varname','=']),
    (True,grammar.INSTRUCTION_ASSIGNMENT,['varname','=','1234567890']),
    (True,grammar.SET,['{','var996',';','1234567890','}']),
    (True,grammar.SET,['{','1000',';','1234567890','}']),
    (True,grammar.SET,['{','}']),
    (False,grammar.SET,['1000','1234567890','}']),
    (False,grammar.SET,['{','1000','1234567890']),
    (True,grammar.LIST,['[','1000',',','"1234567890"',']']),
    (True,grammar.VECTOR,['[','1000',',','1234567890',']']),
    (True,grammar.MATRIX,['[','[','1000',']',',','[','1234567890',']',']']),
    #(True,grammar.MATRIX,['[','[','1000',',','1234567890',']',']']),
    (True,grammar.DICTIONARY,['{','STRING',':','nome','}']),
    #(False,grammar.DICTIONARY,['{','POINT',':','(','x','a','y',')','}']),
    #(True,grammar.DICTIONARY,['{','POINT',':','(','x',',','a',',','y',')',';','"A"',':','100','}']),
    #(True,grammar.DICTIONARY,['{','"A"',':','100',';','"B"',':','200','}']),
    #(False,grammar.DICTIONARY,['{','STRING','nome','}']),
    #(False,grammar.EXPRESSION_ARITHMETIC,[]),
)'''

UNIT = (
    (False,grammar.IDENTIFIER,""),
    (False,grammar.IDENTIFIER,"1Abc"),
    (False,grammar.IDENTIFIER,"_nome"),
    (True,grammar.IDENTIFIER,"Cliente"),
    (True,grammar.IDENTIFIER,"cliente"),
    (True,grammar.KEYWORD,'INTEGER'),
    (True,grammar.KEYWORD,'STRING'),
    (False,grammar.INTEGER,'-'),
    (False,grammar.INTEGER,'+'),
    (False,grammar.INTEGER,'--100'),
    (False,grammar.INTEGER,'++100'),
    (False,grammar.INTEGER,'100-'),
    (True,grammar.INTEGER,'100'),
    (True,grammar.INTEGER,'-100'),
    (True,grammar.INTEGER,'+100'),
    (True,grammar.RATIONAL,'+100'),
    (True,grammar.RATIONAL,'+100.99'),
    (False,grammar.RATIONAL,'+100.99.9'),
    (True,grammar.NUMBER,'+100.99'),
    (True,grammar.REAL,'π'),
)

async def TestGrammar(worker:WORKER.WORKER):    
    WORKER.TEST(worker,UNIT)

if __name__ == "__main__":
    app = application.mathemagic("test.grammar",sys.argv,{})
    app.JOB(TestGrammar)
    app.RUN()