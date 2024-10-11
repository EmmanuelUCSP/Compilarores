class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Lista de tokens obtenida del scanner
        self.posicion = 0
        self.token_actual = self.tokens[self.posicion] if self.tokens else None

    def avanzar(self):
        """Avanza al siguiente token y actualiza el token actual."""
        self.posicion += 1
        self.token_actual = self.tokens[self.posicion] if self.posicion < len(self.tokens) else None

    def coincidir(self, tipo_token):
        """Consume el token actual si coincide con el tipo dado."""
        if self.token_actual and self.token_actual[0] == tipo_token:
            self.avanzar()  # Avanza solo si coincide
            return True
        return False

    def error(self, mensaje):
        """Maneja errores de parseo."""
        print(f"Error: {mensaje} en el token {self.token_actual}")
        raise Exception(mensaje)

    # Aquí irían las demás funciones del parser (variable_declaration, assignment_expression, etc.)

# Uso del scanner y parser juntos
ruta_archivo = 'masmas.txt'
escaner = Escaner(ruta_archivo)
escaner.escanear()  # Esto generará los tokens

# Asumiendo que tienes una lista de tokens generada
tokens = escaner.tokens  # Asegúrate de que tu escáner almacene los tokens generados
parser = Parser(tokens)  # Inicializa el parser con los tokens
parser.program()  # Comienza el análisis sintáctico
