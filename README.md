Data Distribution Service
Data Oriented Languages
Agent Oriented Programming Languages
Authoring languages
Logic programming
Constraint programming
Constraint logic programming
Logic-based languages
Concurrent languages
Dataflow programming
Declarative languages
Functional programming
Fifth-generation programming language
Iterative languages
Metaprogramming languages
Reflective languages
Rule-based languages
Synchronous languages
Event-driven programming
Aspect-oriented programming

https://www.linkedin.com/pulse/choosing-between-data-event-driven-architecture-bruno-fonzi
https://tjhunter.github.io/dds_py/tut_custom_types/
https://en.wikipedia.org/wiki/Finite-state_machine
https://en.wikipedia.org/wiki/Side_effect_(computer_science)
https://en.wikipedia.org/wiki/Pure_function
https://en.everybodywiki.com/Data-oriented_programming
https://en.wikipedia.org/wiki/List_of_programming_languages_by_type#Data-oriented_languages
https://en.wikipedia.org/wiki/Source-to-source_compiler
https://it.wikipedia.org/wiki/Tipo_di_dato
https://thecontentauthority.com/blog/lexer-vs-parser
http://www.di.uniba.it/~lops/linguaggi/TabellaSimboli.pdf
https://en.wikipedia.org/wiki/Abstract_syntax_tree
https://en.wikipedia.org/wiki/Programming_language
https://d2vkrkwbbxbylk.cloudfront.net/sites/default/files/archive/Data-Oriented_Architecture.pdf
https://github.com/dbartolini/data-oriented-design
https://it.wikipedia.org/wiki/Metadato
https://it.wikipedia.org/wiki/Dato
https://www.guru99.com/functional-programming-tutorial.html
https://www.studysmarter.co.uk/explanations/computer-science/computer-programming/declarative-programming/
https://hazelcast.com/glossary/data-pipeline/
https://docs.pydantic.dev/latest/why/
https://en.wikipedia.org/wiki/Truth_table

A pure function is idempotent
Recursion
First-class citizen
Referential transparency
Test unitari
DataFrame
metadato
cloud-native
DevOps,
Truth table
knowledge-based agentes
inference

Redis
Event-Data Pipelines

DSL dichiarativi (linguaggi specifici del dominio)

In Python, le astrazioni di ordine superiore si riferiscono a concetti che coinvolgono funzioni o metodi che operano su altre funzioni come argomenti o restituiscono funzioni come risultato

Una "funzione pura" è una funzione i cui input sono dichiarati come input e nessuno di essi deve essere nascosto. Anche gli output vengono dichiarati come output.

In DOP le tue funzioni sono di scopo generale e vengono applicate a grandi quantità di dati. Idealmente, strutturare i dati il ​​più vicino possibile ai dati di output per garantire il minimo sforzo da parte della funzione stessa.

# Principio - 1: codice separato dai dati

# Principio -2: rappresentare i dati con una struttura dati generica

# Principio - 3: i dati sono immutabili

# Principio -4: Schema dei dati separato dalla rappresentazione dei dati

# I token vengono elaborati internamente dal compilatore durante il processo di traduzione del codice sorgente in codice eseguibile. Ecco come avviene:

# Analisi lessicale (Lexing):
- In questa fase, il compilatore legge il codice sorgente carattere per carattere.
- Identifica sequenze di caratteri che costituiscono token validi.
- Ad esempio, se trova la sequenza if, riconosce questa come una parola chiave e crea un token corrispondente.
# Analisi sintattica (Parsing):
- Il compilatore organizza i token in una struttura gerarchica che rappresenta la struttura del programma.
- Questa struttura è spesso rappresentata come un albero di sintassi astratta (AST).
- Durante l’analisi sintattica, il compilatore verifica anche la correttezza della struttura del programma.
- Ad esempio, verifica se le parentesi sono bilanciate correttamente.
# Analisi semantica:
- In questa fase, il compilatore esamina il significato dei token e delle espressioni.
- Verifica che le variabili siano dichiarate prima di essere utilizzate, controlla la coerenza dei tipi e risolve i riferimenti alle funzioni e alle variabili.
- Ad esempio, se trova un identificatore, cerca la sua dichiarazione nel contesto.
# Generazione del codice intermedio:
- Il compilatore crea una rappresentazione intermedia del programma, spesso sotto forma di codice a tre indirizzi o di un altro formato simile.
- Questo codice intermedio semplifica la traduzione in codice macchina.
# Ottimizzazione del codice:
- Il compilatore applica diverse tecniche di ottimizzazione per migliorare l’efficienza del codice.
- Questo può includere la semplificazione di espressioni, la riduzione del numero di istruzioni e altre trasformazioni.
# Generazione del codice finale:
- Infine, il compilatore traduce il codice intermedio in codice macchina specifico per l’architettura del processore di destinazione.
- Questo codice macchina è ciò che viene eseguito dal computer.
- In breve, i token vengono elaborati internamente dal compilatore attraverso una serie di fasi, ciascuna delle quali contribuisce alla creazione del codice eseguibile finale.