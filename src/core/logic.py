import itertools
from typing import TypeAlias,NewType
'''
# Test
'''
class TEST:
    def __init__(self, *model):
        self.model = model

    def __call__(self,worker):
        return self.check(worker)

    def check(self,worker):
        for test in self.model:
            function, expected_result, input_value = test
            actual_result,actual_name,actual_data = function(worker,input_value)
            if actual_result != expected_result:
                print(f"{actual_name} non passa il test con [{input_value}|{actual_data}]: {actual_result} in {function.identifier}")
                exit(1)
            else:
                print(f"{actual_name} passa il test con [{input_value}|{actual_data}]: {actual_result} in {function.identifier}")

TARGET = "_target"
OUTPUT = tuple[bool, str, list]

class BASE():
    necessity = []
    def change(self,work,args):
        for x in work:
            if type(work[x]) == type([]):
                for idz, z in enumerate(work[x]):
                    if z in args:
                        work[x][idz] = args[z]
            elif type(work[x]) == type(''):
                if work[x] in args:
                    work[x] = args[work[x]]
    
    def start(self,items):
        self.necessity = []
        for item in items:
            if type(item) == type(""):
                if item.startswith('_'):
                    self.necessity.append(item)
                
    def splice(self,work,item):
        for req in item.requirement():
                
            #print('TOT',tot)
            if type(req) == type(''):
                #print(work[TARGET])
                if req.startswith('_') and req[1:].isdigit():
                    if len(work[TARGET]) > int(req[1:]):
                        work[req] = work[TARGET][int(req[1:])]
                    else:
                            work[req] = req
                tt = req[1:].split(':')
                if req.startswith('_') and len(tt) == 2:
                    if len(work[TARGET]) >= 3:
                        if tt[1] == '':
                            work[req] = work[TARGET][int(tt[0]):]
                        else:
                            work[req] = work[TARGET][int(tt[0]):int(tt[1])]
                    else:
                        work[req] = req
                        #print(work[req])
                    

            if req == '_first':
                work['_first'] = work[TARGET][0]
            if req == '_last':
                work['_last'] = work[TARGET][-1]

    def requirement(self):
        return self.necessity

'''
# Logic
'''
class EXPRESSION(BASE):
    def __init__(self, identifier, expression, **kwargs):
        self.necessity = [TARGET]
        self.identifier = identifier
        self.logic = expression
        #self.kwargs[TRANSFORMED] = kwargs.get("TRANSFORM")
        self.data = kwargs

        for x in kwargs:
            self.necessity.append(x)

        

    def __str__(self):
        return f"{self.identifier} := {str(self.logic)}"

    def requirement(self):
        return self.logic.requirement()
    
    def __call__(self, worker,target=None,**kwargs)-> OUTPUT:
        # trasforma i dati 
        new = dict(**kwargs)

        if type(target) == type(dict()):
            new.update(target)
        else:
            new[TARGET] = target
        
        cc = None
        
        for d in self.data:
            cc = self.data[d].COPY(worker)
            #print(cc.GET())
            if cc.GET() == 'FFF':
                cc.SET_TEMP(worker,kwargs.copy())
                #print("--------------------------------------------------------------------------")
                new[d] = cc.TTT(worker)
            else:
                cc.SET_TEMP(worker,new[cc.GET()])
            #print(cc.TTT)
            if cc.TTT != None:
                new[d] = cc.TTT(worker)
            #print("###",new[d])

        #print("------------------------------------------------------",self.identifier,new)
        return self.logic(worker,new)

class TRAN(BASE):
    def __init__(self, logica,da,a,cont=False):
        self.logica = logica
        self.da = da
        self.a = a
        self.cont = cont
        self.start([da])

    def __str__(self):
        return f"{self.logica} == {self.a}"
    
    def __call__(self,worker, args):
        
        #print(args)
        work = dict({})
        if self.da in args:
            
            if self.cont == False:
                work[self.a] = args[self.da]
            else:
                a = []
                a.append(args[self.da])
                work[self.a] = a
                
        
        #print('#001 ',work,self.logica)

        return self.logica(worker,work)

class EQL(BASE):
    def __init__(self, A,B):
        self.A = A
        self.B = B
        self.start([A,B])

    def __str__(self):
        return f"{self.A} == {self.B}"
    
    def __call__(self,worker, args):
        work = dict({'A':self.A,'B':self.B})
        for x in work:
            #print(x,work[x])  
            if type(work[x]) == type(''):
                #if work[x].startswith('@') and work[x][len(work[x])-1] == '@':
                if work[x] in args:
                    work[x] = args[work[x]]
                        #print("ver11",args)

        return OUTPUT((self.logic(work['A'],work["B"]),EQL.__name__,work))
    
    def logic(self,TARGET,TEST):
        #print(type(TARGET),":",TARGET,"==",type(TEST),":",TEST)
        if TARGET == TEST:return True
        else: return False

