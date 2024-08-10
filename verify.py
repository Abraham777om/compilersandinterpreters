import pandas as pd

# Ruta al archivo de Excel
file_path = 'tabla de verdad.xlsx'

global string
string = ''


archivo = open("res.txt", "w")

# Cargar los datos desde el archivo Excel
df = pd.read_excel(file_path, sheet_name='Hoja1')

# Convertir el DataFrame a un diccionario de transiciones usando iloc para evitar la advertencia
transitions = {}
for index, row in df.iterrows():
    state = row.iloc[0]  # Usar iloc para acceder al primer elemento
    transitions[state] = {}
    for symbol in df.columns[1:]:
        transitions[state][symbol] = row[symbol]


# Función para obtener la transición para un estado y un símbolo específico
def get_transition(state, symbol):
    return transitions.get(state, {}).get(symbol, 'Transición no encontrada')


# Función para identificar todas las transiciones de una palabra según sus símbolos y detectar errores de balanceo
def identify_transitions(word, initial_state):
    current_state = initial_state
    transitions_sequence = [(current_state, None)]
    stack = []  # Usaremos una pila para mantener el balance de llaves, paréntesis y corchetes

    i = 0
    while i < len(word):
        char = word[i]
        if char.isalpha():
            transition_key = 'A-Z a-z'
        elif char.isdigit():
            transition_key = '0-9'
        else:
            transition_key = char

        next_state = get_transition(current_state, transition_key)

        if next_state == 'Transición no encontrada' or next_state == 'false' and char != '}':
            print(f"No se encontró transición desde el estado '{current_state}' con el símbolo '{char}'")

            string += f"No se encontró transición desde el estado '{current_state}' con el símbolo '{char}'"

            #archivo.write(f"No se encontró transición desde el estado '{current_state}' con el símbolo '{char}'")
            return transitions_sequence

        # Manejo de llaves, paréntesis y corchetes como entidades individuales
        if char in '{[(':
            stack.append(char)
            transitions_sequence.append((next_state, char))
            current_state = next_state
            i += 1
            continue
        elif char in '}])':
            if not stack:
                print(f"Error: Símbolo de cierre '{char}' sin un símbolo de apertura correspondiente")


                string += f"Error: Símbolo de cierre '{char}' sin un símbolo de apertura correspondiente"

                return transitions_sequence
            top = stack.pop()
            if (top == '{' and char != '}') or (top == '[' and char != ']') or (top == '(' and char != ')'):
                print(f"Error: Desbalance de símbolos, se esperaba '{'{' if top == '{' else ('[' if top == '[' else '(')}' pero se encontró '{char}'")

                #string += f"Error: Desbalance de símbolos"

                return transitions_sequence
            transitions_sequence.append((next_state, char))
            current_state = next_state
            i += 1
            continue

        # Procesar el contenido dentro de delimitadores como palabras separadas
        if char in '{[(':
            closing_delim = '}' if char == '{' else (']' if char == '[' else ')')
            inner_content = ''
            i += 1
            while i < len(word) and word[i] != closing_delim:
                inner_content += word[i]
                i += 1
            if i == len(word):
                print(f"Error: Símbolo de cierre '{closing_delim}' faltante")

                string += f"Error: Símbolo de cierre '{closing_delim}' faltante"

                print("INNER CONTENT: ", inner_content)
                return transitions_sequence
            # Procesar cada subpalabra dentro del delimitador
            for subword in inner_content.split():
                sub_transitions_sequence = identify_transitions(subword, initial_state)
                transitions_sequence.extend(sub_transitions_sequence[1:])  # Omitir el estado inicial duplicado

            transitions_sequence.append((next_state, closing_delim))
            current_state = next_state
            i += 1
            continue


        transitions_sequence.append((next_state, char))
        current_state = next_state
        i += 1

    # Verificar si todos los símbolos de apertura han sido cerrados
    if stack:
        print("Error: Símbolo(s) de apertura sin cerrar:", stack)

        string += f"Error: Símbolo(s) de apertura sin cerrar:, {stack}"

    return transitions_sequence


palabras = []
palabra_actual = ''
dentro_simbolo = False

with open('ex', 'r') as file:
    contenido = file.read()

for caracter in contenido:
    if caracter.isspace() and not dentro_simbolo:
        palabras.append(palabra_actual)
        palabra_actual = ''
    elif caracter in ['{', '(', '[']:
        dentro_simbolo = True
        palabra_actual += caracter
    elif caracter in ['}', ')', ']']:
        dentro_simbolo = False
        palabra_actual += caracter
        palabras.append(palabra_actual)
        palabra_actual = ''
    else:
        palabra_actual += caracter

if palabra_actual:
    palabras.append(palabra_actual)

print("PALABRAS: ", palabras)

words = palabras


# Ejemplo de uso: identificar todas las transiciones de diferentes palabras comenzando desde el estado 'q0'

