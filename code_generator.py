import sys
import time
from lexer import LexicalAnalyzer, TokenType
from parser import SyntacticAnalyzer

class CodeGenerator:
    def __init__(self):
        self.label_count = 0
        self.string_count = 0
        self.data_section = []
        self.text_section = []
        self.variables = {'a': 10, 'b': 5}  # Initial values for testing

    def generate_label(self):
        """Generates a unique label."""
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def generate_string_label(self):
        """Generates a label for a string."""
        label = f"str_{self.string_count}"
        self.string_count += 1
        return label

    def generate(self, statements):
        """Generates the assembly code."""
        print("Starting code generation")  # Debug
        self.data_section.append(".data")
        for var, value in self.variables.items():
            self.data_section.append(f"    {var}: .word {value}")
        self.data_section.append(f"    resultado: .word 0")

        self.text_section.append(".text")
        self.text_section.append(".global _start")
        self.text_section.append("_start:")

        # Print "Iniciando programa"
        str_label = self.generate_string_label()
        self.data_section.append(f"    {str_label}: .ascii \"Iniciando programa\\n\"")
        self.data_section.append(f"    len_{str_label} = . - {str_label}")
        self.text_section.append(f"    @ Imprimir string: Iniciando programa")
        self.text_section.append(f"    MOV R7, #4        @ syscall write")
        self.text_section.append(f"    MOV R0, #1        @ stdout")
        self.text_section.append(f"    LDR R1, ={str_label} @ dirección del string")
        self.text_section.append(f"    MOV R2, #len_{str_label} @ longitud del string")
        self.text_section.append(f"    SWI 0             @ llamada al sistema")

        for statement in statements:
            print(f"Generating code for statement: {statement}")  # Debug
            if statement[0] == "assignment":
                self.generate_assignment(statement)
            elif statement[0] == "if":
                self.generate_if_statement(statement)
            elif statement[0] == "print":
                self.generate_print_statement(statement)
            elif statement[0] == "sentence":
                self.generate_sentence(statement)

        self.text_section.append(f"    @ Terminar programa")
        self.text_section.append(f"    MOV R7, #1       @ syscall exit")
        self.text_section.append(f"    MOV R0, #0       @ código de salida")
        self.text_section.append(f"    SWI 0            @ llamada al sistema")

        return "\n".join(self.data_section + [""] + self.text_section)

    def generate_sentence(self, statement):
        """Generates code for a sentence: <noun_phrase> <verb_phrase> ."""
        print("Generating sentence")  # Debug
        _, noun_phrase, verb_phrase = statement
        _, article, adjectives, noun = noun_phrase
        message = f"{article} {' '.join(adjectives)} {noun}" if adjectives else f"{article} {noun}"
        str_label = self.generate_string_label()
        self.data_section.append(f"    {str_label}: .ascii \"{message}\\n\"")
        self.data_section.append(f"    len_{str_label} = . - {str_label}")
        self.text_section.append(f"    @ Imprimir string: {message}")
        self.text_section.append(f"    MOV R7, #4        @ syscall write")
        self.text_section.append(f"    MOV R0, #1        @ stdout")
        self.text_section.append(f"    LDR R1, ={str_label} @ dirección del string")
        self.text_section.append(f"    MOV R2, #len_{str_label} @ longitud del string")
        self.text_section.append(f"    SWI 0             @ llamada al sistema")

        if verb_phrase[1]:
            _, verb, (_, prep, (_, article2, adjectives2, noun2)) = verb_phrase
            message2 = f"{verb} {prep} {article2} {' '.join(adjectives2)} {noun2}" if adjectives2 else f"{verb} {prep} {article2} {noun2}"
            str_label2 = self.generate_string_label()
            self.data_section.append(f"    {str_label2}: .ascii \"{message2}\\n\"")
            self.data_section.append(f"    len_{str_label2} = . - {str_label2}")
            self.text_section.append(f"    @ Imprimir string: {message2}")
            self.text_section.append(f"    MOV R7, #4        @ syscall write")
            self.text_section.append(f"    MOV R0, #1        @ stdout")
            self.text_section.append(f"    LDR R1, ={str_label2} @ dirección del string")
            self.text_section.append(f"    MOV R2, #len_{str_label2} @ longitud del string")
            self.text_section.append(f"    SWI 0             @ llamada al sistema")

    def generate_assignment(self, statement):
        """Generates code for an assignment: <identifier> = <identifier> <op> <identifier>"""
        print("Generating assignment")  # Debug
        _, target, left, op, right = statement
        str_label = self.generate_string_label()
        op_name = {"+": "Suma", "-": "Resta", "*": "Multiplicacion"}[op]
        self.data_section.append(f"    {str_label}: .ascii \"{op_name} completada\\n\"")
        self.data_section.append(f"    len_{str_label} = . - {str_label}")
        self.text_section.append(f"    @ {op_name}: {target} = {left} {op} {right}")
        self.text_section.append(f"    LDR R0, ={left}   @ Cargar dirección de {left}")
        self.text_section.append(f"    LDR R0, [R0]      @ Cargar valor de {left}")
        self.text_section.append(f"    LDR R1, ={right}  @ Cargar dirección de {right}")
        self.text_section.append(f"    LDR R1, [R1]      @ Cargar valor de {right}")
        if op == "+":
            self.text_section.append(f"    ADD R2, R0, R1    @ R2 = R0 + R1")
        elif op == "-":
            self.text_section.append(f"    SUB R2, R0, R1    @ R2 = R0 - R1")
        elif op == "*":
            self.text_section.append(f"    MUL R2, R0, R1    @ R2 = R0 * R1")
        self.text_section.append(f"    LDR R3, ={target} @ Dirección de {target}")
        self.text_section.append(f"    STR R2, [R3]      @ Guardar resultado en {target}")
        self.text_section.append(f"    @ Imprimir string: {op_name} completada")
        self.text_section.append(f"    MOV R7, #4        @ syscall write")
        self.text_section.append(f"    MOV R0, #1        @ stdout")
        self.text_section.append(f"    LDR R1, ={str_label} @ dirección del string")
        self.text_section.append(f"    MOV R2, #len_{str_label} @ longitud del string")
        self.text_section.append(f"    SWI 0             @ llamada al sistema")

    def generate_if_statement(self, statement):
        """Generates code for an if: if <identifier> <comp_op> <identifier> ( <print_statement> )"""
        print("Generating if statement")  # Debug
        _, left, comp_op, right, print_stmt = statement
        end_label = self.generate_label()
        else_label = self.generate_label()
        self.text_section.append(f"    @ if {left} {comp_op} {right}")
        self.text_section.append(f"    LDR R0, ={left}   @ Cargar dirección de {left}")
        self.text_section.append(f"    LDR R0, [R0]      @ Cargar valor de {left}")
        self.text_section.append(f"    LDR R1, ={right}  @ Cargar dirección de {right}")
        self.text_section.append(f"    LDR R1, [R1]      @ Cargar valor de {right}")
        self.text_section.append(f"    CMP R0, R1        @ Comparar R0 y R1")
        if comp_op == "<":
            self.text_section.append(f"    BGE {else_label}  @ Branch if Greater or Equal (negación de <)")
        elif comp_op == ">":
            self.text_section.append(f"    BLE {else_label}  @ Branch if Less or Equal (negación de >)")
        self.generate_print_statement(print_stmt)
        self.text_section.append(f"    B {end_label}     @ Saltar al final")
        self.text_section.append(f"{else_label}:")
        self.text_section.append(f"    @ else (vacío)")
        self.text_section.append(f"{end_label}:")

    def generate_print_statement(self, statement):
        """Generates code for print: print ( <string> )"""
        print("Generating print statement")  # Debug
        _, string = statement
        str_label = self.generate_string_label()
        self.data_section.append(f"    {str_label}: .ascii \"{string}\\n\"")
        self.data_section.append(f"    len_{str_label} = . - {str_label}")
        self.text_section.append(f"    @ Imprimir string: {string}")
        self.text_section.append(f"    MOV R7, #4        @ syscall write")
        self.text_section.append(f"    MOV R0, #1        @ stdout")
        self.text_section.append(f"    LDR R1, ={str_label} @ dirección del string")
        self.text_section.append(f"    MOV R2, #len_{str_label} @ longitud del string")
        self.text_section.append(f"    SWI 0             @ llamada al sistema")

