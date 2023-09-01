from ProgramaEnPython import *

def test_indicesDirecciones():
    assert indicesDirecciones(0) == [0, 2]
    assert indicesDirecciones(1) == [0, 2, 4]
    assert indicesDirecciones(2) == [0, 1, 2, 3, 4, 5, 6, 7]
    assert indicesDirecciones(3) == [0, 1, 2, 3, 4, 5, 6, 7]

def test_posicionesConDireccion():
    assert posicionesConDireccion(2, 1) == [((0, 0), 0), ((0, 0), 2), ((0, 0), 4), ((0, 1), 0), ((0, 1), 2), ((0, 1), 4), ((1, 0), 0), ((1, 0), 2), ((1, 0), 4), ((1, 1), 0), ((1, 1), 2), ((1, 1), 4)]
    assert posicionesConDireccion(3, 0) == [((0, 0), 0), ((0, 0), 2), ((0, 1), 0), ((0, 1), 2), ((0, 2), 0), ((0, 2), 2), ((1, 0), 0), ((1, 0), 2), ((1, 1), 0), ((1, 1), 2), ((1, 2), 0), ((1, 2), 2), ((2, 0), 0), ((2, 0), 2), ((2, 1), 0), ((2, 1), 2), ((2, 2), 0), ((2, 2), 2)]

def test_direccionPlabra():
    assert direccionPlabra(0) == (1, 0)
    assert direccionPlabra(1) == (-1, 0)
    assert direccionPlabra(2) == (0, 1)
    assert direccionPlabra(3) == (0, -1)
    assert direccionPlabra(4) == (1, 1)
    assert direccionPlabra(5) == (1, -1)
    assert direccionPlabra(6) == (-1, 1)
    assert direccionPlabra(7) == (-1, -1)

def test_separaTupla():
    tupla_posicion_direccion = ((0, 3), 2)
    assert separaTupla(tupla_posicion_direccion, True) == 0
    assert separaTupla(tupla_posicion_direccion, False, True) == 3
    assert separaTupla(tupla_posicion_direccion, False, False, True) == 0
    assert separaTupla(tupla_posicion_direccion, False, False, False, True) == 1

def test_palabraEntraEnTablero():
    assert palabraEntraEnTablero(5, "lapiz", 0, 0, 1, 0) == True
    assert palabraEntraEnTablero(5, "lapiz", 1, 0, 1, 0) == False
    assert palabraEntraEnTablero(5, "celular", 0, 0, 1, 1) == False

def test_palabrasSuperpuestas():
    assert palabrasSuperpuestas(0) == False
    assert palabrasSuperpuestas(1) == False
    assert palabrasSuperpuestas(2) == False
    assert palabrasSuperpuestas(3) == True

def test_verificarTablero():
    tablero0 = [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]
    tablero1 = [
        ['S', 'O', 'L'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]
    assert verificarTablero(tablero0, "SOL", 0, 0, 1, 0, 0, True) == True
    assert verificarTablero(tablero1, "OSO", 1, 0, 0, 1, 3, True) == True
    assert verificarTablero(tablero1, "OSO", 1, 0, 0, 1, 0, True) == False
    assert verificarTablero(tablero0, "SOL", 0, 0, 1, 0, 0) == False
    assert verificarTablero(tablero1, "SOL", 0, 0, 1, 0, 0) == True

def test_escribirLetras():
    tablero = [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]
    resultado0 = [
        ['S', 'O', 'L'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]
    resultado1 = [
        ['S', 'O', 'L'],
        ['-', 'O', '-'],
        ['S', '-', '-']
    ]
    resultado2 = [
        ['S', 'O', 'L'],
        ['O', 'O', '-'],
        ['S', '-', '-']
    ]
    assert escribirLetras(tablero, "SOL", 0, 0, 1, 0) == resultado0
    assert escribirLetras(tablero, "LOS", 2, 0, -1, 1) == resultado1
    assert escribirLetras(tablero, "SOS", 0, 0, 0, 1) == resultado2

def test_crearTablero():
    tablero0 = [
        ['-', '-'],
        ['-', '-']
    ]
    tablero1 = [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]
    assert crearTablero(2) == tablero0
    assert crearTablero(3) == tablero1

def test_insertarPalabras():
    palabras = [("SOL", (0, 0), 0), ("LOS", (2, 0), 6)]
    tablero = [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]
    resultado = [
        ['S', 'O', 'L'],
        ['-', 'O', '-'],
        ['S', '-', '-']
    ]
    assert insertarPalabras(tablero, palabras) == resultado

def test_palabrasPalindromo():
    assert palabrasPalindromo("HOLA") == False
    assert palabrasPalindromo("NEUQUEN") == True

def test_noRepeticionPalabras():
    tablero = [
        ['S', 'O', 'L'],
        ['O', 'O', 'A'],
        ['S', 'H', 'M']
    ]
    palabras0 = [("MAL", (2, 2), 3), ("MOS", (2, 2), 7)]
    palabras1 = [("MAL", (2, 2), 3), ("SOS", (0, 0), 2)]
    palabras2 = [("SOL", (0, 0), 0), ("MAL", (2, 2), 3), ("LOS", (2, 0), 6)]
    assert noRepeticionPalabras(3, tablero, palabras0, 3) == True
    assert noRepeticionPalabras(3, tablero, palabras1, 3) == True
    assert noRepeticionPalabras(3, tablero, palabras2, 3) == False