initial_state = 'q0'

first_char = ''

last_char = ''

list = []

del_words = []

dictionary = {}

key = ''

other_strings = []
non_delimiter_array = []

for word in words:
    if word[0] in ['{', '(', '[']:
        w = word
        print("WORD: ", w)
        delimiters = []
        key = ""
        for char in w:
            print("Char: ", char)
            if char in ['{', '(', '[']:
                delimiters.append(char)
            elif char in ['}', ')', ']']:
                print("Char2: ", char)
                delimiters.append(char)
                key = w
                #break
        if key:
            dictionary[key] = "".join(delimiters)
    else:
        other_strings.append(word)
        non_delimiter_parts = [part for part in word.split() if part not in ['{', '}', '(', ')', '[', ']']]
        non_delimiter_array.extend(non_delimiter_parts)



palabras_filtradas = []
delimiters = []





for palabra in del_words:
    palabra_filtrada = ''.join(char for char in palabra if char not in '{}()[]')
    delimiters.extend(char for char in palabra if char in '{}()[]')
    if palabra_filtrada:
        palabras_filtradas.append(palabra_filtrada)

print("Palabras sin delimitadores:", palabras_filtradas)
print("Delimitadores separados:", delimiters)

x = ''.join(delimiters)
words.append(x)

dictionary[key] = x

for e in palabras_filtradas:
    words.append(e)

for e in delimiters:
    words.append(e)



list2 = []



for word in words:
    print(f"\nPalabra: {word}")

    string += f"\nPalabra: {word}"
    transitions_sequence = identify_transitions(word, initial_state)
    # Imprimir la secuencia de transiciones
    print("Secuencia de transiciones:")

    string += "\nSecuencia de transiciones:"
    c = 0
    #print(word[-1])
    #last_char = word[-1]

    if word in dictionary:
        result = ''
        print("Word in dic: ", word)
        for char in word:
            if char not in '{}()[]':
                #print("Char in word: ", char)
                result += char
        print("Result:", result)
        list2 = result.split()

        for e in list2:
            words.append(e)

        for state, char in transitions_sequence:
            c += 1
            if char is None:
                print(f"Estado inicial: {state}")
                list.append(state)
            else:
                print(f"Con símbolo '{char}': {state}")

                string += f"\nCon símbolo '{char}': {state}"
                list.append(state)
                if (char == '{'):
                    first_char = char

        print(f"\n{list}\n")

        string += f"\n{list}\n"

    print(list2)





    for state, char in transitions_sequence:
        c += 1
        if char is None:
            print(f"Estado inicial: {state}")

            list.append(state)
        else:
            print(f"Con símbolo '{char}': {state}")
            string += f"\nCon símbolo '{char}': {state}"
            list.append(state)
            if (char == '{'):
                first_char = char

    print(f"\n{list}\n")


    if ('q0' and 'q1' and 'q2') in list:
        print("Identifier")
        string += f"\nIdentifier"

    elif ('q0' and 'q21' and 'q22' and 'q23' and 'q24') in list:
        print("Comments")
        string += f"\nComments"
    elif (('q0' and 'q25' and 'q26') in list) or (('q0' and 'q27' and 'q28') in list) or (('q0' and 'q29' and 'q30') in list):
        print("Delimiter {} () []")
        string += f"\nDelimiter"

    elif ('q0' and 'q31') in list:
        print("Delimiter")
        string += f"\nDelimiter"

    elif ('q0' and 'q3' and 'q4' and 'q5') in list:
        print("Decimal")
        string += f"\nDecimal"
    elif ('q0' and 'q3') in list:
        print("Integer")
        string += f"\nInteger"
    elif ('q0' and 'q6' and 'q7') in list:
        print("String")
        string += f"\nString"
    elif ('q0' and 'q8' and 'q9') in list:
        print("Operator Assignment")
        string += f"\nOperator Assignment"

    elif ('q0' and 'q8') in list:
        print("Delimiter")
        string += f"\nDelimiter"

    elif (('q0' and 'q10' and 'q11') in list) or (('q0' and 'q12' and 'q13') in list):
        print("Operator Relational")
        string += f"\nOperator Relational"

    elif (('q0' and 'q10') in list) or (('q0' and 'q12' and 'q13') in list):
        print("Operator Relational")
        string += f"\nOperator Relational"
    elif ('q0' and 'q14') in list:
        print("Operator Arithmetic")
        string += f"\nOperator Arithetic"
    elif (('q0' and 'q15' and 'q16') in list) or (('q0' and 'q17' and 'q18') in list) or (('q0' and 'q19') in list):
        print("Operator Logic")
        string += f"\nOperator Logic"

    list.clear()

#print(first_char)
#print(last_char)




print("Del words: ", del_words)

print(delimiters)



print(dictionary)




print("\nRESULTS\n")
print(string)

archivo.write(string)