class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0
        self.token_actual = self.tokens[self.posicion] if self.tokens else None

    def avanzar(self):
        """Avanza al siguiente token en la lista."""
        self.posicion += 1
        if self.posicion < len(self.tokens):
            self.token_actual = self.tokens[self.posicion]
        else:
            self.token_actual = None

    def coincidir(self, tipo):
        """Verifica si el token actual coincide con el tipo esperado y avanza."""
        if self.token_actual and self.token_actual[0] == tipo:
            self.avanzar()
            return True
        else:
            return False

    def error(self, mensaje):
        """Muestra un mensaje de error sintáctico."""
        raise Exception(f"Error sintáctico: {mensaje} en el token {self.token_actual}")

    def parse(self):
        """Inicia el análisis sintáctico desde el símbolo inicial de la gramática."""
        self.program()
        if self.token_actual is not None:
            self.error("Se esperaban más tokens al final del análisis")

    def program(self):
        """Regla: Program -> Declaration Program | ε"""
        while self.token_actual is not None:
            self.declaration()

    def declaration(self):
        """Regla: Declaration -> FunctionDeclaration | VariableDeclaration"""
        if self.token_actual[0] in ['PALABRA_CLAVE']:  # Las funciones y variables comienzan con un tipo
            if self.tokens[self.posicion + 1][0] == 'IDENTIFICADOR':
                # Necesitamos verificar si es una declaración de función o variable
                if self.tokens[self.posicion + 2][1] == '(':  # Función
                    self.function_declaration()
                else:  # Variable
                    self.variable_declaration()
            else:
                self.error("Se esperaba un identificador después del tipo")
        else:
            self.error("Declaración inválida")

    def function_declaration(self):
        """Regla: FunctionDeclaration -> Type Identifier ( Parameters ) Block"""
        self.type()
        if not self.coincidir('IDENTIFICADOR'):
            self.error("Se esperaba un identificador después del tipo en la declaración de función")
        if not self.coincidir('DELIM') or self.token_actual[1] != '(':
            self.error("Se esperaba '(' después del identificador en la declaración de función")
        self.parameters()
        if not self.coincidir('DELIM') or self.token_actual[1] != ')':
            self.error("Se esperaba ')' después de los parámetros en la declaración de función")
        self.block()

    def variable_declaration(self):
        """Regla: VariableDeclaration -> Type Identifier ;"""
        self.type()
        if not self.coincidir('IDENTIFICADOR'):
            self.error("Se esperaba un identificador en la declaración de variable")
        if not self.coincidir('DELIM') or self.token_actual[1] != ';':
            self.error("Se esperaba ';' al final de la declaración de variable")

    def type(self):
        """Regla: Type -> integer | boolean | char | string | void"""
        if not self.coincidir('PALABRA_CLAVE'):
            self.error("Se esperaba un tipo de dato (integer, boolean, char, string, void)")

    def parameters(self):
        """Regla: Parameters -> ParameterList | ε"""
        if self.token_actual and self.token_actual[0] == 'PALABRA_CLAVE':
            self.parameter_list()

    def parameter_list(self):
        """Regla: ParameterList -> Type Identifier | Type Identifier , ParameterList"""
        self.type()
        if not self.coincidir('IDENTIFICADOR'):
            self.error("Se esperaba un identificador en la lista de parámetros")
        while self.token_actual and self.token_actual[1] == ',':
            self.avanzar()
            self.type()
            if not self.coincidir('IDENTIFICADOR'):
                self.error("Se esperaba un identificador en la lista de parámetros")

    def block(self):
        """Regla: Block -> { StatementList }"""
        if not self.coincidir('DELIM') or self.token_actual[1] != '{':
            self.error("Se esperaba '{' para iniciar un bloque")
        self.statement_list()
        if not self.coincidir('DELIM') or self.token_actual[1] != '}':
            self.error("Se esperaba '}' para cerrar un bloque")

    def statement_list(self):
        """Regla: StatementList -> Statement StatementList | ε"""
        while self.token_actual and self.token_actual[0] in ['IDENTIFICADOR', 'PALABRA_CLAVE', 'DELIM']:
            self.statement()

    def statement(self):
        """Regla: Statement -> Block | ExpressionStatement | IfStatement | WhileStatement | ReturnStatement | PrintStatement"""
        if self.token_actual[1] == '{':
            self.block()
        elif self.token_actual[0] == 'PALABRA_CLAVE':
            # Aquí llamarías a funciones para las otras reglas como IfStatement, WhileStatement, etc.
            pass
        else:
            self.expression_statement()
