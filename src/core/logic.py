import itertools
from typing import TypeAlias,NewType

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

TARGET = "@TARGET@"
OUTPUT = "@OUTPUT@"
TRANSFORMED = "@TRANSFORMED@"
TRANSFORMED2 = "@TRANSFORMED2@"


class TRANSFORM():
    def __init__(self,TRANSFORM=None,*args):
        self.vars = args
        self.function = TRANSFORM
    def __call__(self, TARGET):
        if self.vars[0] in TARGET:
            return self.function(TARGET[self.vars[0]])
        else:
            pass

logic = tuple[bool, str, list]


class EXPRESSION():
    def __init__(self, identifier, expression, **kwargs):
        self.identifier = identifier
        self.logic = expression
        self.kwargs = dict()
        #self.kwargs[TRANSFORMED] = kwargs.get("TRANSFORM")
        self.do = kwargs

    def __call__(self, worker,target=None,**kwargs)-> logic:
        # trasforma i dati 
        new = dict(self.kwargs, **kwargs)
        new[TARGET] = target

        '''TEST=(SON,'X')
        for x in self.do:
            if self.do[x][1] in new:
                new[x] = self.do[x][0](new[self.do[x][1]])'''
        
        for x in self.do:
            new[x] = self.do[x](new)
        
        return self.logic(new)
    
    def __getitem__(self, items):
        print (type(items), items)
        return True

class EQL():
    def __init__(self, A,B):
        self.dat = dict()

        self.A = A
        self.B = B

        un = {'A':A,'B':B}
        for x in un:
            #print(un[x])
            if type(un[x]) == type(""):
                if un[x][0] == '@':
                    self.dat[x] = un[x][1:]


        
    def __str__(self):
        return f"{self.A} == {self.B}"
    def __call__(self, args):
        work = dict({'A':self.A,'B':self.B})     
        print(".....>",work,args)
        for x in self.dat:
            match x:
                case 'A':
                    if self.dat[x] in args:
                        work['A'] = args[self.dat[x]]
                    else:
                        print("NON CE A")
                        return (True,"EQL",[work])
                case 'B':
                    if self.dat[x] in args:
                        work['B'] = args[self.dat[x]]
                    else:
                        print("NON CE B")
                        return (True,"EQL",[work])
        #args.clear()
        return logic((self.logic(work['A'],work["B"]),"EQL",[work]))
    
    def logic(self,TARGET,TEST):
        print(type(TARGET),":",TARGET,"==",type(TEST),":",TEST)
        if TARGET == TEST:return True
        else: return False

class COUNT():
    def __init__(self, targer,count):
        self.dat = dict()

        self.target = targer
        self.count = count

        un = {'A':targer,'B':count}
        for x in un:
            print(un[x])
            if type(un[x]) == type(""):
                if un[x][0] == '@':
                    self.dat[x] = un[x][1:]


        
    def __str__(self):
        return f"{self.A} == {self.B}"
    def __call__(self, args):
        work = dict({'A':self.A,'B':self.B})     
        print(work,args)
        for x in self.dat:
            match x:
                case 'A':
                    if self.dat[x] in args:
                        work['A'] = args[self.dat[x]]
                    else:
                        print("NON CE A")
                        return (True,"EQL",[work])
                case 'B':
                    if self.dat[x] in args:
                        work['B'] = args[self.dat[x]]
                    else:
                        print("NON CE B")
                        return (True,"EQL",[work])
        #args.clear()
        return logic((self.logic(work['A'],work["B"]),"EQL",[work]))
    
    def logic(self,TARGET,TEST):
        print(type(TARGET),":",TARGET,"==",type(TEST),":",TEST)
        if TARGET == TEST:return True
        else: return False

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

        return logic((self.logic(destro,sinstro),"EQL",[destro,sinstro]))
    
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

        return logic((self.logic(destro,sinstro),"EQL",[destro,sinstro]))
    
    def logic(self,TARGET,TEST):
        print(type(TARGET),":",TARGET,"<",type(TEST),":",TEST)
        if TARGET >= TEST:return True
        else: return False

