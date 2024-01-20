# Import
import sys
sys.path.append('src/core/')
sys.path.append('src/analyzer/')
import lexical
import syntax
import semantic
import application
import asyncio
import logic
    
# Main
if __name__ == "__main__":
    app = application.mathmagic("example.cli",sys.argv,{application.INTERFACE.CLI:application.CLI})
    app.JOB(lexical.LEXER)
    app.JOB(syntax.PARSER)
    app.JOB(semantic.VALIDATOR)
    app.RUN()