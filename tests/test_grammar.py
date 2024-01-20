import sys
sys.path.append('src/sloth/core/')
sys.path.append('src/analyzer/')
import grammar
import worker
import application
import asyncio



async def TestGrammar(worker:worker):
    check = grammar.INSTRUCTION_CALL(worker,['varname','(','1',')'])
    print(check)
    #['STRING',':','varname',':=','(','1',')']
    check2 = grammar.INSTRUCTION_ALLOCATION(worker,['STRING',':','varname',':=','(','1',')'])
    print("--->",check2)
    pass

if __name__ == "__main__":
    app = application.mathmagic("example.cli",sys.argv,{application.INTERFACE.CLI:application.CLI})
    app.JOB(TestGrammar)
    app.RUN()


# --------------------------------------------------------------------------------------
#                                TEST
# --------------------------------------------------------------------------------------

'''TEST = LOGIC.TEST(
    (OPERATOR,True,"=="),
    (IDENTIFIER,True,'NOMEVARIABILE'),
    (IDENTIFIER,False,'@NOMEVARASD12IABILE'),
    (IDENTIFIER,True,'NOMEVARIABILE::ALTRO'),
    (IDENTIFIER,True,'NOMEVARIABILE::ALTRO::ALTRO'),
    (IDENTIFIER,False,'::NOMEVARIABILE::ALTRO'),
    (IDENTIFIER,False,'NOMEVARIABILE::ALTRO::'),
    (BOOLEAN,True,'TRUE'),
    (BOOLEAN,True,'FALSE'),
    
)'''