from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: any
    line: int
    column: int

class Escaner:
    def __init__(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r') as archivo:
                self.datos_entrada = archivo.read()
        except FileNotFoundError:
            print(f"Error: El archivo '{ruta_archivo}' no se encontró.")
            self.datos_entrada = ""
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.contador_errores = 0
        self.tokens_generador = self.escanear()
        self.buffer = []

    def obtener_caracter(self):
        """Obtiene el siguiente carácter y avanza el puntero."""
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
        """Mira el siguiente carácter sin mover el puntero."""
        if self.posicion < len(self.datos_entrada):
            return self.datos_entrada[self.posicion]
        return None
    
    def saltar_espacios(self):
        """Salta espacios en blanco y comentarios."""
        while True:
            caracter = self.ver_caracter()
            if caracter in [' ', '\t', '\n']:
                self.obtener_caracter()  # Consumir espacio en blanco
            elif caracter == '/' or caracter == '#':  # Posible comentario
                manejado = self.manejar_comentario_o_division()
                if manejado == ('OPERADOR', '/'):
                    # Retornar el operador de división como un token
                    return Token('OPERADOR', '/', self.linea, self.columna - 1)
            else:
                break
    
    def manejar_comentario_o_division(self):
        """Maneja comentarios estilo C, C++ o el operador de división."""
        caracter = self.obtener_caracter()
        if caracter == '/':
            siguiente_caracter = self.ver_caracter()
            if siguiente_caracter == '/':  # Comentario C++
                self.obtener_caracter()  # Consumir segundo '/'
                while self.obtener_caracter() != '\n':
                    if self.ver_caracter() is None:
                        break
            elif siguiente_caracter == '*':  # Comentario C
                self.obtener_caracter()  # Consumir '*'
                while True:
                    caracter = self.obtener_caracter()
                    if caracter is None:
                        print(f"Error: Comentario sin cerrar en la línea {self.linea}, columna {self.columna}")
                        self.contador_errores += 1
                        return
                    if caracter == '*' and self.ver_caracter() == '/':
                        self.obtener_caracter()  # Consumir '/'
                        break
            else:
                # Es el operador de división
                return ('OPERADOR', '/')
        elif caracter == '#':  # Comentario Python
            while self.obtener_caracter() != '\n':
                if self.ver_caracter() is None:
                    break
    
    def obtener_token(self):
        """Identifica y retorna el siguiente token válido."""
        salto = self.saltar_espacios()
        if isinstance(salto, Token):
            return salto  # Retornar el operador de división
        
        columna_inicial = self.columna  # Guardar la columna inicial
        caracter = self.obtener_caracter()
        
        if caracter is None:
            return Token('EOF', None, self.linea, self.columna)
        
        # Identificadores y palabras clave
        if caracter.isalpha() or caracter == '_':
            return self.manejar_identificador_o_palabra_clave(caracter, columna_inicial)
        
        # Números enteros
        if caracter.isdigit():
            return self.manejar_entero(caracter, columna_inicial)
        
        # Caracteres
        if caracter == "'":
            return self.manejar_caracter(columna_inicial)
    
        # Cadenas
        if caracter == '"':
            return self.manejar_cadena(columna_inicial)
    
        # Operadores y delimitadores adicionales
        if caracter in [':', '{', '}', '[', ']', ',', ';', '>', '<', '=', '+', '-', '*', '/', '$', '%', '^', '!', '&', '|']:
            token = self.manejar_operador_o_delimitador(caracter, columna_inicial)
            if token:
                return token
    
        # Error léxico
        print(f"DEBUG SCAN - Error léxico: carácter inesperado '{caracter}' en línea {self.linea}, columna {self.columna}")
        self.contador_errores += 1
        return self.obtener_token()  # Continuar después del error
    
    def manejar_identificador_o_palabra_clave(self, caracter, columna_inicial):
        """Procesa un identificador o palabra clave."""
        identificador = caracter
        while self.ver_caracter() is not None and (self.ver_caracter().isalnum() or self.ver_caracter() == '_'):
            identificador += self.obtener_caracter()
        
        palabras_clave = ['array', 'boolean', 'char', 'else', 'false', 'for', 'function', 'if', 'integer', 'print', 'return', 'string', 'true', 'void', 'while']
        if identificador in palabras_clave:
            token = Token('PALABRA_CLAVE', identificador, self.linea, columna_inicial)
            print(f"DEBUG SCAN - PALABRA_CLAVE [ {identificador} ] encontrada en línea {self.linea}, columna {columna_inicial}")
            return token
        else:
            token = Token('IDENTIFICADOR', identificador, self.linea, columna_inicial)
            print(f"DEBUG SCAN - IDENTIFICADOR [ {identificador} ] encontrado en línea {self.linea}, columna {columna_inicial}")
            return token
    
    def manejar_entero(self, caracter, columna_inicial):
        """Procesa un número entero."""
        numero = caracter
        while self.ver_caracter() is not None and self.ver_caracter().isdigit():
            numero += self.obtener_caracter()
        
        # Evitar casos 123abc
        if self.ver_caracter() is not None and self.ver_caracter().isalpha():
            print(f"DEBUG SCAN - Error léxico: número inválido '{numero}{self.ver_caracter()}' en línea {self.linea}, columna {self.columna}")
            self.contador_errores += 1
            while self.ver_caracter() is not None and self.ver_caracter().isalnum():
                self.obtener_caracter()  # Consumir caracteres inválidos
            return self.obtener_token()  # Continuar después del error
        token = Token('ENTERO', int(numero), self.linea, columna_inicial)
        print(f"DEBUG SCAN - ENTERO [ {numero} ] encontrado en línea {self.linea}, columna {columna_inicial}")
        return token
    
    def manejar_caracter(self, columna_inicial):
        """Procesa un carácter entre comillas simples."""
        caracter = self.obtener_caracter()  # Obtener el carácter dentro de las comillas simples
        if self.obtener_caracter() != "'":
            print(f"DEBUG SCAN - Error: Carácter no cerrado en línea {self.linea}, columna {self.columna}")
            self.contador_errores += 1
            return Token('ERROR', 'CHAR_NOT_CLOSED', self.linea, columna_inicial)
        token = Token('CHAR', caracter, self.linea, columna_inicial)
        print(f"DEBUG SCAN - CHAR [ '{caracter}' ] encontrado en línea {self.linea}, columna {columna_inicial}")
        return token
    
    def manejar_cadena(self, columna_inicial):
        """Procesa una cadena entre comillas dobles."""
        cadena = ''
        while True:
            caracter = self.obtener_caracter()
            if caracter == '"':  # Final de la cadena
                break
            if caracter is None or caracter == '\n':
                print(f"DEBUG SCAN - Error: Cadena no cerrada en línea {self.linea}, columna {self.columna}")
                self.contador_errores += 1
                return Token('ERROR', 'STRING_NOT_CLOSED', self.linea, columna_inicial)
            cadena += caracter
        token = Token('STRING', cadena, self.linea, columna_inicial)
        print(f"DEBUG SCAN - STRING [ \"{cadena}\" ] encontrada en línea {self.linea}, columna {columna_inicial}")
        return token
    
    def manejar_operador_o_delimitador(self, caracter, columna_inicial):
        """Procesa operadores y delimitadores."""
        siguiente_caracter = self.ver_caracter()

        # Operadores &&, ||, >=, <=, ==, !=
        if caracter == '&':
            if siguiente_caracter == '&':
                self.obtener_caracter()  # Consumir el segundo '&'
                token = Token('AND_OP', '&&', self.linea, columna_inicial)
                print(f"DEBUG SCAN - AND_OP [ && ] encontrada en línea {self.linea}, columna {columna_inicial}")
                return token
        elif caracter == '|':
            if siguiente_caracter == '|':
                self.obtener_caracter()  # Consumir el segundo '|'
                token = Token('OR_OP', '||', self.linea, columna_inicial)
                print(f"DEBUG SCAN - OR_OP [ || ] encontrada en línea {self.linea}, columna {columna_inicial}")
                return token
        elif caracter == '>':
            if siguiente_caracter == '=':
                self.obtener_caracter()  # Consumir '='
                token = Token('GTE_OP', '>=', self.linea, columna_inicial)
                print(f"DEBUG SCAN - GTE_OP [ >= ] encontrada en línea {self.linea}, columna {columna_inicial}")
                return token
        elif caracter == '<':
            if siguiente_caracter == '=':
                self.obtener_caracter()  # Consumir '='
                token = Token('LTE_OP', '<=', self.linea, columna_inicial)
                print(f"DEBUG SCAN - LTE_OP [ <= ] encontrada en línea {self.linea}, columna {columna_inicial}")
                return token
        elif caracter == '=':
            if siguiente_caracter == '=':
                self.obtener_caracter()  # Consumir '='
                token = Token('EQUAL_OP', '==', self.linea, columna_inicial)
                print(f"DEBUG SCAN - EQUAL_OP [ == ] encontrada en línea {self.linea}, columna {columna_inicial}")
                return token
        elif caracter == '!':
            if siguiente_caracter == '=':
                self.obtener_caracter()  # Consumir '='
                token = Token('NOT_EQUAL_OP', '!=', self.linea, columna_inicial)
                print(f"DEBUG SCAN - NOT_EQUAL_OP [ != ] encontrada en línea {self.linea}, columna {columna_inicial}")
                return token
        
        token = Token('DELIMITADOR', caracter, self.linea, columna_inicial)
        print(f"DEBUG SCAN - DELIMITADOR [ {caracter} ] encontrado en línea {self.linea}, columna {columna_inicial}")
        return token

    def escanear(self):
        """Generador de tokens que escanea la entrada."""
        while True:
            token = self.obtener_token()
            if token.type == 'EOF':
                yield token
                break
            yield token
    
    def siguiente_token(self):
        """Devuelve el siguiente token del generador."""
        try:
            return next(self.tokens_generador)
        except StopIteration:
            return Token('EOF', None, self.linea, self.columna)

    def obtener_todos_los_tokens(self):
        """Devuelve todos los tokens generados hasta el momento."""
        return list(self.tokens_generador)

# Ejemplo de uso
if __name__ == "__main__":
    escaner = Escaner('ruta_al_archivo.txt')
    while True:
        token = escaner.siguiente_token()
        if token.type == 'EOF':
            break
        print(token)
