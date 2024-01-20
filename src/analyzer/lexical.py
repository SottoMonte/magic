import sys
sys.path.append('src/core/')
import grammar
import logic
import worker

'''
||| Input(STRING) | Output(TOKENS)
'''
async def LEXER(WORKER:worker.WORKER):
    '''
    ||| Funzione che crea flusso di tokens
    '''
    # keword,opreatori,identificatori,numeri
    #check_token = logic.expression('check_token',logic.OR(grammar.BINARY,grammar.SEPARATOR,grammar.KEYWORD,grammar.OPERATOR,grammar.CLOSE,grammar.LETTER))
    TOKEN = logic.EXPRESSION('TOKEN',logic.OR(grammar.STRING,grammar.SPECIAL,grammar.KEYWORD,grammar.OPERATOR,grammar.SEPARATOR,grammar.CLOSE,grammar.IDENTIFIER,grammar.LETTER,grammar.NUMBER))
    CTOKEN = logic.EXPRESSION('CTOKEN',logic.OR(grammar.STRING_2,grammar.IDENTIFIER,grammar.LETTER,grammar.NUMBER))
    
    '''async def TOKENIZER(self,end):
        
        presente_long = CTOKEN(WORKER,self[:end])
        presente_string = TOKEN(WORKER,[self[:end]])
        
        if presente_long[0] or presente_string[0]:
            #print('[TOKEN]',presente_long,presente_string,self[:end])
            #for idx, x in enumerate(self):
            a = await TOKENIZER(self,end+1)
            #print("====@@@@>",a)
            print('[LONG]',a,self[:end])
            if a[0] != None:
                #print('[EX]',self[:end])
                return a
            else:
                #print("[FA]",self[:end])
                return (a[0],a[1])
        else:
            #print('[!TOKEN]',presente_long,presente_string,self[:end-1])
            print(len(self[:end]))
            presente_long_2 = CTOKEN(WORKER,self[:end-1])
            presente_string_2 = TOKEN(WORKER,[self[:end-1]])

            if type(presente_string_2[1]) == type(''):
                return (presente_string_2[1],end-1)
            elif type(presente_long_2[1]) == type(''):
                return (presente_long_2[1],end-1)
            else:
                return(None,end-1)'''
    # Lexer
    async def TOKENIZER(self,n):
        TOKENIZER.token += self 
        presente_long = CTOKEN(WORKER,TOKENIZER.token)
        futuro_char = CTOKEN(WORKER,TOKENIZER.token+n)
        futuro_string = TOKEN(WORKER,[TOKENIZER.token+n])
        presente_string = TOKEN(WORKER,[TOKENIZER.token])

        if presente_long[0] and (futuro_string[0] == False and  futuro_char[0] == False and presente_string[0] == False ):
            #print(TOKENIZER.token)
            #print(f"---------->{TOKENIZER.token}\n\n{futuro_string_2}\n\n{presente_long}\n\n{futuro_char}\n\n{futuro_string}\n\n{presente_string}")
            await WORKER.SPEAK('PARSER',(presente_long[1],TOKENIZER.token))
            TOKENIZER.token = ""
        elif futuro_string[0] == False and presente_string[0] == False and presente_long[0] == False :
            #print(f"---------->{TOKENIZER.token}\n\n{futuro_string_2}\n\n{presente_long}\n\n{futuro_char}\n\n{futuro_string}\n\n{presente_string}")
            presente_string = TOKEN(WORKER,[TOKENIZER.token[:-1]])
            #print("---------->",TOKENIZER.token,presente_string)
            await WORKER.SPEAK('PARSER',(presente_string[1],TOKENIZER.token[:-1]))
            TOKENIZER.token = TOKENIZER.token[-1]
            
            #presente_string = TOKEN(WORKER,[TOKENIZER.token[:-1]])
            #await WORKER.SPEAK('PARSER',(presente_string[1],TOKENIZER.token[:-1]))
            
        else:
            
            pass
        
        
    TOKENIZER.token = ""
    '''
    ||| Legge la sorgente e applica la funzione tokenizer
    '''
    await WORKER.READER('sorgente.mm',TOKENIZER,'char')
    '''
    ||| Invia segnale parser fine flusso
    '''
    await WORKER.SPEAK('PARSER',None)