def generate_sample1():
    """Generates the content of sample1.s."""
    print("Generating sample1.s")  # Debug
    return """\
.text
.global _start

_start:
    MOV R0, #15       @ Primer número
    MOV R1, #5        @ Segundo número

    ADD R2, R0, R1    @ R2 = 15 + 5 = 20
    SUB R3, R0, R1    @ R3 = 15 - 5 = 10

    CMP R2, R3
    BGT mayor
    BLT menor
    BEQ iguales

mayor:
    LDR R0, =msg_mayor
    BL print_string
    B fin

menor:
    LDR R0, =msg_menor
    BL print_string
    B fin

iguales:
    LDR R0, =msg_iguales
    BL print_string

fin:
    MOV R7, #1
    MOV R0, #0
    SWI 0

.data
msg_mayor: .asciz "Rama mayor ejecutada\\n"
msg_menor: .asciz "Rama menor ejecutada\\n"
msg_iguales: .asciz "Rama iguales ejecutada\\n"

.text
print_string:
    MOV R7, #4
    MOV R1, R0
    MOV R2, #100
    SWI 0
    BX LR
"""

def generate_sample2():
    """Generates the content of sample2.s."""
    print("Generating sample2.s")  # Debug
    return """\
.text
.global _start

_start:
    MOV R0, #5        @ Primer número
    MOV R1, #5        @ Segundo número

    ADD R2, R0, R1    @ R2 = 5 + 5 = 10
    SUB R3, R0, R1    @ R3 = 5 - 5 = 0

    CMP R2, R3
    BGT mayor
    BLT menor
    BEQ iguales

mayor:
    LDR R0, =msg_mayor
    BL print_string
    B fin

menor:
    LDR R0, =msg_menor
    BL print_string
    B fin

iguales:
    LDR R0, =msg_iguales
    BL print_string

fin:
    MOV R7, #1
    MOV R0, #0
    SWI 0

.data
msg_mayor: .asciz "Rama mayor ejecutada\\n"
msg_menor: .asciz "Rama menor ejecutada\\n"
msg_iguales: .asciz "Rama iguales ejecutada\\n"

.text
print_string:
    MOV R7, #4
    MOV R1, R0
    MOV R2, #100
    SWI 0
    BX LR
"""

