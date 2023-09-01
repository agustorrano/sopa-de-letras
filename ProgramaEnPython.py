from random import shuffle
import copy

'''
Representamos la entrada del archivo en C como un diccionario donde las claves
serán "DIMENSION", el cual contendrá un entero, "PALABRAS", el cual contendrá
una lista de strings, y "COMPLEJIDAD", el cual contendrá un entero.
Cuando ya tengamos la posición y dirección de cada palabra se cambiará el valor
de la clave "PALABRAS" por una lista de tuplas que tienen como primer elemento
un string representando la palabra, como segundo elemento la posición inicial de
la misma (una tupla (x, y)), y como tercer elemento un entero que representa el 
indice de la siguiente lista de direcciones:
[(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
Finalmente, representaremos el tablero de la sopa de letras como una lista de listas
de caracteres.

Para facilitar la lectura de las signaturas nombramos los siguientes tipos:

Palabras: Lista(Str)
Posicion: Tupla(Int, Int)
Direccion: Tupla(Int, Int)
Palabra con posicion y direccion: Tupla(Str, Posicion, Int)
Palabras con posicion y direccion: Lista(Palabra con posicion y direccion)
Jugada: Diccionario(Str, Int | Palabras | Int)
Nueva jugada: Diccionario(Str, Int | Palabras con posicion y direccion | Int)
Tablero: Lista(Lista(Char))
'''

# leerArchivo : Str -> Jugada
'''
Lee y parsea un archivo con las características que debe tener la sopa de letras, 
y devuelve un diccionario, donde diccionario[dimension] es la dimensión que debe
tener la sopa de letras, diccionario[palabras] es una lista con las palabras a
encontrar, y diccionario[complejidad] es el nivel de dificultad:
    FÁCIL: 0
    MEDIO: 1
    DIFÍCIL: 2
    MUY DIFÍCIL: 3

Ejemplo de archivo:
    DIMENSION
    8
    PALABRAS
    maria
    arbol
    sol
    COMPLEJIDAD
    1
    
Ejemplo de retorno:
    {"DIMENSION": 8, "PALABRAS": ["MARIA", "ARBOL", "SOL"], "COMPLEJIDAD": 1} 
'''
def leerArchivo(archivo):
    jugada = {}
    palabras = []

    # con "with open file as" no nos tenemos que acordar de cerrar el archivo
    # porque esto sucede automáticamente
    with open(archivo) as f:
        clave_dimension = f.readline()
        jugada[clave_dimension.strip()] = int(f.readline().strip())
        clave_palabras = f.readline()
        palabra = f.readline().strip()

        while palabra != "COMPLEJIDAD":
            # convierte las palabras en mayúscula
            palabra = palabra.upper()
            palabras = palabras + [palabra]
            # elimina los espacios iniciales y finales de un string
            palabra = f.readline().strip()
        
        jugada[clave_palabras.strip()] = palabras
        clave_complejidad = palabra
        jugada[clave_complejidad] = int(f.readline().strip())

    return jugada

# palabrasSuperpuestas : Int -> Bool
'''
Evalua si las palabras se pueden superponer según la complejidad, es decir, si se
pueden compartir letras.

entrada: 0; salida: False
entrada: 1; salida: False
entrada: 2; salida: False
entrada: 3; salida: True
'''
def palabrasSuperpuestas(complejidad):
    return complejidad == 3

# palabrasPalindromo : Str -> Bool
'''
Determina si una palabra es palíndromo, es decir, que es igual si se lee de
izquierda a derecha que de derecha a izquierda.
 
entrada: "hola"; salida: False
entrada: "neuquen"; salida: True
'''
def palabrasPalindromo(palabra):
    return palabra == palabra[::-1]

# indicesDirecciones : Int -> Lista(Int)
'''
Toma el nivel de complejidad y devuleve una lista de números la cuál representa 
las direcciones que pueden tener las palabras teniendo en cuenta que:
    Horizontal de izquierda a derecha = 0
    Horizontal de derecha a izquierda = 1
    Vertical de arriba a abajo = 2
    Vertical de abajo a arriba = 3
    Diagonal de esquina superior izquierda a esquina inferior derecha: 4
    Diagonal de esquina inferior izquierda a esquina superior derecha: 5
    Diagonal de esquina superior derecha a esquina inferior izquierda: 6
    Diagonal de esquina inferior derecha a esquina superior izquierda: 7

entrada: 0; salida: [0, 2]
entrada: 1; salida: [0, 2, 4]
entrada: 2; salida: [0, 1, 2, 3, 4, 5, 6, 7]
entrada: 3; salida: [0, 1, 2, 3, 4, 5, 6, 7]
'''
def indicesDirecciones(complejidad):

    if complejidad == 0:
        lista_indices_direcciones = [0, 2]  
    
    elif complejidad == 1:
        lista_indices_direcciones = [0, 2, 4] 
    
    else:
        lista_indices_direcciones = [0, 1, 2, 3, 4, 5, 6, 7]
    
    return lista_indices_direcciones

