#include "tests.h"

void test_numeroRepetido() {
    long numero = 4;
    long cant_numeros = 3;
    long numeros[cant_numeros];
    numeros[0] = 1;
    numeros[1] = 2;
    numeros[2] = 3;
    assert(numeroRepetido(numero, numeros, cant_numeros) == 0);
    long numero2 = 3;
    assert(numeroRepetido(numero2, numeros, cant_numeros) == 1);
}

void test_cantidadLineas() {
    char* palabras[4];
    palabras[0] = "hola";
    palabras[1] = "arbol";
    palabras[2] = "guitarra";
    palabras[3] = NULL;
    assert(cantidadLineas(palabras) == 3);
}

void test_main() {
    test_numeroRepetido();
    test_cantidadLineas();

    return 0;
}