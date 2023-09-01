/*
Trabajo Práctico Final
Programación II
15/02/2022
María Agustina Torrano
Nro de legajo: T-2989/1
*/

#ifndef PROGRAMAENC_H
#define PROGRAMAENC_H

#include<stdio.h>
#include<stdlib.h> // (srand, rand, malloc)
#include<string.h>
#include<time.h> // Utilizado para generar un número aleatorio (time)
#include<assert.h> // Utilizado para verificar que el archivo se abra correctamente

/*
Representamos las palabras del lemario con un arreglo de cadenas al igual que
las palabras elegidas aleatoriamente para la sopa de letras.

Para facilitar la lectura de las signaturas nombramos los siguientes tipos:
Arreglo de cadenas: char**
Arreglo de numeros: long*
string: char*
archivo: FILE*
*/

// abrirArchivo : string, string -> archivo
// Toma un nombre de archivo y un modo para abrirlo y devuelve el objeto.
FILE* abrirArchivo(const char nombre_archivo[], char modo[]);

// numeroRepetido : long, Arreglo de long, long -> int
// Toma un número, una arreglo de numeros y la cantidad de numeros que hay en el arreglo y
// devuelve un 0 si el número no está repetido y un 1 si lo está.
int numeroRepetido(long numero, long *numeros, long cant_numeros);

// extencionRand : void -> unsigned long
// rand() toma numeros aleatorios en el intervalo [0, RAND_MAX]. RAND_MAX es como minimo 32767
// (en mi caso es asi), por lo tanto esta función extiende este rango.
unsigned long extencionRand();

// numerosAleatorios : int, long, Arreglo de long, long -> Arreglo de long
// Toma dos numeros (minimo, maximo), un arreglo con numeros y la cantidad de numeros que habrá
// en ese arreglo y devuelve otro arreglo de numeros aleatorios en el intervalo [minimo, maximo]
// y verifica que no esten repetidos.
long* numerosAleatorios (int minimo, long maximo, long* numeros, long cant_numeros);

// liberarPalabras : Arreglo de cadenas, long -> void
// Toma un arreglo de cadenas y un numero, el cual representa la cantidad de elementos que 
// posee el arreglo y libera la memoria utilizada para las palabras del arreglo al igual
// que la memoria utilizada para el arreglo.
void liberarPalabras(char **palabras, long cant_palabras);

// leerArchivo : archivo -> Arreglo de cadenas
// Toma un archivo y devuelve un arreglo de cadenas donde cada cadena es una linea del archivo
char** leerArchivo(FILE *archivo_objeto);

// cantidadLineas : Arreglo de cadenas -> long
// Toma un arreglo de cadenas y devuleve la cantidad de elementos del arreglo
long cantidadLineas(char** palabras);

// elegirPalabras : string, long -> Arreglo de cadenas
// Toma una cadena que representa el nombre del archivo de palabras y la cantidad de palabras a elegir,
// y devuelve un arreglo de cadenas con palabras del archivo elegidas al azar.
char** elegirPalabras(const char* nombre_archivo, long cant_palabras);

// bienvenida : void -> void
// Imprime por panatalla los carteles de bienvenida.
void bienvenida();

// agregarPalabras : string, int, archivo -> void
// Toma una cadena que representa el nombre del archivo de palabras, un entero que representa la cantidad
// de palabras que se desean para la sopa de letras y el archivo de salida, y escribe las palabras elegidas
// al azar en el archivo de salida.
void agregarPalabras(const char* nombre_archivo, long cant_palabras, FILE* salida);

// imprimir : void -> void
// Escribe todos los datos deseados en el archivo de salida.
void imprimir();

#endif