class EQL_LESS():
    def __init__(self, A,B):
        self.A = A
        self.B = B

    def __str__(self):
        return f"{self.A} <= {self.B}"
    
    def __call__(self,worker, args):
        work = dict({'A':self.A,'B':self.B})
        for x in work:
            #print(x,work[x])  
            if type(work[x]) == type(''):
                #if work[x].startswith('@') and work[x][len(work[x])-1] == '@':
                if work[x] in args:
                    work[x] = args[work[x]]
                        #print("ver11",args)

        return OUTPUT((self.logic(work['A'],work["B"]),EQL.__name__,work))
    
    def logic(self,TARGET,TEST):
        #print(TARGET,TEST)
        #print(type(TARGET),":",TARGET,"==",type(TEST),":",TEST)
        if TARGET <= TEST:return True
        else: return False

class COUNT(BASE):
    def __init__(self, targer,count,counted,logic=EQL_LESS):
        self.target = targer
        self.count = count
        self.counted = counted
        #print(counted)
        self.bb = logic
        self.ll = logic(TARGET,counted)
        self.start([targer,count,counted])
    def __str__(self):
        return str(self.ll).replace(TARGET,f"{self.count} in {self.target}")
    def __call__(self,worker, args):
        work = dict({'target':self.target,'count':self.count,'counted':self.counted})
        for x in work:
            if type(work[x]) == type(''):
                #if work[x].startswith('@') and work[x][len(work[x])-1] == '@':
                if work[x] in args:
                    work[x] = args[work[x]]
        #print(work)
        self.ll = self.bb(TARGET,work['counted'])

        return OUTPUT((self.logic(work['target'],work["count"]),COUNT.__name__,work))
    
    def logic(self,target,TEST):
        #print("--------------->",target)
        if self.ll(None,{TARGET:target.count(TEST)})[0]:
            return True
        else:
            return False
        
class SORT():
    def __init__(self, GREATER,MINOR):
        self.target = GREATER
        self.check = MINOR
    def __str__(self):
        return " == "
    def __call__(self, args):
        destro,sinstro = self.target,self.check
        print(args)
        if self.target == TARGET:
            destro = args[TARGET]
            
        if self.check == TARGET:
            sinstro = args[TARGET]

        return OUTPUT((self.logic(destro,sinstro),"EQL",[destro,sinstro]))
    
    def logic(self,TARGET,TEST):
        print(type(TARGET),":",TARGET,">",type(TEST),":",TEST)
        if TARGET < TEST:return True
        else: return False

class SORT_EQL():
    def __init__(self, GREATER,MINOR):
        self.target = GREATER
        self.check = MINOR
    def __str__(self):
        return " == "
    def __call__(self, args):
        destro,sinstro = self.target,self.check
        print(args)
        if self.target == TARGET:
            destro = args[TARGET]
            
        if self.check == TARGET:
            sinstro = args[TARGET]

        return OUTPUT((self.logic(destro,sinstro),"EQL",[destro,sinstro]))
    
    def logic(self,TARGET,TEST):
        print(type(TARGET),":",TARGET,"<",type(TEST),":",TEST)
        if TARGET >= TEST:return True
        else: return False

class OR(BASE):
    def __init__(self,*args):
        self.items = args
        self.necessity = []
        for arg in args:
            #print(arg)
            self.necessity.append(arg.requirement())
    def __repr__(self):
        out = str(self.items[0])
        for i in self.items[1:]:
            out += ' | ' + str(i) 
        return out
    def __call__(self,worker,args):
        work = {}
        work.update(args)
        self.change(work,args)
        
        vvv = []
        ggg = [work]
        for item in self.items:
            self.splice(work,item)
            vvv.append(item.identifier)
            
            tested = item(worker,work)
            ggg.append(tested[2])
            
            #print("TESTED ---------------------------------------",tested)
            if tested[0] == True:
                return (tested[0],item.identifier,ggg)
        return (False,vvv,ggg)