# posicionesConDireccion : Int, Int -> Lista(Tupla(Posicion, Int))
'''
Toma la dimensión de la sopa de letras y la complejidad y devuelve una lista de todas
las combinaciones posibles de posiciones (x, y) con direcciones (indice de dirección).

entrada: 2, 1; salida: [((0, 0), 0), ((0, 0), 2), ((0, 0), 4), ((0, 1), 0), ((0, 1), 2), 
    ((0, 1), 4), ((1, 0), 0), ((1, 0), 2), ((1, 0), 4), ((1, 1), 0), ((1, 1), 2), ((1, 1), 4)]
entrada: 3, 0; salida: [((0, 0), 0), ((0, 0), 2), ((0, 1), 0), ((0, 1), 2), ((0, 2), 0),
    ((0, 2), 2), ((1, 0), 0), ((1, 0), 2), ((1, 1), 0), ((1, 1), 2), ((1, 2), 0), ((1, 2), 2),
    ((2, 0), 0), ((2, 0), 2), ((2, 1), 0), ((2, 1), 2), ((2, 2), 0), ((2, 2), 2)]
'''
def posicionesConDireccion(dimension, complejidad):
    posiciones = []
    lista_posicion_direccion = []
    lista_indices_direcciones = indicesDirecciones(complejidad)

    # crea una lista con todas las combinaciones posibles de posiciones según la dimensión
    for x0 in range(dimension):
        for y0 in range(dimension):
            posiciones.append((x0, y0))
    
    # crea una lista con todas las combinaciones posibles de posición y dirección según
    # la dimensión y la complejidad 
    for posicion in posiciones:
        for indice_direccion in lista_indices_direcciones:
            lista_posicion_direccion.append((posicion, indice_direccion))
    
    return lista_posicion_direccion

# direccionPalabra : Int -> Direccion
'''
Toma un índice de dirección y, según lo que vimos antes, retorna una tupla cuyo primer
elemento es la dirección en x y el segundo la dirección en y.
 
entrada: 0; salida: (1, 0) -> (Horizontal de izquierda a derecha)
entrada: 3; salida: (0, -1) -> (Vertical de abajo a arriba)
entrada: 7; salida: (-1, -1) -> (Diagonal de esquina inferior derecha a esquina superior izquierda)
'''
def direccionPlabra(indice_direccion):
    direcciones = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
    direccion = direcciones[indice_direccion]

    return direccion

# separaTupla : Tupla(Posicion, Int), Bool, Bool, Bool, Bool -> Int
'''
Toma una tupla con una posición y un índice de dirección y según lo que se quiera utilizar
(posición en x, posición en y, dirección en x o dirección en y), lo devolverá por su cuenta.
Para devolver lo que desea, se debe poner True en el espacio correspondinte (NO SE PUEDE PONER
TRUE EN MÁS DE UN ESPACIO).

entrada: ((0, 3), 2), True; salida: 0
entrada: ((0, 3), 2), False, True; salida: 3
entrada: ((0, 3), 2), False, False, True; salida: 0
entrada: ((0, 3), 2), False, False, False, True; salida: 1
'''
def separaTupla(tupla_posicion_direccion, devuelve_x = False, devuelve_y = False, devuelve_dx = False, devuelve_dy = False):
    posicion = tupla_posicion_direccion[0]
    indice_direccion = tupla_posicion_direccion[1]

    x = posicion[0]
    y = posicion[1]

    direccion = direccionPlabra(indice_direccion)
    dx = direccion[0]
    dy = direccion[1]

    if devuelve_x:
        return x
    elif devuelve_y:
        return y
    elif devuelve_dx:
        return dx
    elif devuelve_dy:
        return dy

