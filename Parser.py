from scanner import Escaner

class Parser:
    def __init__(self, escaner):
        self.escaner = escaner
        self.token_actual = self.escaner.siguiente_token()  # Obtener el primer token

    def parse(self):
        # Iniciar el análisis sintáctico a partir del nodo raíz
        self.program()

    def program(self):
        self.declaration_list()

    def declaration_list(self):
        while self.token_actual.type in ['PALABRA_CLAVE', 'IDENTIFICADOR']:
            self.declaration()

    def declaration(self):
        if self.token_actual.type in ['PALABRA_CLAVE']:
            self.function_declaration()  # Se considera que las funciones son las declaraciones válidas
        elif self.token_actual.type == 'IDENTIFICADOR':
            self.variable_declaration()  # Se asume que es una declaración de variable
        else:
            self.error("Declaración esperada")

    def function_declaration(self):
        # Analiza una declaración de función
        self.match('PALABRA_CLAVE')  # Tipo
        self.match('IDENTIFICADOR')    # Identificador
        self.match('DELIMITADOR')      # '('
        self.parameters()               # Parámetros
        self.match('DELIMITADOR')      # ')'
        self.block()                   # Bloque

    def variable_declaration(self):
        # Analiza una declaración de variable
        self.match('PALABRA_CLAVE')  # Tipo
        self.match('IDENTIFICADOR')    # Identificador
        self.match('DELIMITADOR')      # ';'

    def parameters(self):
        if self.token_actual.type != 'DELIMITADOR':
            self.parameter_list()

    def parameter_list(self):
        self.parameter()
        while self.token_actual.type == 'DELIMITADOR':
            self.match('DELIMITADOR')  # ','
            self.parameter()

    def parameter(self):
        self.match('PALABRA_CLAVE')  # Tipo
        self.match('IDENTIFICADOR')    # Identificador

    def block(self):
        self.match('DELIMITADOR')  # '{'
        self.statement_list()
        self.match('DELIMITADOR')  # '}'

    def statement_list(self):
        while self.token_actual.type in ['DELIMITADOR', 'PALABRA_CLAVE', 'IDENTIFICADOR']:
            self.statement()

    def statement(self):
        if self.token_actual.type == 'DELIMITADOR':  # Bloque
            self.block()
        elif self.token_actual.type in ['PALABRA_CLAVE', 'IDENTIFICADOR']:  # Expresión
            self.expression_statement()

    def expression_statement(self):
        if self.token_actual.type in ['PALABRA_CLAVE', 'IDENTIFICADOR']:
            self.match('IDENTIFICADOR')  # Expresión
        self.match('DELIMITADOR')  # ';'

    def match(self, token_type):
        if self.token_actual.type == token_type:
            self.token_actual = self.escaner.siguiente_token()
        else:
            self.error(f"Se esperaba el token {token_type} pero se encontró {self.token_actual.type}")

    def error(self, mensaje):
        print(f"Error de análisis: {mensaje}")




if __name__ == "__main__":
    ruta_archivo = 'masmas.txt'
    escaner = Escaner('masmas.txt')
    while True:
        token = escaner.siguiente_token()
        if token.type == 'EOF':
            break
        print(token)

    # Iniciar el parser
    parser = Parser(escaner)
    parser.parse()  
