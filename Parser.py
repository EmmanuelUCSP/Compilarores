class Parser:
    def __init__(self, escaner):
        self.escaner = escaner
        self.token_actual = self.escaner.get_next_token()

    def consumir(self, tipo_token):
        """Consume el token actual y obtiene el siguiente."""
        if self.token_actual.type == tipo_token:
            self.token_actual = self.escaner.get_next_token()
        else:
            self.error(f"Se esperaba token de tipo '{tipo_token}', pero se encontró '{self.token_actual.type}'")

    def error(self, mensaje):
        """Maneja los errores de análisis."""
        print(f"Error: {mensaje}")
        raise Exception(mensaje)

    def parse(self):
        """Inicia el análisis sintáctico."""
        return self.program()

    def program(self):
        """Program ::= DeclarationList"""
        return self.declaration_list()

    def declaration_list(self):
        """DeclarationList ::= Declaration DeclarationList | ε"""
        declaraciones = []
        while self.token_actual.type in ['FUNCTION', 'VARIABLE']:  # Aquí se deben definir los tipos de tokens correspondientes
            declaraciones.append(self.declaration())
        return declaraciones

    def declaration(self):
        """Declaration ::= FunctionDeclaration | VariableDeclaration"""
        if self.token_actual.type == 'FUNCTION':
            return self.function_declaration()
        elif self.token_current.type == 'VARIABLE':
            return self.variable_declaration()
        else:
            self.error(f"Se esperaba FUNCTION o VARIABLE, pero se encontró '{self.token_actual.type}'")

    def function_declaration(self):
        """FunctionDeclaration ::= Type Identifier '(' Parameters ')' Block"""
        tipo = self.token_actual.value
        self.consumir('TYPE')  # Se espera un tipo
        nombre = self.token_actual.value
        self.consumir('IDENTIFICADOR')  # Se espera un identificador
        self.consumir('OPEN_PAR')  # Se espera '('
        parametros = self.parameters()
        self.consumir('CLOSE_PAR')  # Se espera ')'
        bloque = self.block()
        return {'tipo': 'FunctionDeclaration', 'tipo_retorno': tipo, 'nombre': nombre, 'parametros': parametros, 'bloque': bloque}

    def variable_declaration(self):
        """VariableDeclaration ::= Type Identifier ';'"""
        tipo = self.token_actual.value
        self.consumir('TYPE')  # Se espera un tipo
        nombre = self.token_actual.value
        self.consumir('IDENTIFICADOR')  # Se espera un identificador
        self.consumir('SEMICOLON')  # Se espera ';'
        return {'tipo': 'VariableDeclaration', 'tipo': tipo, 'nombre': nombre}

    def parameters(self):
        """Parameters ::= ParameterList | ε"""
        if self.token_actual.type == 'IDENTIFICADOR':
            return self.parameter_list()
        return []  # ε

    def parameter_list(self):
        """ParameterList ::= Parameter (',' Parameter)*"""
        parametros = [self.parameter()]
        while self.token_actual.type == 'COMMA':
            self.consumir('COMMA')
            parametros.append(self.parameter())
        return parametros

    def parameter(self):
        """Parameter ::= Type Identifier"""
        tipo = self.token_actual.value
        self.consumir('TYPE')  # Se espera un tipo
        nombre = self.token_actual.value
        self.consumir('IDENTIFICADOR')  # Se espera un identificador
        return {'tipo': 'Parameter', 'tipo': tipo, 'nombre': nombre}

    def block(self):
        """Block ::= '{' StatementList '}'"""
        self.consumir('OPEN_BRACE')  # Se espera '{'
        statements = self.statement_list()
        self.consumir('CLOSE_BRACE')  # Se espera '}'
        return statements

    def statement_list(self):
        """StatementList ::= Statement StatementList | ε"""
        statements = []
        while self.token_actual.type != 'CLOSE_BRACE':
            statements.append(self.statement())
        return statements

    def statement(self):
        """Statement ::= Block | ExpressionStatement | IfStatement | WhileStatement | ReturnStatement | PrintStatement"""
        if self.token_current.type == 'BLOCK':
            return self.block()
        # Aquí deberías implementar el resto de las declaraciones
        # como ExpressionStatement, IfStatement, WhileStatement, etc.

    # Aquí debes implementar las demás funciones para manejar las declaraciones
    # como ExpressionStatement, IfStatement, WhileStatement, ReturnStatement, PrintStatement, y Expression.

# Ejemplo de uso
if __name__ == "__main__":
    ruta_archivo = 'masmas.txt'  # Reemplaza con la ruta de tu archivo
    escaner = Escaner(ruta_archivo)
    parser = Parser(escaner)
    try:
        resultado = parser.parse()
        print("Análisis completado con éxito:")
        print(resultado)
    except Exception as e:
        print(e)
