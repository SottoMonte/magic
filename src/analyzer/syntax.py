import worker as WORKER
import data as DATA
import grammar
#from STRING import SPLIT
#from BOOLEAN import OR
import builtins
import asyncio

# unary,binary,call,assignment

class BinaryTreeNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.leftChild = left
        self.rightChild = right
    def __str__(self) -> str:
        stringa = f"({str(self.leftChild)},{self.data},{str(self.rightChild)})"
        #for one in self.children:
        #    stringa += str(one)
        return stringa
    

class UnaryTreeNode:
    def __init__(self, data):
        self.data = data
    def __str__(self) -> str:
        stringa = str(self.data)
        #for one in self.children:
        #    stringa += str(one)
        return stringa

class CallTreeNode:
    def __init__(self, data):
        self.data = data
        self.subjects = None
        self.arguments = None
    def __str__(self) -> str:
        stringa = f"({str(self.leftChild)},{self.data},{str(self.rightChild)})"
        #for one in self.children:
        #    stringa += str(one)
        return stringa

class AllocationTreeNode:
    def __init__(self, data):
        self.data = data
        self.leftChild = None
        self.rightChild = None
    def __str__(self) -> str:
        stringa = f"({str(self.leftChild)},{self.data},{str(self.rightChild)})"
        #for one in self.children:
        #    stringa += str(one)
        return stringa

class AssignmenTreeNode:
    def __init__(self, data):
        self.data = data
        self.leftChild = None
        self.rightChild = None
    def __str__(self) -> str:
        stringa = f"({str(self.leftChild)},{self.data},{str(self.rightChild)})"
        #for one in self.children:
        #    stringa += str(one)
        return stringa
    
class TreeNode:
    def __init__(self, data):
        self.children = list([])
        self.data = data
    def __str__(self) -> str:
        stringa = ""
        for one in self.children:
            stringa += str(one)
        return stringa

# Abstract Syntax Tree
# Root Node := il nodo radice è il nodo più alto di un albero.
# Internal Nodes := i nodi interni sono i nodi che hanno almeno un figlio.
# Leaf Node := questi sono quei nodi nell'albero che non hanno figli.
# Edge := il riferimento attraverso il quale un nodo genitore è connesso a un nodo figlio è chiamato bordo.
# Child Node :=  i nodi figlio di un nodo genitore sono i nodi a cui punta il nodo genitore.
# Parent Node :=  il genitore di qualsiasi nodo è il nodo che fa riferimento al nodo corrente.
async def AST(Parent,Childs):
    # Binary operetor := + * & > → := = -
    # Unary operator := ! ~ ∼ - − ¬
    # Ternary
    node = Childs
    '''for edge in Childs:
        if len(edge) == 1:
            pass
        elif len(edge) == 2:
            pass'''

    #print("\n=========>",node)

    if type(Parent) == AllocationTreeNode:
        operator = node.index(':=')
        print(node)
        right = operator + 1
        left = operator - 1
        Parent.data = node[operator]
        
        Parent.leftChild = await AST(BinaryTreeNode(node[:left+1][1]),[node[:left+1][0],node[:left+1][2]])

        # dato,expressione,
        if len(node[right:]) == 1:
            print("--1")
            #Parent.rightChild = await AST(UnaryTreeNode(node[1]),[node[right]])
            Parent.rightChild = node[right]
        elif len(node[right:]) == 3:
            print("--2")
            #print(node[right:],node[right:][0],node[left:][4])
            Parent.rightChild = await AST(BinaryTreeNode(node[left:][3]),[node[right:][0],node[left:][4]])
        else:
            print("--3")
            tot = []
            exp = node[right:]
            ops = ['*','/','+','-',None]
            op = '*'
            while op != None:
                if op in exp:
                    operator2 = exp.index(op)
                    start = operator2-1
                    end = operator2+1
                    gg = await AST(BinaryTreeNode(op),[exp[start],exp[end]])
                    
                    exp[start:end+1] = [gg]*3

                    temp = []
                    
                    [temp.append(x) for x in exp if x not in temp or x != gg ]
                    exp = temp

                    #print(exp,'####')

                    tot.append(gg)
                else:
                    op = ops[ops.index(op) + 1]
            #print(exp,tot,node[right:][0])
            #Parent.rightChild = BinaryTreeNode(node[operator],node[right:][0],exp)
            Parent.rightChild = exp[0]
    elif type(Parent) == AssignmenTreeNode:
        operator = node.index('=')
        right = operator + 1
        left = operator - 1

        Parent.data = node[operator]
        Parent.leftChild = node[left]
        if len(node[right:]) == 1:
            #Parent.rightChild = await AST(UnaryTreeNode(node[1]),[node[right]])
            Parent.rightChild = node[right]
        elif len(node[right:]) == 3:
            #print(node[right:],node[right:][0],node[left:][4])
            Parent.rightChild = await AST(BinaryTreeNode(node[right:][1]),[node[right:][0],node[left:][4]])
        else:
            tot = []
            exp = node[right:]
            ops = ['*','/','+','-',None]
            op = '*'
            while op != None:
                if op in exp:
                    operator2 = exp.index(op)
                    start = operator2-1
                    end = operator2+1
                    gg = await AST(BinaryTreeNode(op),[exp[start],exp[end]])
                    
                    exp[start:end+1] = [gg]*3

                    temp = []
                    
                    [temp.append(x) for x in exp if x not in temp or x != gg ]
                    exp = temp

                    #print(exp,'####')

                    tot.append(gg)
                else:
                    op = ops[ops.index(op) + 1]
            Parent.rightChild = exp[0]
    elif type(Parent) == CallTreeNode:
        Parent.subjects = node[0]
        Parent.arguments = node[1:-1]
    elif type(Parent) == BinaryTreeNode:
        #Parent.data = node[1]
        Parent.leftChild = node[0]
        Parent.rightChild = node[1]
    
    elif type(Parent) == UnaryTreeNode:
        Parent.data = node[0]
    else:pass

    return Parent