def generate_sample3():
    """Generates the content of sample3.s."""
    print("Generating sample3.s")  # Debug
    return """\
.text
.global _start

_start:
    MOV R0, #3        @ Primer número
    MOV R1, #5        @ Segundo número

    ADD R2, R0, R1    @ R2 = 3 + 5 = 8
    SUB R3, R0, R1    @ R3 = 3 - 5 = -2

    CMP R2, R3
    BGT mayor
    BLT menor
    BEQ iguales

mayor:
    LDR R0, =msg_mayor
    BL print_string
    B fin

menor:
    LDR R0, =msg_menor
    BL print_string
    B fin

iguales:
    LDR R0, =msg_iguales
    BL print_string

fin:
    MOV R7, #1
    MOV R0, #0
    SWI 0

.data
msg_mayor: .asciz "Rama mayor ejecutada\\n"
msg_menor: .asciz "Rama menor ejecutada\\n"
msg_iguales: .asciz "Rama iguales ejecutada\\n"

.text
print_string:
    MOV R7, #4
    MOV R1, R0
    MOV R2, #100
    SWI 0
    BX LR
"""

def main():
    """Main function to run the analysis and code generation."""
    start_time = time.time()  # Measure start time
    input_program = """
    resultado = a + b
    if a<b (print("a es menor que b"))
    if a>b (print("a es mayor que b"))
    resultado = a * b
    resultado = a - b
    """

    try:
        # Lexical analysis
        print("Starting lexical analysis")  # Debug
        lexer = LexicalAnalyzer()
        tokens = lexer.tokenize(input_program)
        print("Tokens generados:", tokens)

        # Syntactic analysis
        print("Starting syntactic analysis")  # Debug
        parser = SyntacticAnalyzer(tokens)
        statements = parser.parse()

        # Code generation
        print("Starting code generation and file writing")  # Debug
        generator = CodeGenerator()
        code = generator.generate(statements)

        # Generate sample.s files
        print("Writing sample1.s")  # Debug
        with open("sample1.s", "w") as f:
            f.write(generate_sample1())
        print("Writing sample2.s")  # Debug
        with open("sample2.s", "w") as f:
            f.write(generate_sample2())
        print("Writing sample3.s")  # Debug
        with open("sample3.s", "w") as f:
            f.write(generate_sample3())
        print("Writing ejemplo_generado.s")  # Debug
        with open("ejemplo_generado.s", "w") as f:
            f.write(code)

        print("Código generado exitosamente")
        print("\nCódigo ensamblador generado:")
        print(code)

    except Exception as e:
        print(f"Error: {str(e)}")

    end_time = time.time()  # Measure end time
    print(f"Tiempo de ejecución: {(end_time - start_time) * 1000:.2f} ms")  # Debug

if __name__ == "__main__":
    main()
