from lib2to3.pgen2 import grammar
import time
import re

import pandas as pd

# Leer el archivo Pretable.xlsx
file_path = 'Pretableex3.xlsx'
pretable_df = pd.read_excel(file_path)


# Convertir la tabla predictiva en un diccionario de diccionarios
pretable_dict = {}
tokens = pretable_df.iloc[0, 1:].values  # Primera fila como tokens
non_terminals = pretable_df.iloc[1:, 0].values  # Primera columna como no terminales

print(tokens)
print("")
print(non_terminals)
print("")




for i, non_terminal in enumerate(non_terminals):
    pretable_dict[non_terminal] = {}
    #print(pretable_dict[non_terminal])
    for j, token in enumerate(tokens):
        pretable_dict[non_terminal][token] = pretable_df.iloc[i+1, j+1]
        #print(pretable_dict[non_terminal][token])

print(pretable_dict)
print('')


# Definir las producciones en un diccionario
productions = {
    1: "PROGRAM → !init identifier ; BODY !end",
    2: "BODY → DECLARE MAIN",
    3: "BODY → MAIN",
    4: "DECLARE → var IDENTIFIERS : TYPES ;",
    5: "IDENTIFIERS → identifier ; AUXID",
    6: "AUXID → IDENTIFIERS",
    7: "AUXID → ε",
    8: "TYPES → DEFAULT",
    9: "DEFAULT → integer",
    10: "DEFAULT → decimal",
    11: "DEFAULT → char",
    12: "DEFAULT → string",
    13: "DEFAULT → bool",
    14: "MAIN → { STATEMENT }",
    15: "STATEMENT → ASSING",
    16: "EXPRESSION → EXP AUXEXS",
    17: "AUXEXS → ε",
    18: "AUXEXS → REL EXP",
    19: "EXP → TERM AUXEXP",
    20: "AUXEXP → ε",
    21: "AUXEXP → + EXP",
    22: "AUXEXP → - EXP",
    23: "AUXEXP → || EXP",
    24: "REL → ==",
    25: "REL → <",
    26: "REL → >",
    27: "REL → <=",
    28: "REL → >=",
    29: "REL → !=",
    30: "ASSING → identifier = EXPRESSION",
    31: "TERM → FACTOR AUXTERM",
    32: "AUXTERM → ε",
    33: "AUXTERM → * TERM",
    34: "AUXTERM → / TERM",
    35: "AUXTERM → && TERM",
    36: "FACTOR → { EXPRESSION }",
    37: "FACTOR → identifier",
    38: "FACTOR → true",
    39: "FACTOR → false",
    40: "FACTOR → string",
    41: "FACTOR → number",
    42: "STATEMENTS → STATEMENT AUXSTA",
    43: "AUXSTA → ε",
    44: "AUXSTA → STATEMENTS",
    45: "STATEMENT → FOR",
    46: "STATEMENT → WHILE",
    47: "STATEMENT → INPUT",
    48: "STATEMENT → OUTPUT",
    49: "STATEMENT → IF",
    50: "FOR → for COUNTER do { STATEMENTS }", #SEMANTIC
    51: "COUNTER → identifier := EXPRESSION for EXPRESSION",
    52: "WHILE → while EXPRESSION do { STATEMENTS }", #SEMANTIC
    53: "INPUT → read ( identifier AUXINOU )",
    54: "AUXINOU → , identifier AUXINOU",
    55: "AUXINOU → ε",
    56: "OUTPUT → write ( identifier AUXINOU )",
    57: "IF → if EXPRESSION then { STATEMENTS } AUXIF endif", #SEMANTIC
    58: "AUXIF → ε",
    59: "AUXIF → else { STATEMENTS }"
}



