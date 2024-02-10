from reader import Reader
from parsing import Parser
from nfa import NFA
from dfa import DFA
from direct_dfa import DDFA
from direct_reader import DirectReader
from time import process_time

#Andree Toledo 18439
#CCTI CC3071
#2024 NEW UPDATE


program_title = '''
|||||||||AUTÓMATA FINITO||||||||||

Genera NFA's de DFA's basado en una expresión regular y compara tiempos simulando una cadena!
NOTA: para la expresión epsilon, por favor usa la letra "e"

||||||||||||||||||||||||||||||||||
'''

main_menu = '''
||||||||||||||||||||||||||||||||||||||||||||||||
Elige una de las siguientes opciones, de 0 a 2:
1. Establecer una expresión regular.
2. Probar una cadena dada la expresión regular.
0. Salir.
||||||||||||||||||||||||||||||||||||||||||||||||
'''

submenu = '''
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
Selecciona una de las siguientes para probar tu expresión regular:

    1. Utiliza Thompson para generar un NFA y la construcción de Powerset para generar un DFA.
    2. Utiliza el método DFA directo.
    0. Volver al menú principal.
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''

thompson_msg = '''
     |||CONSTRUCCIÓN THOMPSON Y POWERSET|||'''
direct_dfa_msg = '''
     |||CONSTRUCCIÓN DFA DIRECTA|||'''
invalid_opt = '''
Err: ¡Esa no es una opción válida!
'''
generate_diagram_msg = '''
¿Te gustaría generar y ver el diagrama? [y/n]'''
type_regex_msg = '''
Introduce una expresión regular '''
type_string_msg = '''
Introduce una cadena '''

if __name__ == "__main__":
    print(program_title)
    opt = None
    regex = None
    method = None

    while opt != 0:
        print(main_menu)
        opt = input('> ')

        if opt == '1':
            print(type_regex_msg)
            regex = input('> ')

            try:
                reader = Reader(regex)
                tokens = reader.CreateTokens()
                parser = Parser(tokens)
                tree = parser.Parse()

                direct_reader = DirectReader(regex)
                direct_tokens = direct_reader.CreateTokens()
                direct_parser = Parser(direct_tokens)
                direct_tree = direct_parser.Parse()
                print('\n\tExpresion lista y aceptada')
                print('\tArbol parseado:', tree)

            except AttributeError as e:
                print(f'\n\tERR: Expresion Invalida (falta el parentesis)')

            except Exception as e:
                print(f'\n\tERR: {e}')

        if opt == '2':
            if not regex:
                print('\n\tERR: Debe de setear la expresion regular!')
                opt = None
            else:
                print(submenu)
                method = input('> ')

                if method == '1':
                    print(thompson_msg)
                    print(type_string_msg)
                    regex_input = input('> ')

                    nfa = NFA(tree, reader.GetSymbols(), regex_input)
                    start_time = process_time()
                    nfa_regex = nfa.EvalRegex()
                    stop_time = process_time()

                    print('\nTiempo a evaluar: {:.5E} seconds'.format(
                        stop_time - start_time))
                    print('¿La cadena pertenece a la expresión regular?(NFA)?')
                    print('>', nfa_regex)

                    dfa = DFA(nfa.trans_func, nfa.symbols,
                              nfa.curr_state, nfa.accepting_states, regex_input)
                    dfa.TransformNFAToDFA()
                    start_time = process_time()
                    dfa_regex = dfa.EvalRegex()
                    stop_time = process_time()
                    print('\nTiempo a evaluar: {:.5E} seconds'.format(
                        stop_time - start_time))
                    print('¿Pertenece la cadena a la expresión regular?(DFA)?')
                    print('>', dfa_regex)

                    print(generate_diagram_msg)
                    generate_diagram = input('> ')

                    if generate_diagram == 'y':
                        nfa.WriteNFADiagram()
                        dfa.GraphDFA()

                elif method == '2':
                    print(direct_dfa_msg)
                    print(type_string_msg)
                    regex_input = input('> ')
                    ddfa = DDFA(
                        direct_tree, direct_reader.GetSymbols(), regex_input)
                    start_time = process_time()
                    ddfa_regex = ddfa.EvalRegex()
                    stop_time = process_time()
                    print('\nTiempo a evaluar: {:.5E} seconds'.format(
                        stop_time - start_time))
                    print('¿Pertenece la cadena a la expresión regular?')
                    print('>', ddfa_regex)

                    print(generate_diagram_msg)
                    generate_diagram = input('> ')

                    if generate_diagram == 'y':
                        ddfa.GraphDFA()

                    ddfa = None

                elif method == '3':
                    continue

                else:
                    print(invalid_opt)

        elif opt == '0':
            print('Gracias por usar el programa.')
            exit(1)