# palabraEntraEnTablero : Int, Str, Int, Int, Int, Int -> Bool
'''
Toma la dimensión de la sopa de letras, una palabra, la posición inicial de la misma tanto
en x como en y, y su dirección tanto en x como en y, y devuelve True si la palabra entra en
el tablero de la sopa de letras y False en caso contrario.

entrada: 5, "lapiz", 0, 0, 1, 0; salida: True
entrada: 5, "lapiz", 1, 0, 1, 0; salida: False
entrada: 5, "celular", 0, 0, 1, 1; salida: False
'''
def palabraEntraEnTablero(dimension, palabra, pos_inicial_x, pos_inicial_y, dx, dy):
    pos_fianl_x = pos_inicial_x + (len(palabra) - 1) * dx
    pos_final_y = pos_inicial_y + (len(palabra) - 1) * dy

    # Para entrar en el tablero la posición inicial tanto en x como en y debe estar
    # dentro del tablero, es decir, debe ser mayor o igual a 0 y menor a la dimensión
    # del tablero. La posición final debe cumplir lo mismo.
    b1 = pos_inicial_x >= 0
    b2 = pos_inicial_x < dimension
    b3 = pos_inicial_y >= 0
    b4 = pos_inicial_y < dimension
    b5 = pos_fianl_x >= 0
    b6 = pos_fianl_x < dimension
    b7 = pos_final_y >= 0
    b8 = pos_final_y < dimension

    return b1 and b2 and b3 and b4 and b5 and b6 and b7 and b8

# verificarTablero : Tablero, Str, Int, Int, Int, Int, Int, Bool -> Bool
'''
Verifica que una palabra aparezca en la posición y dirección dadas permitiendo huecos,
es decir, una palabra puede no tener todas las letras pero igual se puede verificar lo
dicho anteriormente. Además, tiene en cuenta la complejidad para ver si se pueden compartir
letras.
'''
def verificarTablero(tablero, palabra, x, y, dx, dy, complejidad, permitir_huecos = False):

    for letra in palabra:

        # si la letra en el tablero es distinta a la letra de la palabra pude ser que haya
        # un hueco, es decir '-', o puede haber otra letra
        if tablero[y][x] != letra:
            if not permitir_huecos:
                return False
            elif tablero[y][x] != '-':
                return False
        
        # si la letra en el tablero es igual a la letra de la palabra y, además, se permiten
        # huecos, entonces las palabras deben permitir compartir letras (complejidad == 3)
        elif tablero[y][x] == letra:
            if not palabrasSuperpuestas(complejidad) and permitir_huecos:
                return False
        
        # sigue con la proxima letra de la palabra
        x += dx
        y += dy
    
    return True

# escribirLetras : Tablero, Str, Int, Int, Int -> Tablero 
'''
Escribe una palabra en el tablero según su posición y dirección.
'''
def escribirLetras(tablero, palabra, x, y, dx, dy):

    for letra in palabra:
        tablero[y][x] = letra
        x += dx
        y += dy
    
    return tablero

# elegirPosicionDireccion : Int, Tablero, Palabras, Int, Int, Palabras con posicion y direccion 
# -> Palabras con posicion y direccion | None
'''
Elige aleatoriamente las posiciones y direcciones de las palabras verificando que entren en
el tablero y verficando que puedan escribirse en el tablero.
'''
def elegirPosicionDireccion(dimension, tablero, palabras, complejidad, indice = 0, palabras_con_direc_pos = []):

    # si el indice es mayor o igual que el largo de la lista de palabras, quiere decir que no
    # hay más palabras a las cuales se les pueda elegir una posición y dirección
    if indice >= len(palabras):
        return palabras_con_direc_pos
    
    palabra = palabras[indice]
    lista_posicion_direccion = posicionesConDireccion(dimension, complejidad)
    shuffle(lista_posicion_direccion) # mezclamos la lista

    for posicion_direccion in lista_posicion_direccion:
        x0 = separaTupla(posicion_direccion, True)
        y0 = separaTupla(posicion_direccion, False, True)
        dx = separaTupla(posicion_direccion, False, False, True)
        dy = separaTupla(posicion_direccion, False, False, False, True)

        # si la palabra no entra en el tablero con la posición y dirección 
        # dadas, prueba con la siguiente
        if not palabraEntraEnTablero(dimension, palabra, x0, y0, dx, dy):
            continue

        # copiamos el tablero para evitar sobreescribir los datos
		# que vamos a necesitar al intentar usar otra posicion y dirección
        nuevo_tablero = copy.deepcopy(tablero)
        tablero_posible = verificarTablero(nuevo_tablero, palabra, x0, y0, dx, dy, complejidad, True)

        # verifica que sea posible escribir la palabra en el tablero y
        # si no es viable prueba con la siguinete posición y dirección
        if not tablero_posible:
            continue

        # ponemos la palabra sobre el tablero, agregamos la misma a la lista 
        # con su respectiva posición y dirección y pasamos a la siguiente palabra 
        # haciendo recursion en indice+1
        escribirLetras(nuevo_tablero, palabra, x0, y0, dx, dy)
        palabras_con_direc_pos = palabras_con_direc_pos + [(palabra, posicion_direccion[0], posicion_direccion[1])]
        siguiente_palabra = elegirPosicionDireccion(dimension, nuevo_tablero, palabras, complejidad, indice + 1, palabras_con_direc_pos)
        
        # es posible armar la sopa
        if siguiente_palabra != None:
            return siguiente_palabra
        # no es posible armar la sopa, entonces eliminamos el ultimo elemento de
        # la lista y probamos con otra posicion y direccion
        else:
            largo_lista = len(palabras_con_direc_pos)
            palabras_con_direc_pos[(largo_lista - 1):largo_lista] = []
            continue
    
    # me parece que es necesario que esta función devuelva None para hacer posible 
    # la recursión y para luego determinar si se puede hacer la sopa de letras o no
    return None