class TYPE():
    def __init__(self, A,B):
        self.target = A
        self.check = B
    def __str__(self):
        return " == "
    def __call__(self, args):
        destro,sinstro = self.target,self.check
        print(args)
        if self.target == TARGET:
            destro = args[TARGET]
            
        if self.check == TARGET:
            sinstro = args[TARGET]

        return logic((self.logic(destro,sinstro),"EQL",[destro,sinstro]))
    
    def logic(self,TARGET,TEST):
        print(TARGET,TEST)
        if TARGET == TEST:return True
        else: return False

class OR():
    def __init__(self,*args):
        self.items = args
    def __repr__(self):
        
        return "OR"
    def __call__(self,*args):
        for ITEM in self.items:
            TESTED = ITEM(*args)
            if TESTED[0] == True : return TESTED
        return (False,repr(self),TARGET)

class AND():
    def __init__(self,*args):
        self.items = args
    def __repr__(self):
        strig = "AND("
        for x in self.items:
            strig += repr(x) + ","
        strig += ")"
    def __call__(self,*args):
        lis = []
        for ITEM in self.items:
            TESTED = ITEM(*args)
            if TESTED[0] == False : return (TESTED[0],"AND",TESTED[2])
        return (True,"AND",args)

class EACH():
    def __init__(self, check,*args):
        self.args = args
        self.check = check

        self.dat = dict()
        un = {'A':args[0],'B':""}
        for x in un:
            print(un[x])
            if type(un[x]) == type(""):
                try:
                    if un[x][0] == '@':
                        self.dat[x] = un[x][1:]
                except:
                    pass
                
    def __repr__(self):
        return f"EQL(DATA,DATA)"
    def __call__(self, args):
        work = dict({'A':self.args[0],'B':"self.target"})     
        #print(work,args)
        for x in self.dat:
            match x:
                case 'A':
                    if self.dat[x] in args:
                        work['A'] = args[self.dat[x]]
                    else:
                        #print("NON CE A")
                        return (True,"EQL",[work])
                case 'B':
                    if self.dat[x] in args:
                        work['B'] = args[self.dat[x]]
                    else:
                        #print("NON CE B")
                        return (True,"EQL",[work])
        print("---->",work)
        #if hasattr(work['A'],'__iter__'):
        if True:
            for x in args:
                print("-->",x)

            logic((False,"tt",[]))
        

class EACH_t():
    def __init__(self, check,a,b):
        self.target = a
        self.targets = b
        self.check = check
        self.dat = dict()
        un = {'A':b,'B':a}
        for x in un:
            #print(un[x])
            if type(un[x]) == type(""):
                if un[x][0] == '@':
                    self.dat[x] = un[x][1:]

    def __repr__(self):
        return f"EQL(DATA,DATA)"
    def __call__(self, args):
        out = []
        work = dict({'A':self.targets,'B':self.target})
        for x in self.dat:
            match x:
                case 'A':
                    if self.dat[x] in args:
                        work['A'] = args[self.dat[x]]
                    else:
                        #print("NON CE A")
                        return (True,"EQL",[work])
                case 'B':
                    if self.dat[x] in args:
                        work['B'] = args[self.dat[x]]
                    else:
                        #print("NON CE B")
                        return (True,"EQL",[work])
        print("---->",work)
        if hasattr(work['A'],'__iter__'):
            if hasattr(work['B'],'__iter__'):
                for x in  work['A']:
                    w = []
                    for y in work['B']:
                        a = self.check(x,y)
                        #print(x,y,a(args))
                        w.append(a(args)[0])
                    out.append(any(w))
                return logic((all(out),"",[]))
            else:
                for x in  work['A']:
                    a = self.check(x,y)
                    out.append(a(args)[0])
                    out.append(any(w))
                return logic((all(out),"",[]))

        else:
            if hasattr(work['B'],'__iter__'):
                for x in  work['B']:
                    a = self.check(x,work['A'])
                    out.append(a(args)[0])
                return logic((all(out),"",[]))
            else:
                return logic((self.check(work['B'],work['A']),"",[]))