def find_identifiers_and_literals(text):
    # Define the regular expression patterns
    identifier_pattern = r'\$[A-Za-z0-9]+'  # Identifiers
    decimal_pattern = r'\b\d+\.\d+\b'       # Decimals
    integer_pattern = r'\b\d+\b'            # Integers
    string_pattern = r'\'[^\']*\'|\"[^\"]*\"'  # Strings enclosed in single or double quotes
    type_pattern = r'\b(?:integer|decimal|char|string|bool)\b'  # Specific keywords
    boolean_pattern = r'\b(?:true|false)\b'  # Booleans

    # Find all matches in the input text
    strings = re.findall(string_pattern, text)
    # Remove strings from text to avoid overlap with numbers
    text_without_strings = re.sub(string_pattern, '', text)

    decimals = re.findall(decimal_pattern, text_without_strings)
    # Remove decimals from text to avoid overlap with integers
    text_without_decimals = re.sub(decimal_pattern, '', text_without_strings)

    integers = re.findall(integer_pattern, text_without_decimals)
    identifiers = re.findall(identifier_pattern, text_without_strings)
    types = re.findall(type_pattern, text_without_strings, re.IGNORECASE)
    booleans = re.findall(boolean_pattern, text_without_strings, re.IGNORECASE)

    return {
        'identifiers': identifiers,
        'integers': integers,
        'decimals': decimals,
        'strings': strings,
        'types': types,
        'booleans': booleans
    }

# Example usage
text = "Here are some identifiers: $Identifier1, $ID2, and $Invalid. Some numbers: 123, 45.67, and 89. Some strings: 'Hello World', 'Python'."
print(find_identifiers_and_literals(text))


symbol_table = []


def find_productions(codigo, productions):
    words = codigo.split()
    found_productions = []

    for word in words:
        for key, production in productions.items():
            if word in production:
                found_productions.append((word, key))
                #print(word)

    return found_productions


#codigo = "!init identifier ; { identifier = true } !end"
#codigo = "!init identifier ; var identifier ; identifier ; : integer ; { identifier = number ; identifier = number } !end"
#codigo = "!init identifier ; { read ( identifier , identifier ) } !end"
#codigo = "!init identifier ; var identifier ; : integer ; { for identifier := identifier for identifier do { identifier = true } } !end"
#codigo = "!init identifier ; var identifier ; : integer ; { if number == number then { read ( identifier ) } else { write ( identifier ) } endif } !end"
#codigo = '!init identifier ; var identifier ; identifier ; identifier ; : integer ; { for identifier := identifier for identifier do { identifier = identifier + identifier } } !end'
#codigo = '!init identifier ; var identifier ; identifier ; identifier ; identifier ; : integer ; { identifier = number ; identifier = number ; if identifier == identifier then { identifier = number ; identifier = number ; } else { identifier = identifier ; identifier = number ; } endif } !end'
#codigo = '!init identifier ; var identifier ; identifier ; identifier ; identifier ; : integer ; { for identifier := number for number do { identifier = number identifier = number identifier = number + identifier ; identifier = identifier * number ; } } !end'

codigo = "!init identifier ; var identifier ; identifier ; identifier ; : integer ; { if true == true then { identifier = number identifier = number identifier = number } else { identifier = number identifier = number identifier = number } endif } !end"
codigo2 = "!init $MyProgam ; var $id1 ; $id2 ; $id3 ; : integer ; { if true == true then { $id1 = 5 $id2 = 10 $id3 = 20 } else { $id1 = 1 $id2 = 2 $id3 = 3 } endif } !end"

codigo = "!init $MyProgam ; var $id1 ; $id2 ; $id3 ; : integer ; { if true == true then { $id1 = 1 $id2 = 2 $id3 = 3 } else { $id1 = 5 $id2 = 9 $id3 = 10 } endif } !end"


print()

idlit = find_identifiers_and_literals(codigo)
print(idlit)

print(f'{len(codigo.split())} {len(codigo2.split())}')

productions_found = find_productions(codigo, productions)

change = ''

for key, value in productions.items():
    if productions_found[0][0] in value:
        print(value)
        change = value


print('AUXILIAR')
print(pretable_dict['IDENTIFIERS']['identifier'])


stack = [change.split()[0], '$']

print('CHANGE ',change.split()[0])



print()



codigosplit = codigo.split()
codigosplit.append('$')


print(f'PALABRA A VERIFICAR: {codigosplit[0]}')
print(f'EN TOP: {stack[0]}')

print()


n = 1


auxpaso = ''

auxid = ''


codigosplit2 = codigosplit.copy()

type = ''

stop = False

