import object
import logic

# ------------------------------------------------------------------------------
#   Un dato è caratterizzato da 3 proprietà fondamentali: tipo, cardinalità e valore.
# ------------------------------------------------------------------------------

class VARIABLE(object.OBJECT):
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
        VALUE=None,
        identifier = "@ID",
        PROPERTY:dict=dict(),
        EVENTS:dict=dict(),#quando viene cambiato il valore x 
    ) -> None:
        # imposta valore
        self._VALUE = VALUE
        self._INDEX = 0
        self.identifier = identifier
        # controlla tipo
        if TYPE == None:
            self._TYPE = str(type(VALUE))
        else:
            self._TYPE = TYPE

        # controlla il tipo variabile
        if hasattr(VALUE,'__iter__'):
            self._CARDINALITY = len(self._VALUE)
            self.Identity = logic.EXPRESSION('VALUE',logic.EACH_t(logic.EQL,TYPE,logic.TARGET))
        else:
            self._CARDINALITY = 1
            self.Identity = logic.EXPRESSION('VALUE',logic.EACH_t(logic.EQL,logic.TARGET,TYPE))

        #self.OPERATORS = dict()
        #self.OPERATORS['='] = self.SET

        for KEY in PROPERTY:
            if hasattr(self,KEY):
                if PROPERTY[KEY](None,getattr(self,KEY))[0]:
                    print(KEY,"true")
                else:
                    print("false")
                #self.IDENTITY = logic.EXPRESSION('VALUE',logic.OR())
        
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
    
    def ECHO(self,worker):
        print(self._VALUE)
    
    
    @object.OBJECT.ACTION(logic.EXPRESSION("ECHO",logic.EQL(1,1)),['asd'])
    def SET(self,worker,VALUE)->None:
        #self.Identity(worker,[str(type(VALUE))])[0]:
        if True:
            self._VALUE = VALUE
        else:
            worker.logger.error('value does not respect constraints !')
    
    def GET(self)->any:
        return self._VALUE
    
    def TYPE(self,worker)->str:
        return str(self._TYPE)
    
    @object.OBJECT.ACTION(logic.EXPRESSION("ECHO",logic.EQL(1,1)),['asd'])
    def CAD(self,worker)->any:
        return self._VALUE
    def SIZE(self,worker)->any:
        return self._VALUE
    def ADD(self,worker,VALUE)->None:
        ss = []
        for x in VALUE:
            ss.append(str(type(VALUE[x])))
        if self.Identity(worker,ss)[0] and hasattr(self._VALUE,'__iter__'):
            self._VALUE = self._VALUE | VALUE
        else:
            print("ERROR ADD")
    
    def __iter__(self):
        return self
    
    def __str__(self):
        return "DATA:" + str(self._VALUE)
    
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
    

class CONSTANT(VARIABLE):pass