'''
||| INSTRUCTOR
'''
async def INSTRUCTOR(worker,**constants):
    token = constants['data']
    varname = "tokens"
    if token != '\n' and not all([s.isspace() for s in token]) and token != "\n\n":
        varname = "tokens"
        #await WORKER.NEW(worker,DATA.VARIABLE(worker,'list',varname,[tokens]))
        await WORKER.SET(worker,varname,token,DATA.VARIABLE(worker,'list',varname,[token]))
        #await WORKER.SET(worker,varname,token,DATA.VARIABLE(worker,'list',varname,[token]))
        tokens = await WORKER.GET(worker,varname)
        #blocks = DATA.SPLIT(worker,tokens,';','{','}')
        #print("====>",blocks)
        #print(tokens.value)
        #print(tokens)
        
        
        if token == ';':
            instruction = tokens.value[:-1]
            print(instruction,token)
        #for instruction in blocks:
            for expression in [grammar.INSTRUCTION_ALLOCATION]:
                boolean, identifier, stated = expression(worker,instruction)
                print(identifier,boolean,instruction,stated)
                if boolean:
                    await WORKER.REM(worker,varname,tokens.cardinality+10)
                    match expression.identifier:
                        case grammar.INSTRUCTION_ASSIGNMENT.identifier:
                            chil = await AST(AssignmenTreeNode(None),instruction)
                            #ROOT.children.append(chil)
                        case grammar.INSTRUCTION_CALL.identifier:
                            chil = await AST(CallTreeNode(None),instruction)
                            #ROOT.children.append(chil)
                        case grammar.INSTRUCTION_ALLOCATION.identifier:
                            #print("BOOMM!!",blocks,instruction,stated)
                            chil = await AST(AllocationTreeNode(None),instruction)
                            print("======>",str(chil))
                            await WORKER.SPEAK(worker,"ast",str(chil))
                        case grammar.INSTRUCTION_BLOCK.identifier:
                            await WORKER.SPEAK(worker,"files:main.mm","")
                            pass
                else:
                    worker.app.logger.critical(f"SyntaxError{INSTRUCTOR.__name__[0] + INSTRUCTOR.__name__[1:].lower()}: '{''.join(instruction)}': invalid instruction at {constants['pattern']}")
                    print(f"maybe it was '{''.join(instruction).replace(stated[2],stated[0])}'")
'''
||| Input(TOKEN) | Output(AST)
'''
async def PARSER(worker:WORKER.WORKER):
    '''
    ||| Handle Tokens
    '''
    await WORKER.REM(worker,'tokens',100)
    await WORKER.EVENT(worker,'tokens:*',INSTRUCTOR)
    '''
    ||| Ascolta tutto il flusso di tokens e lo salva in TOKENS.
    '''
    await WORKER.HEAR(worker,'tokens:*')