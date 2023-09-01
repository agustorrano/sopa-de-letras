#include "ProgramaEnC.h"

FILE* abrirArchivo(const char nombre_archivo[], char modo[]) {
    FILE *archivo;
    archivo = fopen(nombre_archivo, modo);

    // verifica que el archivo se pueda abrir correctamente
    assert(archivo != NULL);

    return archivo; 
}

int numeroRepetido(long numero, long *numeros, long cant_numeros) {
    int vof = 0;

    for (long i = 0; (i < cant_numeros && vof == 0); i++) {
        if (numeros[i] == numero) {
            vof = 1;
        }
    }

    return vof;
}

unsigned long extencionRand() {
    unsigned long x = rand();
    // significa (x * 2^15)
    x <<= 15; // 15 es el largo en bits de RAND_MAX

    // bitwise XOR es un operado lógico bit a bit en el cual los bits se comparan
    // uno con el otro. Cuando dos bits son idénticos, XOR devuelve un 0 y cuando los 
    // dos bits son diferentes, XOR devuelve un 1
    // utilizamos XOR porque RAND_MAX puede ser mayor a 15 bits
    x ^= rand();

    return x;
}

long* numerosAleatorios (int minimo, long maximo, long* numeros, long cant_numeros) {
    unsigned long numero_aleatorio;
    int numero_repetido;
    unsigned long random;
    srand(time(NULL));
    long tamanio_intervalo = maximo - minimo;

    for (long i = 0; i < cant_numeros ; i++) {

        // si el número aleatorio está repetido, busca otro
        do {
            if (maximo < RAND_MAX) {
                random = rand();
            }
            else {
                random = extencionRand();
            }
            numero_aleatorio = (random % tamanio_intervalo) + minimo;
            numero_repetido = numeroRepetido(numero_aleatorio, numeros, cant_numeros);
        } while (numero_repetido);

        numeros[i] = numero_aleatorio;
    }

    return numeros;
}

void liberarPalabras(char **palabras, long cant_palabras) {
  for (long i = 0; i < cant_palabras; free(palabras[i++]));
  free(palabras);
}

char** leerArchivo(FILE *archivo_objeto) {
    char linea[50];
    int largo_linea = 0;
    long cantidad_palabras = 1;

    // asigno memoria para un arreglo de cadenas
    char** palabras = malloc(sizeof(char*));
    assert(palabras != NULL);

    // asigno memoria para la primer cadena la cual sé que es "aaronico"
    palabras[0] = malloc(sizeof(char) * 9);
    assert(palabras[0] != NULL);

    strcpy(palabras[0], "aaronico");
    fscanf(archivo_objeto, "%s\n", linea); 
    fscanf(archivo_objeto, "%s\n", linea);

    for (int i = 0; EOF != fscanf(archivo_objeto, "%s\n", linea); i++) {
        cantidad_palabras = cantidad_palabras + 1;
        largo_linea = strlen(linea);
        char** palabras_aux;
        // redimensiono la memoria pedida anteriormente cada vez que se agrega una palabra
        palabras_aux = realloc(palabras, sizeof(char*) * cantidad_palabras);

        // si hay un OOM, se libera la memoria pedida anteriormente
        if (palabras_aux == NULL) {
            printf("\nERORR AL ASIGNAR MEMORIA\n\n");
            liberarPalabras(palabras, cantidad_palabras);
        }
        else {
            palabras = palabras_aux;
        }

        assert(palabras_aux != NULL);
        // asigno memoria para la cadena que se va a agregar
        palabras[cantidad_palabras - 1] = malloc(sizeof(char) * (largo_linea + 1));

        // si hay un OOM, se libera la memoria pedida anteriormente
        if (palabras[cantidad_palabras - 1] == NULL) {
            printf("\nERORR AL ASIGNAR MEMORIA\n\n");
            liberarPalabras(palabras, cantidad_palabras);
        }

        assert(palabras[cantidad_palabras - 1] != NULL);
        strncpy(palabras[cantidad_palabras - 1], linea, largo_linea);
        palabras[cantidad_palabras - 1][largo_linea] = '\0';
    }

    // se agrega para utilizar en la próxima función
    palabras[cantidad_palabras] = NULL;

    return palabras;
}

long cantidadLineas(char** palabras) {
    long contador = 0;

    while(palabras[contador] != NULL) {
        contador++;
    }

    return contador;
}

