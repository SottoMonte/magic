
def STRING(target) -> str:
    return f"{target.identifier} = str({target.value})"

def INTEGER(target) -> str:
    return f"{target.identifier} = int({target.value})"

def CALL(target) -> str:
    args = ""
    for x in target.value:
        args += str(x) + ','
    return f"{target.identifier}({args})"


def APPLICATION(target) -> str:
    return '''# Import
import sys
import asyncio
sys.path.append('src/core/')
import application
import logic
sys.path.append('src/analyzer/')
import lexical
import syntax
import semantic
sys.path.append('src/compiler/')
import transpiler
    
# Main
if __name__ == "__main__":
    app = application.mathemagic("language.mathemagic",sys.argv,{application.INTERFACE.CLI:application.CLI})
    app.JOB(lexical.LEXER)
    app.JOB(syntax.PARSER)
    app.JOB(semantic.VALIDATOR)
    app.JOB(transpiler.BUILDER)
    app.RUN()'''