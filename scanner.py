class Escaner:
    def __init__(self, ruta_archivo):
        with open(ruta_archivo, 'r') as archivo:
            self.datos_entrada = archivo.read()
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.contador_errores = 0

    def obtener_caracter(self):
        """Obtiene el siguiente carácter y avanza el puntero"""
        if self.posicion < len(self.datos_entrada):
            caracter = self.datos_entrada[self.posicion]
            self.posicion += 1
            if caracter == '\n':
                self.linea += 1
                self.columna = 1
            else:
                self.columna += 1
            return caracter
        return None  # Fin del archivo

    def ver_caracter(self):
        """Mira el siguiente carácter sin mover el puntero"""
        if self.posicion < len(self.datos_entrada):
            return self.datos_entrada[self.posicion]
        return None

    def manejar_identificador_o_palabra_clave(self, caracter, columna_inicial):
        """Procesa un identificador o palabra clave"""
        identificador = caracter
        while self.ver_caracter() is not None and (self.ver_caracter().isalnum() or self.ver_caracter() == '_'):
            identificador += self.obtener_caracter()

        # Verificar si es una palabra clave reservada
        palabras_clave = ['array', 'boolean', 'char', 'else', 'false', 'for', 'function', 'if', 'integer', 'print', 'return', 'string', 'true', 'void', 'while']
        if identificador in palabras_clave:
            print(f"DEBUG SCAN - PRINT_KEY [ {identificador} ] found at ({self.linea}:{columna_inicial})")
            return ('PALABRA_CLAVE', identificador)
        else:
            print(f"DEBUG SCAN - ID [ {identificador} ] found at ({self.linea}:{columna_inicial})")
            return ('IDENTIFICADOR', identificador)

    def manejar_operador_o_delimitador(self, caracter, columna_inicial):
        """Procesa operadores y delimitadores"""
        siguiente_caracter = self.ver_caracter()

        # Manejar operadores dobles como &&, ||, >=, <=, ==, !=
        if caracter == '&':
            if siguiente_caracter == '&':
                self.obtener_caracter()  # Consumir el segundo '&'
                return ('AND_OP', '&&')
            else:
                self.contador_errores += 1
                return None

        elif caracter == '|':
            if siguiente_caracter == '|':
                self.obtener_caracter()  # Consumir el segundo '|'
                return ('OR_OP', '||')
            else:
                self.contador_errores += 1
                return None

        elif caracter == '>':
            if siguiente_caracter == '=':
                self.obtener_caracter()  # Consumir el '='
                return ('GE', '>=')
            else:
                return ('GT', '>')

        elif caracter == '<':
            if siguiente_caracter == '=':
                self.obtener_caracter()  # Consumir el '='
                return ('LE', '<=')
            else:
                return ('LT', '<')

        elif caracter == '=':
            if siguiente_caracter == '=':
                self.obtener_caracter()  # Consumir el '='
                return ('EQ', '==')
            else:
                return ('ASSIGN_OP', '=')

        elif caracter == '!':
            if siguiente_caracter == '=':
                self.obtener_caracter()  # Consumir el '='
                return ('NE', '!=')
            else:
                return ('NOT_OP', '!')

        # Operadores de un solo carácter
        operadores_y_delimitadores = {
            '+': 'ADD_OP',
            '-': 'SUB_OP',
            '*': 'MUL_OP',
            '/': 'DIV_OP',
            '%': 'MOD_OP',
            '^': 'EXP_OP',
            '!': 'NOT_OP',
            '=': 'ASSIGN_OP',
            '<': 'LT',
            '>': 'GT',
            '(': 'OPEN_PAR',
            ')': 'CLOSE_PAR',
            ';': 'SEMICOLON',
            '$': 'EOP',
            ':': 'COLON',
            '{': 'OPEN_BRACE',
            '}': 'CLOSE_BRACE',
            '[': 'OPEN_BRACKET',
            ']': 'CLOSE_BRACKET',
            ',': 'COMMA'
        }

        if caracter in operadores_y_delimitadores:
            return ('DELIM', caracter)

        # Si no es ninguno de los operadores o delimitadores esperados
        self.contador_errores += 1
        return None

    def obtener_token(self):
        """Identifica el siguiente token válido"""
        self.saltar_espacios()
        columna_inicial = self.columna  # Guardar la columna inicial
        caracter = self.obtener_caracter()

        if caracter is None:
            return None  # Fin del archivo

        # Identificadores y palabras clave
        if caracter.isalpha() or caracter == '_':  # Empieza con letra o '_'
            return self.manejar_identificador_o_palabra_clave(caracter, columna_inicial)

        # Números enteros
        if caracter.isdigit():
            return self.manejar_entero(caracter, columna_inicial)

        # Operadores y delimitadores
        return self.manejar_operador_o_delimitador(caracter, columna_inicial)

    def manejar_entero(self, caracter, columna_inicial):
        """Procesa un número entero"""
        numero = caracter
        while self.ver_caracter() and self.ver_caracter().isdigit():
            numero += self.obtener_caracter()
        return ('ENTERO', int(numero))

    def saltar_espacios(self):
        """Salta espacios en blanco y comentarios"""
        while True:
            caracter = self.ver_caracter()
            if caracter in [' ', '\t', '\n']:
                self.obtener_caracter()  # Consumir espacio en blanco
            elif caracter == '/':  # Posible comentario
                self.manejar_comentario()
            else:
                break

    def manejar_comentario(self):
        """Maneja comentarios estilo C y C++"""
        caracter = self.obtener_caracter()
        if caracter == '/':
            siguiente_caracter = self.ver_caracter()
            if siguiente_caracter == '/':  # Comentario de una línea estilo C++
                while self.obtener_caracter() != '\n':
                    continue  # Ignorar todo hasta el final de la línea
            elif siguiente_caracter == '*':  # Comentario de varias líneas estilo C
                self.obtener_caracter()  # Consumir '*'
                while True:
                    caracter = self.obtener_caracter()
                    if caracter == '*' and self.ver_caracter() == '/':
                        self.obtener_caracter()  # Consumir '/'
                        break
            else:
                print(f"Error: '/' inesperado en la línea {self.linea}, columna {self.columna}")

    def escanear(self):
        """Función principal para escanear todo el archivo"""
        print("INFO SCAN - Start scanning…")
        token = self.obtener_token()
        while token is not None:
            token = self.obtener_token()
        print(f"INFO SCAN - Completed with {self.contador_errores} errors")


# Ejemplo de uso
ruta_archivo = 'prueba.txt'  # Cambia el nombre del archivo aquí
escaner = Escaner(ruta_archivo)
escaner.escanear()
