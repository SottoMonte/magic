import sys
sys.path.append('src/core/')
import grammar
import logic
import worker as WORKER
import asyncio

TOKEN = logic.EXPRESSION('TOKEN',logic.OR(
    grammar.CSTRING,grammar.STRING,
    grammar.SPECIAL,grammar.KEYWORD,
    grammar.OPERATOR,grammar.SEPARATOR,
    grammar.CLOSE,grammar.IDENTIFIER,
    grammar.LETTER,grammar.NUMBER))

'''
||| TOKENIZER: produttore di token
'''
async def TOKENIZER(worker,**constants):
    stringa_c = constants['output'] + constants['current']
    stringa_f = stringa_c + constants['next']
    index = constants['index']
    
    if 'onset' in constants:
        onset_token = constants['onset']
    else:
        onset_token = 1
    if 'endset' in constants:
        endset_token = constants['endset']
    else:
        endset_token = 1
    
    if 'row' in constants:
        row_token = constants['row']
    else:
        row_token = 1
    
    if constants['current'] == '\n':
        row_token = constants['row'] + 1
        endset_token = 0
        onset_token = 0

    present = TOKEN(worker, stringa_c)
    future = TOKEN(worker, stringa_f)

    if present[0] == True and future[0] == False:
        endset_token += 1
        await WORKER.SPEAK(worker,f"tokens:{constants['file']}|{row_token}:{onset_token}:{endset_token}",stringa_c)
        #await WORKER.ECHO(worker,out+c)
        #print(constants)
        #print(f"ON:'{onset_token}',END:'{endset_token}',ROW:'{row_token}',Token:'{stringa_c}'")
        return {'output':'','onset':endset_token,'endset':endset_token,'row':row_token}
    else:
        endset_token += 1
        return {'output':stringa_c,'onset':onset_token,'endset':endset_token,'row':row_token}
'''
||| Lexer: Analizza una sequenza di caratteri e li converte in una sequenza di token.
'''
async def FILE(worker,**constants):
    #print(constants)
    file = constants['pattern'].replace('files:', '')
    await WORKER.READER(worker,file,TOKENIZER,'char')

async def LEXER(worker):
    '''
    ||| Legge la sorgente e applica la funzione tokenizer
    '''
    await asyncio.sleep(1)
    await WORKER.READER(worker,worker.app.args[1],TOKENIZER,'char')
    await WORKER.EVENT(worker,'files:*',FILE)
    await WORKER.HEAR(worker,'files:*')