# tableroPosible : Int, Tablero, Palabras, Int -> Bool
'''
Determina si con las palabras, la dimensión y la complejidad, es posible armar el
tablero. Si es posible devuelve True, en caso contrario devuelve False.
'''
def tableroPosible(dimension, tablero, palabras, complejidad):

    # si la función anterior devuleve None, entonces no se puede hacer la 
    # sopa de letras
    if elegirPosicionDireccion(dimension, tablero, palabras, complejidad) == None:
        return False
    else:
        return True

# crearTablero : Int -> Tablero
'''
Toma una dimensión y crea un tablero vacío donde cada posición será '-'.
 
entrada: 2; salida: [['-', '-'], ['-', '-']]
entrada: 3; salida: [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
'''
def crearTablero(dimension):
    tablero_vacio = []

    for i in range(dimension):
        tablero_vacio.append(['-'] * dimension)
    
    return tablero_vacio

# nuevoDiccionarioJugada : Jugada -> Nueva jugada
'''
Genera un nuevo diccionario donde el valor de "PALABRAS" tendrá las palabras con sus
respectivas posiciones y direcciones
'''
def nuevoDiccionarioJugada(jugada):
    dimension = jugada["DIMENSION"]
    palabras = jugada["PALABRAS"]
    complejidad = jugada["COMPLEJIDAD"]
    tablero = crearTablero(dimension)
    palabras_con_direc_pos = elegirPosicionDireccion(dimension, tablero, palabras, complejidad)
    # cambia el valor de "PALABRAS"
    jugada["PALABRAS"] = palabras_con_direc_pos

    return jugada

# insertarPalbras -> Tablero, Palabras con posicion y direccion -> Tablero
'''
Escribe las palabras en el tablero según su posición y dirección.
'''
def insertarPalabras(tablero, palabras_con_direc_pos):

    for palabra, posicion, indice_direccion in palabras_con_direc_pos:
        x = posicion[0]
        y = posicion[1]
        direccion = direccionPlabra(indice_direccion)
        dx = direccion[0]
        dy = direccion[1]
        # copiamos el tablero para evitar sobreescribir
        nuevo_tablero = copy.deepcopy(tablero)
        tablero = escribirLetras(nuevo_tablero, palabra, x, y, dx, dy)
    
    return tablero

# repeticionPalabras : Int, Tablero, Palabras con posicion y direccion, Int -> Bool
'''
Evalua si se repiten las palabras que se deben buscar en la sopa de letras teniendo en
cuenta las palabras palíndromo.
'''
def noRepeticionPalabras(dimension, tablero, palabras_con_direc_pos, complejidad):

    for palabra, posicion, direccion in palabras_con_direc_pos:
        palabra_palindromo = palabrasPalindromo(palabra)
        direcciones = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        apariciones_por_direccion = [0, 0, 0, 0, 0, 0, 0, 0] 

        for i, (dx, dy) in enumerate(direcciones):
            for x0 in range(dimension):
                for y0 in range(dimension):

                    if not palabraEntraEnTablero(dimension, palabra, x0, y0, dx, dy):
                        continue

                    # verfica cuantas veces apaece una palabara en la misma dirección
                    apariciones_por_direccion[i] += verificarTablero(tablero, palabra, x0, y0, dx, dy, complejidad)    
        
        # verifica que la palabra aparezca una vez en la
        # dirección dada al principio de la funcion
        if apariciones_por_direccion[direccion] != 1:
            return False    
        
        # si la palabra es palíndromo, elimina los casos en
        # los que la palabra pueda aparecer más de una vez
        if palabra_palindromo:
            apariciones_por_direccion[3] = 0
            apariciones_por_direccion[4] = 0
            apariciones_por_direccion[6] = 0
            apariciones_por_direccion[7] = 0    
        
        apariciones_totales = sum(apariciones_por_direccion)    
        
        # la palabra debe aperecer solo una vez en toda la sopa
        if apariciones_totales != 1:
            return False        
    
    return True