class AND(BASE):
    def __init__(self,*args,**kwargs):
        self.items = args
        self.stran = kwargs
        self.necessity = []
        for arg in args:
            #print(arg)
            cccc = arg.requirement()
            
            if len(cccc) <= 1:
                self.necessity.append(cccc)
            else:
                for nnn in cccc:
                    if len(nnn) != 0:
                        self.necessity.append(nnn)
                pass
    def __repr__(self):
        out = str(self.items[0])
        for i in self.items[1:]:
            out += ' & ' + str(i) 
        return out
    def __call__(self,worker,args):
        work = {}
        work.update(args)
        w_out = []
        
        self.change(work,args)
        uni = {}
        for itx,item in enumerate(self.items):
            uni = {}
            for req in self.stran:
                
                if req[1:] == str(itx):
                    #print("-----------------------------------------------------------------",work[self.stran[req][0]])
                    worker.job.SET_TEMP(worker,work[self.stran[req][0]])
                    if self.stran[req][4] == False: 
                        uni[self.stran[req][1]] = self.stran[req][2](worker.job,worker,*self.stran[req][3])
                    else:
                        uni[self.stran[req][1]] = [self.stran[req][2](worker.job,worker,*self.stran[req][3])]
            
            TESTED = item(worker,work|uni)
            w_out.append(TESTED[2])
            #print(TESTED)
            if TESTED[0] == False : return (False,"AND",w_out)
        return (True,"AND",w_out)

class EACH(BASE):
    def __init__(self, logic, target, compare):
        self.target = target
        self.compare = compare
        self.check = logic
        self.exem = logic(target,compare)
        self.start([target,compare])


    def __repr__(self):
        return str(self.exem).replace(str(self.compare),f"$next in {self.compare}")
        #return "MINI"
    
    def __call__(self,worker, args):
        # Data job
        work = dict({'target':self.target,'com':self.compare.copy()})
        #print(work,args)
        # Trasform data
        for x in work:
            if type(work[x]) == type([]):
                for idz, z in enumerate(work[x]):
                    if z in args:
                        work[x][idz] = args[z]
            elif type(work[x]) == type(''):
                if work[x] in args:
                    work[x] = args[work[x]]

        lall = []
        temp = []
        # Do job
        for x in work['target']:
            temp = []
            for target in work['com']:
                #print("=====>",target,x)
                check_d = self.check(target,x)
                check = check_d(worker,work)
                temp.append(check[0])
            lall.append(any(temp))

        if len(lall) == 0:
            return (False,'EACH',work)
        
        #print(lall)
        return (all(lall),"minimum",work)
    
class EACH2(BASE):
    def __init__(self, logic, target):
        self.target = target
        self.check = logic
        #self.exem = logic(target,compare)
        self.start([target])


    def __repr__(self):
        return 'str(self.exem).replace(str(self.compare),f"$next in {self.compare}")'
        #return "MINI"
    
    def __call__(self,worker, args):
        # Data job
        work = dict({'target':self.target})
        self.change(work,args)
        lall = []
        temp = []
        # Do job
        for x in work['target']:
            check = self.check(worker,x)
            
            lall.append(check[0])

        #print("4444 ###########",all(lall))
        return (all(lall),"minimum",work)

class EACHONE():
    def __init__(self, logic, target, compare):
        self.target = target
        self.compare = compare
        self.check = logic
        self.exem = logic(target,compare)

    def __repr__(self):
        return str(self.exem).replace(str(self.compare),f"$next in {self.compare}")
        #return "MINI"
    
    def __call__(self,worker, args):
        # Data job
        work = dict({'target':self.target,'com':self.compare.copy()})
        #print(work,args)
        # Trasform data
        for x in work:
            if type(work[x]) == type([]):
                for idz, z in enumerate(work[x]):
                    if z in args:
                        work[x][idz] = args[z]
            elif type(work[x]) == type(''):
                if work[x] in args:
                    work[x] = args[work[x]]

        lall = []
        temp = []
        # Do job
        for x in work['target']:
            temp = []
            for target in work['com']:
                #print("=====>",target,x)
                check_d = self.check(target,x)
                check = check_d(worker,work)
                temp.append(check[0])
            lall.append(any(temp))

        
        #print(lall)
        return (all(lall),"minimum",work)
#maximum
        
class SEQUENTIAL():
    def __init__(self, logic, target, compare):
        self.target = target
        self.targets = compare
        self.check = logic
        self.exem = logic(target,compare)

    def __repr__(self):
        return str(self.exem).replace(str(self.targets),f"$next in {self.targets}")
        #return "MINI"
    
    def __call__(self, w,args):
        # Data job
        work = dict({'target':self.target,'check':self.targets})
        #print(work,args)
        # Trasform data
        for x in work:
            if type(work[x]) == type(''):
                if work[x] in args:
                    work[x] = args[work[x]]
        # Do job
        for idx, target in enumerate(work['target']):
            check_d = self.check(str(type(target)),work['check'][idx])
            check = check_d(w,work)
            if not check[0]:return (False,"seq",work)

        return (True,"seq",work)