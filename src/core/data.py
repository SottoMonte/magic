import object
import logic
import copy

# ------------------------------------------------------------------------------
#   Un dato è caratterizzato da 3 proprietà fondamentali: tipo, cardinalità e valore.
# ------------------------------------------------------------------------------

class variable(object.OBJECT):
    '''
    ||| -- VARIABLE -- [CARDINALITY,VALUE,TYPE]
    |||[DATA]: CARDINALITY,VALUE,TYPE
    |||[logic]: HOMOGENEOUS,HETEROGENEOUS,EMPTY,INIT
    |||[ACT]: SET,GET,ECHO
    |||[EVENTS]: SET,SETTING,GET,GETTING
    '''

    def __init__(
        self,
        TYPE=None,
        identifier = "@ID",
        VALUE=None,
        *args,
        **kwargs,
        #PROPERTY:dict=dict(),
        #EVENTS:dict=dict(),#quando viene cambiato il valore x 
    ) -> None:
        # imposta valore
        self._INDEX = 0
        self.identifier = identifier
        # controlla tipo
        if TYPE != None:
            if str(type(VALUE)) in TYPE:
                print("PASS",identifier,type(VALUE),TYPE)
                #self._TYPE = str(type(VALUE))
                self._TYPE = TYPE
                self._VALUE = VALUE
            elif str(type(VALUE)) == str(type(None)):
                print("PASS",identifier,type(VALUE),TYPE)
                self._TYPE = TYPE
                self._VALUE = VALUE
            else:
                print("NOT",identifier,type(VALUE),TYPE)
        else:
            self._TYPE = TYPE

        # controlla il tipo variabile
        if hasattr(VALUE,'__iter__'):
            self._CARDINALITY = len(VALUE)
            self.Identity = logic.EXPRESSION('Identity',logic.EACH(logic.EQL,logic.TARGET,TYPE))
        else:
            self._CARDINALITY = 1
            self.Identity = logic.EXPRESSION('Identity',logic.EACH(logic.EQL,logic.TARGET,self._TYPE))

        #self.OPERATORS = dict()
        #self.OPERATORS['='] = self.SET

        '''for KEY in PRO:
            if hasattr(self,KEY):
                if PROPERTY[KEY](None,getattr(self,KEY))[0]:
                    print(KEY,"true")
                else:
                    print("false")
                #self.IDENTITY = logic.EXPRESSION('VALUE',logic.OR())'''
        if 'transform' in kwargs:
            self.transform = kwargs['transform']
        else:
            self.transform = None
        
    '''
    |||[DATA]
    '''
    #CARDINALITY = logic.EXPRESSION('CARDINALITY',logic.EQL(logic.TARGET,type(1)))
    #TYPE = logic.EXPRESSION('TYPE',logic.EQL(logic.TARGET,type("str")))
    #VALUE = logic.EXPRESSION('VALUE',logic.EQL(logic.TARGET,type("str")))
    '''
    |||[logic]
    '''
    Identity = logic.EXPRESSION('Identity',logic.EQL("1","1"))
    Iterable = logic.EXPRESSION('Iterable',logic.EQL("1","1"))
    Homogeneous = logic.EXPRESSION('Homogeneous',logic.EQL("1","1"))
    Heterogeneous = logic.EXPRESSION('Heterogeneous',logic.EQL("1","1"))
    '''
    |||[ACTION]
    '''
    
    #@object.OBJECT.ACTION(logic.EXPRESSION("SET",logic.minimum(logic.EQL,logic.TARGET,["<class 'str'>"])),['asd'])
    @object.OBJECT.ACTION(None,logic.EXPRESSION("SET",logic.SEQUENTIAL(logic.EQL,logic.TARGET,["<class 'str'>"])))
    def SET(self,worker,VALUE)->None:
        id = self.Identity(worker,str(type(VALUE)))
        
        if id[0]:
            worker.app.GET().logger.debug(f"SET pass the bound {id[1]} with {self.Identity} and data := {id[2]}")
            self._VALUE = VALUE
        else:
            worker.app.GET().logger.error(f"SET Not pass the bound {id[1]} with {self.Identity} and data := {id[2]}")
    
    def SET_TEMP(self,worker,VALUE):
        self._VALUE = VALUE

    def GET(self)->any:
        return self._VALUE
    
    def FIRST(self,worker):
        return self._VALUE[0]
    def LAST(self,worker):
        return self._VALUE[-1]
        
    def RANGE(self,worker,a=None,b=None):
        if 0 <= a < len(self._VALUE):
            print("BOOOOM!!!")
            if b == None:
                
                return self._VALUE[a:]
            else:
                return self._VALUE[a:b]
        else:
            print('KABOOM!')
            return "self._VALUE"
        
    def ELEMENT(self,worker,a=None):
        if 0 <= a < len(self._VALUE):
            return self._VALUE[a]
        else:
            return self._VALUE
        
    def NONE(self,worker):
        for x in self._VALUE:
            print(x)
        return self._VALUE
    
    def TTT(self,worker):
        #return worker.loop.GET().run_until_complete(self.transform(self,worker))
        return self.transform(self,worker)
    
    def GG(self,worker):
        return worker.loop.GET().run_until_complete(self.transform(self,worker))
        #return self.transform(self,worker)
    
    def TYPE(self,worker)->str:
        return str(self._TYPE)
    
    def COPY(self,worker)->any:
        return copy.deepcopy(self)
    
    #@object.OBJECT.ACTION(logic.EXPRESSION("ECHO",logic.EQL(1,1)),['asd'])
    def CAD(self,worker)->any:
        return self._VALUE
    
    def SIZE(self,worker)->any:
        return self._VALUE
    
    def ADD(self,worker,VALUE)->None:
        OUT = self.Identity(worker,[str(type(VALUE))])
        #print(OUT)
        if OUT[0]  and hasattr(self._VALUE,'__iter__'):
            #print(self._VALUE,VALUE)
            self._VALUE = self._VALUE | VALUE
            #self._VALUE.append(VALUE)
        else:
            print("ERROR ADD")
    
    def __iter__(self):
        return self
    
    def __str__(self):
        return f"{self._TYPE}:{self.identifier} := {str(self._VALUE)}"
    
    def __repr__(self):
        return f"{str(self._TYPE):<40.40}:{self.identifier:<15.15} = {str(self._VALUE):<30.30}"
    
    def __next__(self):
        if hasattr(self._VALUE,'__iter__'):
            if self._INDEX >= len(self._VALUE):
                self._INDEX = 0
                raise StopIteration
            try:
                result = self._VALUE[self._INDEX]
            except:
                result = self._VALUE[next(iter(self._VALUE))]
            
            self._INDEX += 1
            return result
        else:
            if self._INDEX >= 1:
                raise StopIteration
            self._INDEX += 1
            return self._VALUE
    

class constant(variable):pass