char** elegirPalabras(const char* nombre_archivo, long cant_palabras) {
    // asigno memoria para el arreglo que representa las palabras que despúes
    // serán utilizadas para armar la sopa de letras
    char **palabras_sopa = malloc(sizeof(char*) * cant_palabras);
    assert(palabras_sopa != NULL);

    long indice;
    int largo_palabra;

    FILE *archivo_objeto = abrirArchivo(nombre_archivo, "r");
    char** palabras = leerArchivo(archivo_objeto);
    fclose(archivo_objeto);

    long cant_lineas = cantidadLineas(palabras);
    long numeros[cant_palabras];
    long *indices_palabras = numerosAleatorios(0, cant_lineas, numeros, cant_palabras);

    for (long m = 0; m < cant_palabras; m++) {
        indice = indices_palabras[m];
        largo_palabra = strlen(palabras[indice]);
        // asigno memoria para la cadena
        palabras_sopa[m] = malloc(sizeof(char) * (largo_palabra + 1));

        // si hay un OOM se libera la memoria pedida anteriormente
        if (palabras_sopa[m] == NULL) {
            printf("\nERORR AL ASIGNAR MEMORIA\n\n");
            liberarPalabras(palabras_sopa, m);
        }

        assert(palabras_sopa[m] != NULL);
        strcpy(palabras_sopa[m], palabras[indice]);
    }

    liberarPalabras(palabras, cant_lineas);

    return palabras_sopa;
}

void bienvenida() {
    printf("\tLE DAMOS LA BIENVENIDA AL JUEGO DE LA SOPA DE LETRAS\n\n");
    printf("Para comenzar le pediremos algunos datos que necesitamos para armar la sopa de letras.\n\n");
    printf("Tenga en cuenta que a la hora de ingresar la complejidad habra 4 niveles representados con numeros:\n");
    printf("0 Facil\n1 Medio\n2 Dificil\n3 Muy dificil\n\n");
}

void agregarPalabras(const char* nombre_archivo, long cant_palabras, FILE* salida) {
    char **palabras_sopa = elegirPalabras(nombre_archivo, cant_palabras);

    // escribe las palabras en el archivo de salida
    for (long i = 0; i < cant_palabras; i++) {
        fprintf(salida, "%s\n", palabras_sopa[i]);
    }

    liberarPalabras(palabras_sopa, cant_palabras);
} 

void imprimir() {
    const char* nombre_archivo;
    printf("Ingrese un archivo que contenga palabras: ");
    scanf("%s", nombre_archivo);

    int dimension;
    printf("Ingrese la dimension de la sopa de letras (tiene la misma cantidad de filas que de columnas): ");
    scanf("%d", &dimension);

    // dimension debe ser un número mayor que 0
    while (dimension <= 0) {
        printf("\nERROR. NUMERO NO VALIDO, PRUEBE INGRESANDO UN NUMERO NATURAL\n\n");
        printf("Ingrese la dimension de la sopa de letras (tiene la misma cantidad de filas que de columnas): ");
        scanf("%d", &dimension);
    }

    long cant_palabras;
    printf("Ingrese la cantidad de palabras a buscar en la sopa de letras: ");
    scanf("%ld", &cant_palabras);

    // cant_palabras debe ser un número mayor que 0
    while (cant_palabras <= 0) {
        printf("\nERROR. NUMERO NO VALIDO, PRUEBE INGRESANDO UN NUMERO NATURAL\n\n");
        printf("Ingrese la cantidad de palabras a buscar en la sopa de letras: ");
        scanf("%ld", &cant_palabras);
    }

    int complejidad;
    printf("Ingrese un numero de 0 al 3 segun la complejidad que desee: ");
    scanf("%d", &complejidad);

    // complejidad debe ser un número en el intervalo [0, 3]
    while (complejidad != 0 && complejidad != 1 && complejidad != 2 && complejidad != 3) {
        printf("\nERROR. NUMERO NO VALIDO, PRUEBE CON UN NUMERO EN EL INTERVALO [0, 3]\n\n");
        printf("Ingrese un numero de 0 al 3 segun la complejidad que desee: ");
        scanf("%d", &complejidad);
    }

    FILE *salida = fopen("salida_sopa.txt", "a");
    fprintf(salida, "DIMENSION\n%d\nPALABRAS\n", dimension);
    agregarPalabras(nombre_archivo, cant_palabras, salida);
    fprintf(salida, "COMPLEJIDAD\n%d\n", complejidad);
    fclose(salida);
}

int main() {
    bienvenida();
    imprimir();

    return 0;
}