while len(stack) > 0 and stop == False:
    print(f'\n{n} ------------------------------------------\n')
    print(auxpaso)
    #print(auxid)
    #print(f'TYPE: {type}')

    for k,v in find_identifiers_and_literals(codigosplit2[0]).items():
        if len(v) > 0:
            if k == 'identifiers':
                auxid = v

    #print(find_identifiers_and_literals(codigosplit[0]))

    for k,v in find_identifiers_and_literals(codigosplit[0]).items():
        if len(v) > 0:
            #print(f'{k} : {v}')
            if k == 'identifiers':
                #print(f'K: {k}')
                codigosplit[0] = 'identifier'
                if auxpaso == 'DECLARE':
                    if v not in symbol_table:
                        symbol_table.append({"var": v})

            elif k == 'strings':
                codigosplit[0] = 'string'
                #print('Valor encontrado: STRING')

                if type == 'string' or type == 'char':
                    print(f'{codigosplit2[0]} es un tipo correcto para el tipo: {type}')
                else:
                    print('----------------SEMANTIC ERROR------------------')
                    print(f'{codigosplit2[0]} es de tipo string o char cuando debería ser tipo: {type}\n')
                    stop = True

                if auxpaso == 'ASSING' and stop == False:
                    print(f'LISTA DE SIMBOLOS ---------')
                    for s in range(len(symbol_table)):
                        print(symbol_table[s])
                        if auxid == symbol_table[s].get('var'):
                            symbol_table[s].update({'value': codigosplit2[0]})

            ########
            elif k == 'integers':
                codigosplit[0] = 'number'
                #print('-----------------------INTEGER')

                if type == 'integer':
                    print(f'{codigosplit2[0]} es un tipo correcto para el tipo: {type}')
                else:
                    print('----------------SEMANTIC ERROR------------------')
                    print(f'{codigosplit2[0]} es de tipo integer cuando debería ser tipo: {type}\n')
                    stop = True

                if auxpaso == 'ASSING' and stop == False:
                    print(f'LISTA DE SIMBOLOS ---------')
                    for s in range(len(symbol_table)):
                        print(symbol_table[s])
                        if auxid == symbol_table[s].get('var'):
                            symbol_table[s].update({'value': codigosplit2[0]})



            elif k == 'booleans':
                if auxpaso == 'ASSING':
                    #codigosplit[0] = 'string'
                    #print('-----------------------BOOLEAN')

                    if type == 'bool':
                        print(f'{codigosplit2[0]} es un tipo correcto para el tipo: {type}')
                    else:
                        print('----------------SEMANTIC ERROR------------------')
                        print(f'{codigosplit2[0]} es de tipo bool cuando debería ser tipo: {type}\n')
                        stop = True

                if auxpaso == 'ASSING' and stop == False:
                    print(f'LISTA DE SIMBOLOS ---------')
                    for s in range(len(symbol_table)):
                        print(symbol_table[s])
                        if auxid == symbol_table[s].get('var'):
                            symbol_table[s].update({'value': codigosplit2[0]})

            elif k == 'decimals':
                codigosplit[0] = 'number'
                #print('-----------------------DECIMAL')

                if type == 'decimal':
                    print(f'{codigosplit2[0]} es un tipo correcto para el tipo: {type}')
                else:
                    print('----------------SEMANTIC ERROR------------------')
                    print(f'{codigosplit2[0]} es de tipo decimal cuando debería ser tipo: {type}\n')
                    stop = True

                if auxpaso == 'ASSING' and stop == False:
                    print(f'LISTA DE SIMBOLOS ---------')
                    for s in range(len(symbol_table)):
                        print(symbol_table[s])
                        if auxid == symbol_table[s].get('var'):
                            symbol_table[s].update({'value': codigosplit2[0]})

            #########



            # elif k == 'integers':
            #     codigosplit[0] = 'number'
            #     if auxpaso == 'ASSING':
            #         print(f'LISTA 2---------- {codigosplit2[0]}')
            #         for s in range(len(symbol_table)):
            #             print(symbol_table[s])
            #             if auxid == symbol_table[s].get('var'):
            #                 symbol_table[s].update({'value': codigosplit2[0]})




                            # if codigosplit2[0] in idlit['integers'] or codigosplit2[0] in idlit['decimals']:
                            #     if type == 'integer' or type == 'decimal':
                            #         print('INTEGER')
                            #     else:
                            #         print('----------------SEMANTIC ERROR------------------')
                            #         print(f'{codigosplit2[0]} es de tipo integer cuando debería ser tipo {type}')
                            # elif codigosplit2[0] in idlit['strings']:
                            #     if type == 'string' or type == 'char':
                            #         print('STRING')
                            #     else:
                            #         print('----------------SEMANTIC ERROR------------------')
                            #         print(f'{codigosplit2[0]} es de tipo string cuando debería ser tipo {type}')
                            # elif codigosplit2[0] in idlit['booleans']:
                            #     if type == 'boolean':
                            #         print('BOOLEAN')
                            #     else:
                            #         print('----------------SEMANTIC ERROR------------------')
                            #         print(f'{codigosplit2[0]} es de tipo boolean cuando debería ser tipo {type}')


            elif k == 'types':
                if auxpaso == 'TYPES':
                    for s in range(len(symbol_table)):
                        symbol_table[s].update({'type': v})
                        type = str(v[0])


    if stack[0] == codigosplit[0]:
        print(f'TERMINAL')

        print('STACK:')
        print(stack)
        print('CODIGO ACTUAL:')
        print(codigosplit)
        print(codigosplit2)

        print(f'Stack POP: {stack.pop(0)}')
        print(f'Codigo POP: {codigosplit.pop(0)}')
        codigosplit2.pop(0)

    else:
        if stack[0] in non_terminals:
            print(f'NON TERMINAL')

            print('STACK TOP: ', stack[0])
            print('CODE TOP: ', codigosplit[0])

            if 'DECLARE' == stack[0]:
                auxpaso = 'DECLARE'
            if 'MAIN' == stack[0]:
                auxpaso = 'MAIN'
            if 'TYPES' == stack[0]:
                auxpaso = 'TYPES'
            if 'ASSING' == stack[0]:
                auxpaso = 'ASSING'

            aux = pretable_dict[stack[0]][codigosplit[0]]

            #print(f'Aux out: {aux}')

            aux = str(aux)

            if aux.isdigit():
                aux = int(aux)

            if isinstance(aux, (int, float)):
                #print('NUMBER')
                #print(aux)
                #stack.pop(0)
                print(f'Stack POP: {stack.pop(0)}')
                #print(productions[aux])

                prorev = []

                cf = 0
                for e in productions[aux].split():
                    if cf > 1:
                        #print(e)
                        if e != 'ε':
                            prorev.append(e)
                    cf += 1

                #print()
                #print(stack)

                #print()
                #print(list(reversed(prorev)))

                for e in list(reversed(prorev)):
                    stack.insert(0, e)
                    print(f'Insertando en TOP: {e}')




                print('STACK:')
                print(stack)
                print('CODIGO ACTUAL:')
                print(codigosplit)
                print(codigosplit2)
            else:
                x = False
                for clave, valor in productions.items():
                    if 'ε' in valor:
                        if stack[0] in ('AUXEXS', 'AUXEXP', 'AUXTERM'):
                            #print('E')
                            x = True

                if x == True:
                    stack.pop(0)

                else:
                    print(f'ERROR INNER')
                    print('Syntax Error -------------------------------')
                    print(f"Se buscaba: '{stack[0]}', se econtro: '{codigosplit[0]}'")

                    print('STACK TOP: ', stack[0])
                    print('CODE TOP: ', codigosplit[0])
                    print('STACK:')
                    print(stack)
                    print('CODIGO ACTUAL:')
                    print(codigosplit)

                    break
        else:
            print('Syntax Error -------------------------------')
            print(f"Se buscaba: '{stack[0]}', se econtro: '{codigosplit[0]}'")

            print('STACK TOP: ', stack[0])
            print('CODE TOP: ', codigosplit[0])
            print('STACK:')
            print(stack)
            print('CODIGO ACTUAL:')
            print(codigosplit)

            break
    n = n + 1
    #time.sleep(0.1)



print()

idc = 0

print('--------------------- SYMBOL TABLE ----------------------------')


for id in range(len(symbol_table)):
    print(symbol_table[id])





