import fileinput
import GRAMMAR
from BOOLEAN import OR
import WORKER

'''
||| Input(STRING) | Output(TOKENS)
'''
async def LEXER(WORKER:WORKER.WORKER):
    '''
    ||| Legge un file e aggiunge un carattere di fine file @ è il carattere di fine stringa
    '''
    SOURCE = open('sorgente.sl', 'r').read() + '@'
    '''
    ||| Funzione che crea flusso di tokens
    '''
    async def TOKENIZER(self):
        '''
        ||| Concatena il token corrente con il prossimo carattere
        '''
        A = self.JOB + self.READ()
        '''
        ||| Se il token corrente è un identificatore, un numero, una parentesi chiusa, un separatore o un operatore,
        ||| aggiungi il token corrente al flusso di token.
        '''
        if OR([A],[GRAMMAR.IDENTIFIER,GRAMMAR.NUMBER,GRAMMAR.CLOSE,GRAMMAR.SEPARATOR,GRAMMAR.OPERATOR])[0] == True:
            self.JOB += self.READ()
        else:
            '''
            ||| Se il token corrente non è uno dei tipi sopra elencati,
            ||| invia il token corrente al parser e imposta il token corrente al prossimo
            '''
            if self.READ() != "\n":
                #await self._APP._PIPES['PARSER'].put(self.JOB)
                await self.SPEAK('PARSER',self.JOB)
                self.JOB = self.READ()
            #print("-",self.JOB)
        #print(self.READ())
        '''
        ||| Legge il prossimo carattere
        '''
        self.CONSUME()
    '''
    ||| Legge la sorgente e applica la funzione tokenizer
    '''
    await WORKER.READER(SOURCE,TOKENIZER)
    '''
    ||| Invia segnale parser fine flusso
    '''
    await WORKER.SPEAK('PARSER',None)