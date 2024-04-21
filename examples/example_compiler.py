# Import
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
    app = application.mathemagic("mathemagic.com",sys.argv,{})
    app.JOB(lexical.LEXER)
    app.JOB(syntax.PARSER)
    app.JOB(semantic.VALIDATOR)
    #app.JOB(transpiler.TRANSLATOR)
    app.RUN()