import sys
sys.path.append('src/core/')
sys.path.append('src/analyzer/')
import data
import worker as WORKER
import logic
import application
import asyncio
import grammar


def sostituisci_dati(stringa, dati):
    # Sostituisci le occorrenze dei dati nella stringa
    for chiave, valore in dati.items():
        stringa = stringa.replace(f"'{chiave}'", str(valore))
    
    return stringa
# cose ?
# cosa è sbagliato ?
# dati
# ricostruire da i dati
def display_tree(node ,verity, depth=0, is_last=False,is_true=False):
    #print("====>",is_true)
    INDENT = "  "
    PREFIX = "└── " if is_last else "├── "
    RESET = "\u001b[0m"

    ERE = f'|{INDENT}' * (depth)
    #C = f'|{INDENT}' * depth
    COLOR2 = "\u001b[92m" if is_true else "\033[91m"
    #BAR = f'|{INDENT}' * depth
    BAR = f"{COLOR2}{ERE}{RESET}"
    

    if isinstance(verity, bool):
        exp = verity
        tipo = None
    else:
        exp = verity[1]
        tipo = verity[0]
        if isinstance(tipo, tuple):
            exp = verity[0][1]
            tipo = verity[0][0]
    COLOR = "\u001b[92m" if exp else "\033[91m"
    TUTTO = f"{BAR}{COLOR}{PREFIX}{RESET}"

    #print(tipo,exp)
    if tipo == logic.OR:
        #show(tipo, (1, True), liv)
        verita = any([x[1] for x in exp])
        display_tree(tipo, verita, depth,False,verita)
        for idx, x in enumerate(node):
            if len(node) == idx:
                display_tree(x, exp[idx], depth + 1,True,verita)
            else:
                display_tree(x, exp[idx], depth + 1,False,verita)
    elif tipo == logic.AND:
        eeeee = str(grammar.STRING)
        a= eeeee.split('∧')
        print(a)
        #show(tipo, (1, True), liv)
        verita = all([x[1] for x in exp])
        display_tree(tipo, verita, depth,False,verita)
        for idx, x in enumerate(node):
            if len(node) == idx:
                display_tree(x, exp[idx], depth + 1,True,verita)
            else:
                display_tree(x, exp[idx], depth + 1,False,verita)
    elif isinstance(node, tuple) and len(node) == 3:
        left_child, value, right_child = node
        print(f"{TUTTO}{value}")
        display_tree(left_child, verity, depth + 1,False,is_true)
        display_tree(right_child, verity, depth + 1,True,is_true)
    else:
        print(f"{TUTTO}{node}")

async def Test(worker:WORKER.WORKER):
    Identity = logic.EXPRESSION('Identity',logic.AND(
        #logic.EQL(logic.TARGET,10),
        logic.EQL(10,10),
        logic.EQL(10,10),
        logic.AND(
            logic.EQL(33,33),
            logic.EQL(10,10)
        )
        #logic.NOT(logic.EQL(10,10)),
        #logic.OR(logic.EQL(1,10),logic.EQL(50,10),logic.EQL(50,50)),
        #logic.COUNT('1234',"",6),
        #logic.OR(logic.EQL(10,10)),
        #logic.ALL(['11','22','3+'],grammar.NUMBER),
        #logic.INCLUSION("CIAOz",{'C','I','A','O','L'}),

    ))
    #print(Identity)
    
    #show(('', 'COUNT', ('12345', '#', '')))
    #show((6, '==', 6))
    #show(gg[2])
    try:
        #gg = Identity(worker,10)
        gg = grammar.STRING(worker,'"345"')
        print(grammar.STRING)
        print(gg)
        display_tree(gg[2],gg[1])
    except Exception as e:
        e_type = type(e).__name__
        e_file = e.__traceback__.tb_frame.f_code.co_filename
        e_line = e.__traceback__.tb_lineno

        e_message = str(e)

        print(f'exception type: {e_type}')

        print(f'exception filename: {e_file}')

        print(f'exception line number: {e_line}')

        print(f'exception message: {e_message}')


if __name__ == "__main__":
    app = application.mathemagic("logic.test",sys.argv,{})
    app.JOB(Test)
    app.RUN()