# insertarLetras : Int, Tablero, Int, Int -> Tablero
'''
Escribe letras aleatorias en el tablero.
'''
def insertarLetras(dimension, tablero, x, y):
    
    # estamos al final del tablero
    if y >= dimension:
        return tablero
    
    # estamos al final de la fila entonces pasamos a la siguiente
    if x >= dimension:
        return insertarLetras(dimension, tablero, 0, y + 1)
    
    # ya hay una letra entntonces pasamos a la siguente posición
    if tablero[y][x] != '-':
        return insertarLetras(dimension, tablero, x + 1, y) 
    
    # hay un espacio vacío entonces agregamos una letra aleatoria
    abecedario = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    shuffle(abecedario)
    tablero[y][x] = abecedario[0]
    
    # pasamos a la siguente posición
    return insertarLetras(dimension, tablero, x + 1, y)

# tableroSinRepeticion : Int, Tablero, Palabras con posicion y direccion, Int -> Tablero
'''
Escribe letras aleatorias en el tablero hasta que no haya repeticiones de las palabras a
buscar. Devuelve el tablero final.
'''
def tableroSinRepeticion(dimension, tablero, palabras_con_direc_pos, complejidad):
    posible_tablero = insertarLetras(dimension, tablero, 0, 0)
    
    while not noRepeticionPalabras(dimension, posible_tablero, palabras_con_direc_pos, complejidad):
        posible_tablero = insertarLetras(dimension, tablero, 0, 0)
    
    return posible_tablero

# completarTablero : Int, Tablero, Palabras con posicion y direccion, Int -> Str
'''
Escribe las palabras a buscar y rellena el tablero con letras aleatorias sin repetir las
palabras. Luego transforma el tablero en un string devolviendo la sopa de letras definitiva.
'''
def completarTablero(dimension, tablero_vacio, palabras_con_direc_pos, complejidad):
    lista_filas_sopa = []
    tablero_con_palabras = insertarPalabras(tablero_vacio, palabras_con_direc_pos)
    tablero_completo = tableroSinRepeticion(dimension, tablero_con_palabras, palabras_con_direc_pos, complejidad)
    
    # transformamos el tablero en un string
    for fila in tablero_completo:
        lista_filas_sopa = lista_filas_sopa + [" ".join(fila) + "\n"]
    
    sopa_de_letras = "".join(lista_filas_sopa)
    
    return sopa_de_letras

# crearSopaDeLetras : Nueva jugada -> Str
'''
Dado el archivo de jugada, devuelve un string con las palabras a buscar y la sopa de letras.
'''
def crearSopaDeLetras(dic_jugada):
    dimension = dic_jugada["DIMENSION"]
    palabras = dic_jugada["PALABRAS"]
    complejidad = dic_jugada["COMPLEJIDAD"]
    tablero = crearTablero(dimension)
    
    if not tableroPosible(dimension, tablero, palabras, complejidad):
        return "\nERROR, NO ES POSIBLE CREAR LA SOPA DE LETRAS\n"
    
    else:
        dic_jugada_nueva = nuevoDiccionarioJugada(dic_jugada)
        palabras_con_direc_pos = dic_jugada_nueva["PALABRAS"]
        palabras_buscar = ", ".join(palabras)
        sopa_de_letras = completarTablero(dimension, tablero, palabras_con_direc_pos, complejidad)
        mensaje = "\nLas palabras a buscar son: " + "[" + palabras_buscar + "]" + "\n\n"
        return mensaje + sopa_de_letras

# main : None -> Str
'''
Toma el input del usurio y genera la sopa de letras.
'''
def main():
    print("\nAhora crearemos la Sopa De Letras según sus requerimientos.")
    print("Tenga en cuenta que las palabras que debe buscar en la Sopa De Letras le serán proporcionadas.\n")
    archivo_jugada = input("Ingrese la ruta al archivo de la jugada (nombre del archivo de salida de C): ")
    dic_jugada = leerArchivo(archivo_jugada)
    sopa_de_letras = crearSopaDeLetras(dic_jugada)
    
    return sopa_de_letras

# print(main())
